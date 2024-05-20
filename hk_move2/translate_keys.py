#
# LICENSE None / You are allowed to use this mod in TS4
# © 2024 https://github.com/Oops19
#


import math
from typing import Union

import camera
import services
import sims4
from hk_move2.move import Move

from objects.game_object import GameObject

from sims.sim import Sim
from sims.sim_info import SimInfo
# noinspection PyUnresolvedReferences
from sims4.math import Vector3, Quaternion, Transform, Location

from hotkey_bindings.modinfo import ModInfo
from sims4communitylib.classes.math.common_vector3 import CommonVector3
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry
from sims4communitylib.utils.misc.common_camera_utils import CommonCameraUtils
from sims4communitylib.utils.sims.common_sim_interaction_utils import CommonSimInteractionUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from ts4lib.utils.simple_ui_notification import SimpleUINotification
from ts4lib.utils.singleton import Singleton
from ui.ui_dialog_notification import UiDialogNotification


log: CommonLog = CommonLogRegistry.get().register_log(ModInfo.get_identity(), 'Move')
log.enable()


class TranslateKeys(metaclass=Singleton):
    self = None

    def __init__(self, log_movement: bool = False):
        self.move = Move()
        self.move_mode_move_or_rotate = True  # True - Move the item; False - Rotate the item
        self.move_axes_camera_or_world = True  # True - Move along axes relative to the camera (x=right, z=to camera); False - Move along world coordinates
        self.to_mode_sim_or_camera = True  # True - Send sim to location; False - Point camera to location  # TODO - can't be set
        self._log_movement = log_movement
        TranslateKeys.self = self
    
    @property
    def log_movement(self) -> bool:
        return self._log_movement
    
    @log_movement.setter
    def log_movement(self, do_log: bool):
        self._log_movement = bool(do_log)
        self.move.log_movement = do_log

    @property
    def item(self) -> Union[SimInfo, GameObject, None]:
        return self.move.item

    @item.setter
    def item(self, obj: Union[SimInfo, GameObject, None]):
        self.move.item = obj

    @property
    def move_mode(self) -> bool:
        return self.move_mode_move_or_rotate

    @move_mode.setter
    def move_mode(self, move_or_rotate: bool):
        """ True=Move; False=Rotate """
        self.move_mode_move_or_rotate = bool(move_or_rotate)
        
    @property
    def move_axes(self) -> bool:
        return self.move_axes_camera_or_world

    @move_axes.setter
    def move_axes(self, camera_or_world: bool):
        """ True=Move; False=Rotate """
        self.move_axes_camera_or_world = bool(camera_or_world)

    @staticmethod
    def toggle_move_rotate():
        TranslateKeys.self._toggle_move_rotate()

    def _toggle_move_rotate(self):
        """
        Input can either move the sim/object or rotate it.
        """
        self.move_mode_move_or_rotate = not self.move_mode_move_or_rotate
        log.debug(f"toggle_move_rotate({self.move_mode_move_or_rotate})")
        if self.move_mode_move_or_rotate:
            title = '> Movement'
            text = 'Sim will be moved around (not rotated).'
        else:
            title = '> Rotation'
            text = 'Sim will be rotated (not moved around)).'
        SimpleUINotification().show(title, text)

    @staticmethod
    def toggle_move_mode():
        TranslateKeys.self._toggle_move_mode()

    def _toggle_move_mode(self):
        """
        Input can either move along the axis defined by the screen/camera (natural left/right/closer/away) or use the TS4 world coordinates
        """
        if not self.move_mode_move_or_rotate:
            # Change from Rotate Mode to Move Mode
            self._toggle_move_rotate()
        self.move_axes_camera_or_world = not self.move_axes_camera_or_world
        log.debug(f"toggle_move_mode({self.move_axes_camera_or_world})")
        if self.move_axes_camera_or_world:
            title = '> Camera Movement'
            text = 'Sim will be moved naturally on the screen, relative to the camera.'
        else:
            title = '> World Movement'
            text = 'Sim will be moved along the axes of the sim world.'
        SimpleUINotification().show(title, text)

    @staticmethod
    def move_rot_sim(direction: str, item: Union[Sim, GameObject, None] = None):
        TranslateKeys.self._move_rot_sim(direction, item)

    def _move_rot_sim(self, direction: str, item: Union[Sim, GameObject, None] = None):
        """
        @param direction: 'command x y z' - Supported commands are: 'rotate'; 'move', 'move_rel', 'move_abs'; 'go_to', 'cam_to'
        The command 'move' will be converted to 'move_rel', move_abs' or 'rotate' depending on 'mode_move_rotate' and 'move_relative_absolute'
        The command 'to' will be converted to 'go_to' or 'cam_to' depending on 'to_sim_camera'
        """
        command, _x, _y, _z = direction.split(' ', 3)
        factor = 1
        if command == 'to':
            if self.to_mode_sim_or_camera:
                command = 'go_to'
            else:
                command = 'cam_to'
        elif command == 'move':
            if self.move_mode:
                if self.move_axes:
                    command = 'move_rel'
                else:
                    command = 'move_abs'
            else:
                factor = 90
                command = 'rotate'
        x = float(_x) * factor
        y = float(_y) * factor
        z = float(_z) * factor
        if self._log_movement:
            log.debug(f"move_rot_sim({command} {x} {y} {z}) - ({item})")
        self.move_gp(command, x, y, z, item)

    def move_gp(self, command: str, x: float, y: float, z: float, item: Union[Sim, GameObject, None] = None):
        if self._log_movement:
            log.debug(f"move_gk({command} {x} {y} {z}) - ({item})")
        if command == '_rotate':
            position, orientation, item, routing_surface = self.move.relocate(move_or_rotate=False, camera_or_world=True, convert_deg_to_rad=True, item=item, x=x, y=y, z=z)
        elif command == '_move_rel':
            position, orientation, item, routing_surface = self.move.relocate(move_or_rotate=True, camera_or_world=True, convert_deg_to_rad=True, item=item, x=x, y=y, z=z)
        else:
            position, orientation, item, routing_surface = self.move.relocate(move_or_rotate=self.move_mode, camera_or_world=self.move_axes, convert_deg_to_rad=True, item=item, x=x, y=y, z=z)

        if command == 'go_to':
            if self._log_movement:
                log.debug(f"Sending the sim to location")
            import objects
            import objects.system
            from objects.terrain import TravelSuperInteraction
            from server.pick_info import PickType
            from server_commands.sim_commands import _build_terrain_interaction_target_and_context, CommandTuning

            sim_info = CommonSimUtils.get_active_sim_info()
            CommonCameraUtils.start_focus_on_sim(sim_info, follow=True)
            sim = CommonSimUtils.get_active_sim()
            add_to_queue = 0
            for i in CommonSimInteractionUtils.get_queued_interactions_gen(sim_info):
                if (getattr(i, 'guid64', 0) == 14410) or (getattr(i, 'guid', 0) == 14410):  # terrain-gohere
                    add_to_queue += 1
            if add_to_queue <= 1:
                # Add interaction to queue if only one other route interaction is in queue
                position.y = services.terrain_service.terrain_object().get_routing_surface_height_at(position.x, position.z, routing_surface)
                (target, context) = _build_terrain_interaction_target_and_context(sim, position, routing_surface, PickType.PICK_TERRAIN, objects.terrain.TerrainPoint)
                sim.push_super_affordance(CommandTuning.TERRAIN_GOHERE_AFFORDANCE, target, context)
        elif command == 'cam_to':
            if self._log_movement:
                log.debug(f"Focusing the camera to location")
            CommonCameraUtils.start_focus_on_position(CommonVector3(x, y, z))
        else:
            if self._log_movement:
                log.debug(f"Moving or rotating '{item}'")
            location = sims4.math.Location(sims4.math.Transform(position, orientation), routing_surface)
            try:
                item.location = location
                item.resend_location()
            except Exception as e:
                log.info(f"Exception '{e}' occurred. Ignore it.")

        if self._log_movement:
            log.debug(f"Completed.")

    def _get_angle_to_camera(self, sim: Sim) -> float:
        angle = 0.0
        camera_position = None
        sim_position = None
        try:
            (sim_position, orientation, level, surface_id) = sim.get_location_for_save()

            camera_position = camera._camera_position
            dx = camera_position.x - sim_position.x
            dz = camera_position.z - sim_position.z
            if dz == 0:  # <=0 <=3 ?
                dz = 10
            angle = math.atan(dx / dz)
        except Exception as e:
            pass
        if self._log_movement:
            log.debug(f"𝛼={angle} 📷={camera_position}, 🤰={sim_position}")
        return angle


