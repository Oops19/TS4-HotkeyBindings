#
# LICENSE None / You are allowed to use this mod in TS4
# © 2024 https://github.com/Oops19
#


from typing import Dict, Set

import services
from sims.sim_info import SimInfo
from sims4communitylib.enums.common_age import CommonAge
from sims4communitylib.services.sim.cas.common_sim_outfit_io import CommonSimOutfitIO
from sims4communitylib.utils.cas.common_outfit_utils import CommonOutfitUtils
from sims4communitylib.utils.sims.common_age_utils import CommonAgeUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils
from socials.group import SocialGroup
from sims.outfits.outfit_enums import OutfitCategory, BodyType
from ts4lib.utils.singleton import Singleton

try:
    from deviantcore.cas_part_system.enums.part_layer import DCPartLayer
    from deviousdesires.nudity_system.utils.nudity_system_utils import DDNuditySystemUtils
except:
    pass

from hotkey_bindings.modinfo import ModInfo
from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry

log: CommonLog = CommonLogRegistry.get().register_log(ModInfo.get_identity(), 'Undress')
log.enable()


class Undress(object, metaclass=Singleton):
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
            Undress.use_outfit_modifiers = True
        except:
            Undress.use_outfit_modifiers = False

        log.debug(f"Undress.use_outfit_modifiers = {Undress.use_outfit_modifiers}")

    @staticmethod
    def undress_me():
        sim_info = CommonSimUtils.get_active_sim_info()
        log.debug(f"undress_me {sim_info}")
        Undress._undress_sim(sim_info)

    @staticmethod
    def undress_you():
        Undress._undress_others(max_sims=1)

    @staticmethod
    def undress_social_group():
        Undress._undress_others(max_sims=2 ** 16)

    @staticmethod
    def undress_all():
        Undress.undress_me()
        Undress.undress_social_group()

    @staticmethod
    def undress_club():
        Undress._undress_club()

    @staticmethod
    def _undress_sim(sim_info: SimInfo):
        if Undress.use_outfit_modifiers is True:
            Undress._undress_sim_dd(sim_info)
        else:
            Undress._undress_sim_vanilla(sim_info)

    @staticmethod
    def _undress_sim_dd(sim_info):
        def update_outfit(_sim_info: SimInfo):
            # TS4 applies the outfit without outfit modifiers, so it makes no sense.
            # _sim_info.set_outfit_dirty(current_outfit_cat_and_idx)
            # _sim_info.set_current_outfit(current_outfit_cat_and_idx)
            return

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
        for body_part_id in Undress.order:
            if body_part_id not in current_body_parts:
                missing_parts.append(body_part_id)
                continue  # process only existing body parts
            part_handle = DDNuditySystemUtils().get_equipment_part_handle_by_body_location(body_part_id)
            if part_handle:
                if part_handle.is_part_set(sim_info, DCPartLayer.NUDE):
                    skipped_parts.append(body_part_id)
                    continue
                log.debug(f"_undress_sim_dd {sim_info}: {body_part_id} (skipped: {skipped_parts}, missed: {missing_parts})")

                if body_part_id == BodyType.FULL_BODY:
                    if part_handle.is_part_set(sim_info, DCPartLayer.OUTERWEAR):
                        DDNuditySystemUtils().set_equipment_part_to_layer_by_body_location(sim_info, BodyType.FULL_BODY, DCPartLayer.UNDERWEAR)
                        DDNuditySystemUtils().set_equipment_part_to_layer_by_body_location(sim_info, BodyType.UPPER_BODY, DCPartLayer.UNDERWEAR)
                        DDNuditySystemUtils().set_equipment_part_to_layer_by_body_location(sim_info, BodyType.LOWER_BODY, DCPartLayer.UNDERWEAR)
                        update_outfit(sim_info)
                        return
                    else:
                        DDNuditySystemUtils().set_equipment_part_to_layer_by_body_location(sim_info, BodyType.FULL_BODY, DCPartLayer.UNDERWEAR)
                        DDNuditySystemUtils().set_equipment_part_to_layer_by_body_location(sim_info, BodyType.UPPER_BODY, DCPartLayer.NUDE)
                        DDNuditySystemUtils().set_equipment_part_to_layer_by_body_location(sim_info, BodyType.LOWER_BODY, DCPartLayer.NUDE)
                        update_outfit(sim_info)
                        return

                elif body_part_id == BodyType.UPPER_BODY:
                    if part_handle.is_part_set(sim_info, DCPartLayer.OUTERWEAR):
                        DDNuditySystemUtils().set_equipment_part_to_layer_by_body_location(sim_info, BodyType.UPPER_BODY, DCPartLayer.UNDERWEAR)
                        update_outfit(sim_info)
                        return
                    else:
                        # sim wears top underwear
                        _part_handle_l = DDNuditySystemUtils().get_equipment_part_handle_by_body_location(BodyType.LOWER_BODY)
                        if _part_handle_l.is_part_set(sim_info, DCPartLayer.OUTERWEAR):
                            # sim wears top underwear and bottom outerwear >> change bottom to underwear
                            DDNuditySystemUtils().set_equipment_part_to_layer_by_body_location(sim_info, BodyType.LOWER_BODY, DCPartLayer.UNDERWEAR)
                            update_outfit(sim_info)
                            return
                        # else: sim wears top and bottom underwear, undress top normally

                DDNuditySystemUtils().set_equipment_part_to_layer_by_body_location(sim_info, body_part_id, DCPartLayer.NUDE)
                update_outfit(sim_info)
                return
            log.debug(f"_undress_sim_dd {sim_info}: {body_part_id} (skipped: {skipped_parts}, missed: {missing_parts}) - Nothing left to undress")

    @staticmethod
    def _undress_sim_vanilla(sim_info: SimInfo):

        def update_outfit(_sim_info: SimInfo, parts: Dict):
            log.debug(f"Changing to {parts}")
            sim_outfit_io = CommonSimOutfitIO(_sim_info, outfit_category_and_index=Undress.outfit_cat_and_idx_special0,
                                              initial_outfit_parts=parts, mod_identity=ModInfo.get_identity())
            sim_outfit_io.apply(apply_to_outfit_category_and_index=Undress.outfit_cat_and_idx_special0)
            _sim_info.set_outfit_dirty(Undress.outfit_cat_special)
            _sim_info.set_current_outfit(Undress.outfit_cat_and_idx_special0)

        if CommonAgeUtils.is_baby(sim_info):
            log.warn(f"Babies can't undress.")
            return
        if (CommonSpeciesUtils.is_pet(sim_info) or CommonSpeciesUtils.is_animal(sim_info)
                or CommonSpeciesUtils.is_cat(sim_info) or CommonSpeciesUtils.is_dog(sim_info)
                or CommonSpeciesUtils.is_horse(sim_info)):
            log.warn(f"Pets can't undress.")
            return

        log.debug(f"undress_sim {sim_info}")
        if not sim_info.has_outfit_category(Undress.outfit_cat_bathing):
            log.debug(f"Generating bathing outfit")
            sim_info.generate_outfit(Undress.outfit_cat_bathing)
        if not sim_info.has_outfit_category(Undress.outfit_cat_special):
            log.debug(f"Generating special outfit")
            sim_info.generate_outfit(Undress.outfit_cat_special)

        # gather the current and the bathing body parts
        current_outfit_cat_and_idx = CommonOutfitUtils.get_current_outfit(sim_info)
        current_body_parts = CommonOutfitUtils.get_outfit_parts(sim_info, current_outfit_cat_and_idx)
        bathing_body_parts = CommonOutfitUtils.get_outfit_parts(sim_info, (OutfitCategory.BATHING, 0))
        log.debug(f"Current outfit: {current_body_parts}")
        log.debug(f"Bathing outfit: {bathing_body_parts}")
        # if current_outfit_cat_and_idx != Undress.outfit_cat_and_idx_special0:
        #     log.debug(f"Changing from {current_outfit_cat_and_idx} to {Undress.outfit_cat_and_idx_special0}.")
        #     update_outfit(sim_info, current_body_parts)  # Switch to Special.0
        current_body_part_ids = sorted(current_body_parts.keys())
        bathing_body_part_ids = sorted(bathing_body_parts.keys())
        for body_part_id in Undress.order:
            if body_part_id in current_body_part_ids:
                # undress it
                if body_part_id not in bathing_body_part_ids:
                    del current_body_parts[body_part_id]
                    if body_part_id == BodyType.FULL_BODY:
                        # Bathing outfit are two parts
                        current_body_parts.update({BodyType.LOWER_BODY: bathing_body_parts.get(BodyType.LOWER_BODY)})
                        current_body_parts.update({BodyType.UPPER_BODY: bathing_body_parts.get(BodyType.UPPER_BODY)})
                    elif body_part_id == BodyType.UPPER_BODY:
                        # Bathing outfit is one part
                        del current_body_parts[BodyType.LOWER_BODY]
                        current_body_parts.update({BodyType.FULL_BODY: bathing_body_parts.get(BodyType.FULL_BODY)})
                    update_outfit(sim_info, current_body_parts)
                    return
                else:
                    current_body_part = current_body_parts.get(body_part_id)
                    bathing_body_part = bathing_body_parts.get(body_part_id)
                    if current_body_part != bathing_body_part:
                        current_body_parts.update({body_part_id: bathing_body_part})
                        update_outfit(sim_info, current_body_parts)
                        return

    @staticmethod
    def _undress_others(max_sims: int = 1):
        self_sim_id = CommonSimUtils.get_active_sim_id()
        self_sim = CommonSimUtils.get_active_sim()
        log.debug(f"_undress_others {self_sim}")
        sim_ids = set()
        for group in self_sim.get_groups_for_sim_gen():
            log.debug(f"\t_undress_others group {group}")
            group: SocialGroup = group

            for sim_id in group.member_sim_ids_gen():
                log.debug(f"\t\t_undress_others sim_id {sim_id}")
                if sim_id != self_sim_id:
                    sim_ids.add(sim_id)

        log.debug(f"_undress_others sim_ids {sim_ids}")
        if (len(sim_ids) == 0) or (len(sim_ids) > max_sims):
            if max_sims == 1:
                log.warn(f"Found {len(sim_ids)} sims for a sim-to-sim interaction!")
            else:
                log.warn(f"Found {len(sim_ids)} sims for a sim-to--group(max={max_sims}) interaction!")
            return

        self_sim_info = CommonSimUtils.get_active_sim_info()
        self_sim_age = CommonAgeUtils.get_age(self_sim_info, exact_age=True)
        for sim_id in sim_ids:
            sim_info = CommonSimUtils.get_sim_info(sim_id)
            c = CommonAgeUtils
            log.debug(f"undress_you {c.get_age(self_sim_info, exact_age=True)} => {c.get_age(sim_info, exact_age=True)}")
            if ((c.is_infant(sim_info) or c.is_toddler(sim_info))
                    and (c.is_infant(self_sim_info) or c.is_toddler(self_sim_info))):
                Undress._undress_sim(sim_info)
            elif (c.is_toddler(sim_info) or c.is_child(sim_info)
                    or c.is_toddler(self_sim_info) or c.is_child(self_sim_info)):
                Undress._undress_sim(sim_info)
            elif c.is_teen(sim_info) and c.is_teen(self_sim_info):
                Undress._undress_sim(sim_info)
            elif ((c.is_young_adult(sim_info) or c.is_adult(sim_info) or c.is_elder(sim_info)) and
                    (c.is_young_adult(self_sim_info) or c.is_adult(self_sim_info) or c.is_elder(self_sim_info))):
                Undress._undress_sim(sim_info)

            # As child-child interactions are allowed we allow also
            # Child-Teen and Teen-YoungAdult as long as the age difference it not too big.
            # So celebrating a birthday will not break those interactions for the involved sims.
            # youngChild + oldTeen is not supported.
            # youngTeen + oldYoungAdult is not supported.
            elif c.is_teen(sim_info) or c.is_teen(self_sim_info):
                sim_age = CommonAgeUtils.get_age(sim_info, exact_age=True)
                if c.is_teen(sim_info):
                    if c.is_child(self_sim_info):
                        if abs(sim_age - self_sim_age) < int(CommonAge.CHILD):
                            Undress._undress_sim(sim_info)
                    else:
                        if abs(sim_age - self_sim_age) < int(CommonAge.TEEN):
                            Undress._undress_sim(sim_info)
                else:
                    if c.is_child(sim_info):
                        if abs(sim_age - self_sim_age) < int(CommonAge.CHILD):
                            Undress._undress_sim(sim_info)
                    else:
                        if abs(sim_age - self_sim_age) < int(CommonAge.TEEN):
                            Undress._undress_sim(sim_info)
            else:
                log.debug(f"undress_you {c.get_age(self_sim_info, exact_age=True)} => {c.get_age(sim_info, exact_age=True)} - checks failed!")

    @staticmethod
    def _undress_club():
        log.debug(f"club undress")
        club_service = services.get_club_service()
        clubs = club_service.clubs
        c = CommonAgeUtils
        for club in clubs:
            try:
                club_gathering = club_service.clubs_to_gatherings_map.get(club)
                log.debug(f"'{club.leader}' - '{club._name}'/'{club._description}' ({club.club_id}) - private={club.invite_only} - active='{club_gathering}'")
                if club_gathering is None:
                    continue
                do_undress = True
                for sim_info in club.members:
                    if c.is_infant(sim_info) or c.is_toddler(sim_info) or c.is_child(sim_info):
                        do_undress = False
                        log.info(f"Skipping club '{club._name}' with '{c.get_age(sim_info)}' member '{sim_info}'.")
                        break
                if do_undress:
                    for sim_info in club.members:
                        Undress._undress_sim(sim_info)
            except Exception as e:
                log.error(f"Error: {e}")


Undress()
