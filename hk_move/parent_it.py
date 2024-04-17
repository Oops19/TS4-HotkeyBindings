#
# LICENSE
# https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#


from hotkey_bindings.modinfo import ModInfo
from hk_move.move import Move

from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils

from sims.sim import Sim
import sims4
import sims4.commands
import sims4.math
import sims4.hash_util
# noinspection PyUnresolvedReferences
from sims4.math import Vector3, Quaternion, Transform, Location


class ParentIt:

    @staticmethod
    @CommonConsoleCommand(ModInfo.get_identity(), 'o19.sim.p', 'ddd')
    def parent_sim_to_object(output: CommonConsoleCommandOutput):
        sim: Sim = CommonSimUtils.get_active_sim()
        obj = Move.item

        output(f"{sim} -> {obj}")
        if isinstance(obj, Sim):
            return

        bone_name = 'b__ROOT__'
        bone_hash: int = sims4.hash_util.hash32(bone_name)

        position = sims4.math.Vector3(0, 0, 0)
        orientation = sims4.math.Quaternion(0, 0, 0, 1)
        transformation = sims4.math.Transform(position, orientation)

        sim.set_parent(obj, transform=transformation, joint_name_or_hash=bone_hash)
        output(f"OK")

    @staticmethod
    @CommonConsoleCommand(ModInfo.get_identity(), 'o19.sim.up', 'ddd')
    def unparent_sim_to_object(output: CommonConsoleCommandOutput):
        sim: Sim = CommonSimUtils.get_active_sim()
        obj = Move.item

        output(f"{sim} -> {obj}")
        if isinstance(obj, Sim):
            return

        sim.remove_reference_from_parent()
        output(f"OK")


r'''
def remove_reference_from_parent(self):
    parent = self.parent
    if parent is not None:
        parent._remove_child(self, new_parent=UNSET)
        

if parent_id is None:
    parent_object = child_object.get_parenting_root()
    child_object.clear_parent(child_object.transform, parent_object.routing_surface)
'''
