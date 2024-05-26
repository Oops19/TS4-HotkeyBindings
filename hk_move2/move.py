#
# LICENSE None / You are allowed to use this mod in TS4
# © 2024 https://github.com/Oops19
#


import math
from typing import Union, Any, Tuple

import camera
import routing

from interactions.utils import routing
from objects.game_object import GameObject

from sims.sim import Sim
from sims.sim_info import SimInfo
# noinspection PyUnresolvedReferences
from sims4.math import Vector3, Quaternion, Transform, Location

import services

from hotkey_bindings.modinfo import ModInfo
from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from ts4lib.classes.coordinates.std_euler_angle import StdEulerAngle
from ts4lib.classes.coordinates.std_quaternion import StdQuaternion
from ts4lib.classes.coordinates.std_vector3 import StdVector3
from ts4lib.utils.singleton import Singleton


log: CommonLog = CommonLogRegistry.get().register_log(ModInfo.get_identity(), 'Move')
log.enable()


class Move(metaclass=Singleton):
    def __init__(self, item: Union[SimInfo, GameObject, None] = None, trace_log: bool = True):  # TODO
        self._item = item
        self._trace_log = trace_log

    @property
    def trace_log(self) -> bool:
        return self._trace_log

    @trace_log.setter
    def trace_log(self, do_log: bool):
        self._trace_log = bool(do_log)

    @property
    def item(self) -> Union[SimInfo, GameObject, None]:
        return self._item

    @item.setter
    def item(self, obj: Union[SimInfo, GameObject, None]):
        self._item = obj

    def _game_object_location(self, _object) -> Tuple[Vector3, Quaternion, int, int, int]:
        try:
            position: Vector3 = _object._location.transform.translation
            orientation: Quaternion = _object._location.transform.orientation
            level: int = getattr(_object._location, 'level', 0)
            # level = _object._location.routing_surface.secondary_id
            routing_surface = getattr(_object, 'routing_surface', routing.SurfaceType.SURFACETYPE_WORLD)
            if _object.parent:
                parent_object_id = _object.parent.id
            else:
                parent_object_id = None
            return position, orientation, level, routing_surface, parent_object_id
        except Exception as e:
            log.warn(f"Oops ({e}). Couldn't get generic position of '{_object}'")
            return None, None, None, None, None

    def relocate(self, move_or_rotate: bool = True, camera_or_world: bool = True, convert_deg_to_rad: bool = False, item: Union[Sim, GameObject] = None, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> Tuple[Vector3, Quaternion, Union[Sim, GameObject], Any]:
        """
        @param move_or_rotate: bool = True - Move the item; False - Rotate the item
        @param camera_or_world: bool = True - Move the item along axis relative to the camera (x=right; z=to camera); False - Move the item along the world axis; Only valid for 'relocate_type_move=False'
        @param convert_deg_to_rad: bool = False - Angles in rad; False - Angles in deg; Only valid for 'relocate_type_move=False'
        @param item: [SimInfo, GameObject] - The object or sim to move. If it is None the stored value will be used if available. Otherwise the active sim will be used.
        @param x: float = 0.0 - The x offset or x/pitch angle
        @param y: float = 0.0 - The y offset or y/yaw angle
        @param z: float = 0.0 - The z offset or z/roll angle
        """
        if item is None:
            if self.item:
                item = self.item
            else:
                item = CommonSimUtils.get_active_sim()
        if self._trace_log:
            log.debug(f"relocate(move={move_or_rotate}, camera={camera_or_world}, item={item}, x={x}, y={y} z={z})")

        position, orientation, level, routing_surface, parent_object_id = self._game_object_location(item)
        if position is None:
            try:
                if isinstance(item, Sim):
                    (position, orientation, level, _surface_id) = item.get_location_for_save()
                    _zone_id = services.current_zone_id()
                    routing_surface = routing.SurfaceIdentifier(_zone_id, level, routing.SurfaceType.SURFACETYPE_WORLD)
                else:
                    position = item.position
                    orientation = item.orientation
                    # _level = getattr(item, 'level', 0)
                    routing_surface = getattr(item, 'routing_surface', routing.SurfaceType.SURFACETYPE_WORLD)
            except Exception as e:
                log.warn(f"Oops ({e}). Couldn't get position of '{item}'")

        q = StdQuaternion(orientation.w, orientation.x, orientation.y, orientation.z)
        if self._trace_log:
            v = StdVector3(position.x, position.y, position.z)
            ea: StdEulerAngle = q.euler_angles()
            log.debug(f"Location: {v} {q} {ea.deg()}")

        if move_or_rotate is False:
            '''
            Rotate the item
            Assign absolute angle values to create a quaternion.
            Avoid 'un-expected' rotation issues depending on the current pitch/roll/yaw values and/or gimbal lock
            '''
            roll = y  # in ° (deg)
            pitch = z
            yaw = x
            relative_euler_angle = StdEulerAngle(roll, pitch, yaw, convert_deg_to_rad=convert_deg_to_rad)
            relative_q: StdQuaternion = relative_euler_angle.quaternion()
            q = q * relative_q
            orientation = q.as_ts4_quaternion()
        else:
            ''' Move the item around '''
            relative_euler_angle = StdEulerAngle()
            # 'move_abs', 'move_rel', 'go_to', 'cam_to'
            if camera_or_world is False:
                # Move along world coordinates
                x = position.x + x
                y = position.y + y
                z = position.z + z
                position = Vector3(x, y, z)
            else:
                # Move item along camera axis, x=right, z=to viewer
                cam_angle = self._get_angle_to_camera(item)
                # Rotate the supplied delta values f(cam_angle)
                x2 = x * math.cos(cam_angle) - z * math.sin(cam_angle)
                y2 = y
                z2 = x * math.sin(cam_angle) + z * math.cos(cam_angle)
                # Add the values to the current position
                x = position.x + x2
                y = position.y + y2
                z = position.z + z2
                position = Vector3(x, y, z)

        if self._trace_log:
            v = StdVector3(position.x, position.y, position.z)
            log.debug(f"Location: {v} {q} ±{relative_euler_angle.deg()} (NEW)")

        return position, orientation, item, routing_surface

    def _get_angle_to_camera(self, sim: Sim) -> float:
        angle = 0.0
        camera_position = None
        sim_position = None
        try:
            (sim_position, orientation, level, surface_id) = sim.get_location_for_save()
            camera_position = camera._camera_position

            dx = camera_position.x - sim_position.x
            dz = camera_position.z - sim_position.z

            x2 = 0
            z2 = 1

            n = math.sqrt(dx ** 2 + dz ** 2) * math.sqrt(x2 * x2 + z2 * z2)
            if n != 0:
                z = dx * x2 + dz * z2
                a = z / n
                angle = math.acos(a)
                if dx > x2:
                    angle *= -1

        except Exception as e:
            pass

        if self.trace_log:
            log.debug(f"𝛼={angle:.3f} 📷={camera_position}, 🤰={sim_position}")
        return angle


Move()
