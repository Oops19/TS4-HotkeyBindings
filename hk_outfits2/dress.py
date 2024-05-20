#
# LICENSE None / You are allowed to use this mod in TS4
# © 2024 https://github.com/Oops19
#


from sims.sim_info import SimInfo
from sims4communitylib.utils.cas.common_outfit_utils import CommonOutfitUtils
from sims4communitylib.utils.sims.common_age_utils import CommonAgeUtils

from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims.outfits.outfit_enums import OutfitCategory, BodyType
from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils
from ts4lib.utils.singleton import Singleton

try:
    from deviantcore.cas_part_system.enums.part_layer import DCPartLayer
    from deviousdesires.nudity_system.utils.nudity_system_utils import DDNuditySystemUtils
except:
    pass

from hotkey_bindings.modinfo import ModInfo
from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry

log: CommonLog = CommonLogRegistry.get().register_log(ModInfo.get_identity(), 'Dress')
log.enable()


class Dress(object, metaclass=Singleton):
    outfit_cat_special = OutfitCategory.SPECIAL
    outfit_cat_and_idx_special0 = (outfit_cat_special, 0)
    outfit_cat_bathing = OutfitCategory.BATHING
    outfit_cat_and_idx_bathing0 = (outfit_cat_bathing, 0)

    order = [BodyType.HAT, BodyType.SHOES, BodyType.SOCKS, BodyType.FULL_BODY, BodyType.CUMMERBUND, BodyType.UPPER_BODY,
             BodyType.LOWER_BODY, BodyType.GLOVES, BodyType.TIGHTS, BodyType.NECKLACE, BodyType.EARRINGS,
             BodyType.GLASSES]

    use_outfit_modifiers = None

    def __init__(self):
        # noinspection PyBroadException
        try:
            from deviantcore import modinfo
            Dress.use_outfit_modifiers = True
        except:
            Dress.use_outfit_modifiers = False
        log.debug(f"Dress.use_outfit_modifiers = {Dress.use_outfit_modifiers}")

        Dress.order.reverse()
        log.debug(f"Dress.order = {Dress.order}")

    @staticmethod
    def dress_me():
        sim_info = CommonSimUtils.get_active_sim_info()
        log.debug(f"dress_me {sim_info}")
        Dress._dress_sim(sim_info)

    @staticmethod
    def _dress_sim(sim_info: SimInfo):
        if Dress.use_outfit_modifiers is True:
            Dress._dress_sim_dd(sim_info)
        else:
            Dress._dress_sim_vanilla(sim_info)

    @staticmethod
    def _dress_sim_dd(sim_info: SimInfo):

        def update_outfit(_sim_info: SimInfo):
            _sim_info.set_outfit_dirty(current_outfit_cat_and_idx)
            _sim_info.set_current_outfit(current_outfit_cat_and_idx)

        if CommonAgeUtils.is_baby(sim_info):
            log.warn(f"Babies can't undress.")
            return
        if (CommonSpeciesUtils.is_pet(sim_info) or CommonSpeciesUtils.is_animal(sim_info)
                or CommonSpeciesUtils.is_cat(sim_info) or CommonSpeciesUtils.is_dog(sim_info)
                or CommonSpeciesUtils.is_horse(sim_info)):
            log.warn(f"Pets can't undress.")
            return

        current_outfit_cat_and_idx = CommonOutfitUtils.get_current_outfit(sim_info)
        current_body_parts = CommonOutfitUtils.get_outfit_parts(sim_info, current_outfit_cat_and_idx)

        skipped_parts = []
        missing_parts = []
        for body_part_id in Dress.order:
            if body_part_id not in current_body_parts:
                missing_parts.append(body_part_id)
                continue  # process only existing body parts
            part_handle = DDNuditySystemUtils().get_equipment_part_handle_by_body_location(body_part_id)
            if part_handle:
                if part_handle.is_part_set(sim_info, DCPartLayer.OUTERWEAR):
                    skipped_parts.append(body_part_id)
                    continue
                log.debug(f"_dress_sim_dd {sim_info}: {body_part_id} (skipped: {skipped_parts})")

                if body_part_id == BodyType.FULL_BODY:
                    if part_handle.is_part_set(sim_info, DCPartLayer.NUDE):
                        DDNuditySystemUtils().set_equipment_part_to_layer_by_body_location(sim_info, BodyType.FULL_BODY, DCPartLayer.UNDERWEAR)
                        DDNuditySystemUtils().set_equipment_part_to_layer_by_body_location(sim_info, BodyType.UPPER_BODY, DCPartLayer.UNDERWEAR)
                        DDNuditySystemUtils().set_equipment_part_to_layer_by_body_location(sim_info, BodyType.LOWER_BODY, DCPartLayer.UNDERWEAR)
                        update_outfit(sim_info)
                        return
                    else:
                        DDNuditySystemUtils().set_equipment_part_to_layer_by_body_location(sim_info, BodyType.FULL_BODY, DCPartLayer.OUTERWEAR)
                        DDNuditySystemUtils().set_equipment_part_to_layer_by_body_location(sim_info, BodyType.UPPER_BODY, DCPartLayer.OUTERWEAR)
                        DDNuditySystemUtils().set_equipment_part_to_layer_by_body_location(sim_info, BodyType.LOWER_BODY, DCPartLayer.OUTERWEAR)
                        update_outfit(sim_info)
                        return

                elif body_part_id == BodyType.LOWER_BODY:
                    if part_handle.is_part_set(sim_info, DCPartLayer.NUDE):
                        DDNuditySystemUtils().set_equipment_part_to_layer_by_body_location(sim_info, BodyType.LOWER_BODY, DCPartLayer.UNDERWEAR)
                        update_outfit(sim_info)
                        return
                    else:
                        # sim wears bottom underwear
                        _part_handle_u = DDNuditySystemUtils().get_equipment_part_handle_by_body_location(BodyType.UPPER_BODY)
                        if _part_handle_u.is_part_set(sim_info, DCPartLayer.NUDE):
                            # sim wears bottom underwear and top nude >> change top to underwear
                            DDNuditySystemUtils().set_equipment_part_to_layer_by_body_location(sim_info, BodyType.UPPER_BODY, DCPartLayer.UNDERWEAR)
                            DDNuditySystemUtils().set_equipment_part_to_layer_by_body_location(sim_info, BodyType.FULL_BODY, DCPartLayer.UNDERWEAR)
                            update_outfit(sim_info)
                            return
                        # else: sim wears top and bottom underwear, dress top normally

                DDNuditySystemUtils().set_equipment_part_to_layer_by_body_location(sim_info, body_part_id, DCPartLayer.OUTERWEAR)
                if (body_part_id == BodyType.UPPER_BODY) and (part_handle.is_part_set(sim_info, DCPartLayer.UNDERWEAR)):
                    DDNuditySystemUtils().set_equipment_part_to_layer_by_body_location(sim_info, BodyType.FULL_BODY, DCPartLayer.OUTERWEAR)
                update_outfit(sim_info)
                return
        log.debug(f"_dress_sim_dd {sim_info}: {body_part_id} (skipped: {skipped_parts}, missed: {missing_parts}) - Nothing left to dress")

    @staticmethod
    def _dress_sim_vanilla(sim_info: SimInfo):
        if CommonAgeUtils.is_baby(sim_info):
            log.warn(f"Babies can't undress.")
            return
        if (CommonSpeciesUtils.is_pet(sim_info) or CommonSpeciesUtils.is_animal(sim_info)
                or CommonSpeciesUtils.is_cat(sim_info) or CommonSpeciesUtils.is_dog(sim_info)
                or CommonSpeciesUtils.is_horse(sim_info)):
            log.warn(f"Pets can't undress.")
            return

        log.debug(f"_dress_sim_vanilla({sim_info}) not yet implemented")


Dress()
