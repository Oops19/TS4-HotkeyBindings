#
# LICENSE None / You are allowed to use this mod in TS4
# © 2024 https://github.com/Oops19
#


from sims.sim_info import SimInfo

from sims4communitylib.utils.sims.common_age_utils import CommonAgeUtils

from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims.outfits.outfit_enums import BodyType
from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils
from ts4lib.utils.singleton import Singleton

try:
    from deviantcore.cas_part_system.enums.part_layer import DCPartLayer
    from deviousdesires.nudity_system.utils.nudity_system_utils import DDNuditySystemUtils
except:
    pass

from hotkey_bindings.modinfo import ModInfo
from sims4communitylib.utils.common_log_registry import CommonLogRegistry, CommonLog

log: CommonLog = CommonLogRegistry.get().register_log(ModInfo.get_identity(), 'Heels')
log.enable()


class Heels(object, metaclass=Singleton):
    use_outfit_modifiers = None

    def __init__(self):
        # noinspection PyBroadException
        try:
            from deviantcore import modinfo
            Heels.use_outfit_modifiers = True
        except:
            Heels.use_outfit_modifiers = False
        log.debug(f"Heels.use_outfit_modifiers = {Heels.use_outfit_modifiers}")

    @staticmethod
    def toggle():
        sim_info = CommonSimUtils.get_active_sim_info()
        log.debug(f"toggle {sim_info}")
        Heels._toggle(sim_info)

    @staticmethod
    def _toggle(sim_info: SimInfo):
        if Heels.use_outfit_modifiers is True:
            Heels._toggle_dd(sim_info)
        else:
            # Heels._toggle_vanilla(sim_info)
            pass

    @staticmethod
    def _toggle_dd(sim_info: SimInfo):
        if CommonAgeUtils.is_baby(sim_info):
            log.warn(f"Babies can't undress.")
            return
        if (CommonSpeciesUtils.is_pet(sim_info) or CommonSpeciesUtils.is_animal(sim_info)
                or CommonSpeciesUtils.is_cat(sim_info) or CommonSpeciesUtils.is_dog(sim_info)
                or CommonSpeciesUtils.is_horse(sim_info)):
            log.warn(f"Pets can't undress.")
            return

        body_part_id = BodyType.SHOES
        part_handle = DDNuditySystemUtils().get_equipment_part_handle_by_body_location(body_part_id)
        if part_handle.is_part_set(sim_info, DCPartLayer.OUTERWEAR):
            DDNuditySystemUtils().set_equipment_part_to_layer_by_body_location(sim_info, body_part_id, DCPartLayer.NUDE)
        else:
            DDNuditySystemUtils().set_equipment_part_to_layer_by_body_location(sim_info, body_part_id, DCPartLayer.OUTERWEAR)


Heels()
