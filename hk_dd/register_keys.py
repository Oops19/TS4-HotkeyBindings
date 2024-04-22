#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#


import random
from typing import Union, List, Dict

from deviantcore.animation_system.utils.animation_runner_utils import DCAnimationRunnerUtils
from deviousdesires.animation_customization.customization_operations.actor_position_offset_operation import DDModifyActorPositionOffsetOperation
from deviousdesires.animation_customization.dtos.customized_animation import DDCustomizedAnimation
from deviousdesires.animation_customization.persistence.dd_animation_customization_data_manager_utils import DDAnimationCustomizationDataManagerUtils
from hotkey_bindings.modinfo import ModInfo
from sims.sim_info import SimInfo
from sims4communitylib.classes.runnables.common_runnable_with_sims import CommonRunnableSimContextType
from sims4communitylib.utils.common_log_registry import CommonLogRegistry, CommonLog
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
# noinspection PyUnresolvedReferences
from sims4.math import Vector3, Quaternion, Transform, Location
from ts4lib.classes.coordinates.std_quaternion import StdQuaternion
from ts4lib.classes.coordinates.std_vector3 import StdVector3

log: CommonLog = CommonLogRegistry.get().register_log(ModInfo.get_identity(), 'RegisterKeys')
log.enable()


class RegisterKeys:
    @staticmethod
    def dd_next_pose():
        try:
            from deviantcore.animation_system.utils.animation_runner_utils import DCAnimationRunnerUtils

            sim_info = CommonSimUtils.get_active_sim_info()
            sex_instance = DCAnimationRunnerUtils().get_animation_runner(sim_info)
            if sex_instance is None:
                for sim_info in CommonSimUtils.get_sim_info_for_all_sims_generator():
                    sex_instance = DCAnimationRunnerUtils().get_animation_runner(sim_info)
                    if sex_instance:
                        break
            if sex_instance:
                log.debug(f'Progressing animation for sim {sim_info}.')
                sex_instance.advance_animation(is_manual_change=True)
            else:
                log.debug(f"No running animations found.")
        except Exception as e:
            log.error(f"Error {e}")

    @staticmethod
    def dd_orgasm_all_sims():
        RegisterKeys.dd_happy_other_sims()
        RegisterKeys.dd_happy_active_sim()

    @staticmethod
    def dd_happy_active_sim():
        RegisterKeys._dd_orgasm(active_sim=True)

    @staticmethod
    def dd_happy_other_sims():
        RegisterKeys._dd_orgasm(active_sim=False)

    @staticmethod
    def _dd_orgasm(active_sim: bool = True):
        try:
            from deviousdesires.sex.sex_animation_interactions.utils.sex_runner_utils import DDSexRunnerUtils
            from deviantcore.classes.components.enums.sim_component_type import DCRunnableSimComponentType

            sim_info = CommonSimUtils.get_active_sim_info()
            animation_runner = DDSexRunnerUtils().get_sex_animation_runner(sim_info)

            if animation_runner is None:
                log.debug(f'No animation runner found for active sim {sim_info}.')
                return
            if animation_runner.context.is_solo:
                active_sim = True
            if active_sim:
                target_sim_context = animation_runner.context.get_sim_context(sim_info)
                if target_sim_context is None:
                    log.debug(f'No Sim Context found for {sim_info}.')
                    return
                log.debug(f'Setting orgasm_level to 99 for sim {sim_info}.')
                target_sim_context.get_component(DCRunnableSimComponentType.ORGASM).orgasm_level = 99
            else:
                for target_sim_context in animation_runner.context.get_other_sim_contexts_gen(sim_info):
                    if target_sim_context is None:
                        log.debug(f'No Sim Context found for {sim_info}.')
                        return
                    sim_info = target_sim_context.sim_info
                    log.debug(f'Setting orgasm_level to 99 for sim {sim_info}.')
                    target_sim_context.get_component(DCRunnableSimComponentType.ORGASM).orgasm_level = 99
        except Exception as e:
            log.error(f"Error {e}")

    @staticmethod
    def dd_swap_spots():
        RegisterKeys._dd_swap_spots(current_animation=True, current_actor=True)

    @staticmethod
    def dd_swap_other_spots():
        RegisterKeys._dd_swap_spots(current_animation=True, current_actor=False)

    @staticmethod
    def dd_swap_poses():
        RegisterKeys._dd_swap_spots(current_animation=False, current_actor=True)

    @staticmethod
    def dd_swap_other_poses():
        RegisterKeys._dd_swap_spots(current_animation=False, current_actor=False)

    @staticmethod
    def _dd_swap_spots(current_animation: bool = True, current_actor:bool = True):
        log.debug(f"_dd_swap_spots(current_animation={current_animation})")
        from deviantcore.animation_system.runnables.animation_runner import DCAnimationRunner
        from deviantcore.animation_system.runnables.animation_runner_registry import DCAnimationRunnerRegistry
        from deviantcore.animation_system.runnables.contexts.animation_actor_context import DCAnimationActorContext
        from deviantcore.animation_system.runnables.animation_runner_stop_reason import DCAnimationRunnerStopReason
        from deviantcore.animation_system.utils.animation_runner_utils import DCAnimationRunnerUtils
        from deviousdesires.sex.utils.swap_utils import DDSwapUtils
        animation_utils = DCAnimationRunnerUtils()
        swap_utils = DDSwapUtils()

        sim_info = CommonSimUtils.get_active_sim_info()
        sex_instance = animation_utils.get_animation_runner(sim_info)
        if sex_instance is None:
            return
        if sex_instance.context.is_solo:
            return
        if current_actor is False:
            # Replace sim_info whe a random other sim
            actor_contexts: List[DCAnimationActorContext] = list(sex_instance.context.animation_context.actor_contexts)
            random.shuffle(actor_contexts)
            for actor_context in actor_contexts:
                if sim_info != actor_context.assigned_context.sim_info:
                    sim_info = actor_context.assigned_context.sim_info
                    break
        if current_animation:
            if sex_instance.context.is_duo:
                log.debug(f"DUO")
                swap_utils.swap_spots(sim_info)
                return
            log.debug(f"3+")
            # Figure out a spot to use
            actor_context_active_sim: Union[DCAnimationActorContext, None] = None
            actor_contexts: List[DCAnimationActorContext] = list(sex_instance.context.animation_context.actor_contexts)
            random.shuffle(actor_contexts)
            for actor_context in actor_contexts:
                if sim_info == actor_context.assigned_context.sim_info:
                    actor_context_active_sim = actor_context
                    break
            log.debug(f"Active sim '{sim_info}' found.")
            if not actor_context_active_sim:
                return
            sexual_organs_active_sim = list(getattr(actor_context_active_sim, 'sexual_organs', tuple()))
            sexual_organs_active_sim.sort()
            actor_context_fallback: Union[DCAnimationActorContext, None] = None
            for actor_context in actor_contexts:
                if actor_context == actor_context_active_sim:
                    continue
                if swap_utils.is_compatible_actor(actor_context_active_sim, actor_context):
                    sexual_organs = list(getattr(actor_context, 'sexual_organs', tuple()))
                    sexual_organs.sort()
                    if sexual_organs_active_sim == sexual_organs:
                        log.debug(f"Swapping {sim_info} <--> {actor_context.assigned_context.sim_info}")
                        swap_utils._swap_sims(sex_instance, actor_context_active_sim, actor_context)
                        return
                    else:
                        actor_context_fallback = actor_context
                else:
                    log.debug(f"Skipping {actor_context.assigned_context.sim_info}")

            if actor_context_fallback:
                log.debug(f"Swapping {sim_info} <--> {actor_context_fallback.assigned_context.sim_info} (fallback)")
                swap_utils._swap_sims(sex_instance, actor_context_active_sim, actor_context_fallback)
                return
        else:
            # Search a 2nd animation
            actor_context_active_sim: Union[DCAnimationActorContext, None] = None
            animation_runners: Dict[str, DCAnimationRunner] = DCAnimationRunnerRegistry().registered_animation_runners
            i = 0
            main_animation_runner = -1
            for _, dc_animation_runner in animation_runners.items():
                dc_animation_runner: DCAnimationRunner = dc_animation_runner
                sim_contexts: List[CommonRunnableSimContextType] = dc_animation_runner.sim_contexts
                for sim_context in sim_contexts:
                    if sim_context.sim_info == sim_info:
                        main_animation_runner = i
                        actor_contexts = dc_animation_runner.context.animation_context.actor_contexts
                        for actor_context in actor_contexts:
                            if sim_info == actor_context.assigned_context.sim_info:
                                actor_context_active_sim = actor_context
                                break
                i += 1

            log.debug(f"Active sim '{actor_context_active_sim}' found.")
            sexual_organs_active_sim = list(getattr(actor_context_active_sim, 'sexual_organs', tuple()))
            sexual_organs_active_sim.sort()
            actor_context_fallback: Union[DCAnimationActorContext, None] = None
            i = 0
            for _, dc_animation_runner in animation_runners.items():
                if i == main_animation_runner:
                    continue
                log.debug(f"Processing animation {i}")
                i += 1
                actor_contexts: List[DCAnimationActorContext] = list(dc_animation_runner.context.animation_context.actor_contexts)
                random.shuffle(actor_contexts)
                for actor_context in actor_contexts:
                    if swap_utils.is_compatible_actor(actor_context_active_sim, actor_context):
                        sexual_organs = list(getattr(actor_context, 'sexual_organs', tuple()))
                        sexual_organs.sort()
                        if sexual_organs_active_sim == sexual_organs:
                            log.debug(f"Swapping {sim_info} <--> {actor_context.assigned_context.sim_info}")
                            # swap_utils._swap_sims(sex_instance, actor_context_active_sim, actor_context)
                            # dc_animation_runner.restart(DCAnimationRunnerStopReason.SIM_POSITION_SWAP)
                            temp_actor_context = actor_context_active_sim
                            actor_context_active_sim = actor_context
                            actor_context = temp_actor_context
                            sex_instance.restart(DCAnimationRunnerStopReason.SIM_POSITION_SWAP)
                            dc_animation_runner.restart(DCAnimationRunnerStopReason.SIM_POSITION_SWAP)
                            return
                        else:
                            actor_context_fallback = actor_context

                if actor_context_fallback:
                    log.debug(f"Swapping {sim_info} <--> {actor_context_fallback.assigned_context.sim_info} (fallback)")
                    # swap_utils._swap_sims(sex_instance, actor_context_active_sim, actor_context_fallback)
                    # dc_animation_runner.restart(DCAnimationRunnerStopReason.SIM_POSITION_SWAP)
                    temp_actor_context = actor_context_active_sim
                    actor_context_active_sim = actor_context_fallback
                    actor_context = temp_actor_context
                    sex_instance.restart(DCAnimationRunnerStopReason.SIM_POSITION_SWAP)
                    dc_animation_runner.restart(DCAnimationRunnerStopReason.SIM_POSITION_SWAP)
                    return

    r'''
    TODO
    @staticmethod
    def dd_clear_actor_position(sim_info: SimInfo = None):
        if sim_info is None:
            sim_info = CommonSimUtils.get_active_sim_info()
    '''

    @staticmethod
    def dd_save_actor_position(sim_info: SimInfo = None):
        if sim_info is None:
            sim_info = CommonSimUtils.get_active_sim_info()

        animation_instance = DCAnimationRunnerUtils().get_animation_runner(sim_info)
        _animation_data_manager_utils = DDAnimationCustomizationDataManagerUtils()
        animation_with_object = animation_instance.context.object_context
        if not animation_with_object:
            log.warn(f"Empty / Invisible object needed to get the animation position and orientation")
            return

        object_position: Vector3 = animation_with_object.location.transform.translation
        object_orientation: Quaternion = animation_with_object.location.transform.orientation
        object_v = StdVector3(object_position.x, object_position.y, object_position.z)
        object_q = StdQuaternion(object_orientation.w, object_orientation.x, object_orientation.y, object_orientation.z)

        sim = CommonSimUtils.get_sim_instance(sim_info)
        sim_position: Vector3 = sim._location.transform.translation
        sim_orientation: Quaternion = sim._location.transform.orientation
        sim_v = StdVector3(sim_position.x, sim_position.y, sim_position.z)
        sim_q = StdQuaternion(sim_orientation.w, sim_orientation.x, sim_orientation.y, sim_orientation.z)

        r""" The optional data  """
        # Gather all needed location data
        import services
        lot = services.active_lot()
        lot_position: Vector3 = lot.position
        lot_orientation: Quaternion = lot.orientation
        lot_v = StdVector3(lot_position.x, lot_position.y, lot_position.z)
        lot_q = StdQuaternion(sim_orientation.w, lot_orientation.x, lot_orientation.y, lot_orientation.z)

        log.debug(f"On-Save LOT {lot_v} {lot_q}")
        log.debug(f"On-Save OBJ {object_v} {object_q}")
        log.debug(f"On-Save SIM {sim_v} {sim_q}")

        ''' On-SAVE '''
        ''' Calculate the position of the sim relative to the animation position '''
        sim_position_offset_v = sim_v - object_v
        conjugated_object_q = object_q.conjugate()
        rotated_v: StdVector3 = conjugated_object_q.rotate_vector(sim_position_offset_v)
        log.debug(f"SRC sim positions {sim_position_offset_v} >> {rotated_v}")
        sim_position_offset_without_object_and_lot_orientations = rotated_v.as_ts4_vector3()

        ''' Calculate sim rotation with rotated lot and object to sim rotation in 1000 space '''
        rotated_q = conjugated_object_q.multiply(sim_q)
        sim_orientation_without_object_and_lot_orientation = rotated_q.as_ts4_quaternion()

        default_file_name = _animation_data_manager_utils.data_manager.get_default_file_name()
        animation_data_store = _animation_data_manager_utils.get_animation_customization_data_store(file_name=default_file_name)
        actor = animation_instance.context.animation_context.locate_actor_context_by_assigned_sim(sim_info)
        animation = animation_instance.context.animation_context.animation
        customized_animation = animation_data_store.get_animation(animation, default_value=DDCustomizedAnimation.from_object(animation))
        operation_to_add = DDModifyActorPositionOffsetOperation(
            actor.actor_id,
            sim_position_offset_without_object_and_lot_orientations,
            sim_orientation_without_object_and_lot_orientation,
        )
        customized_animation.add_operation(operation_to_add)
        existing_operation = customized_animation.find_existing_operation(operation_to_add)
        if existing_operation is not None:
            existing_operation.apply(animation)
        else:
            operation_to_add.apply(animation)
        animation_data_store.set_animation(customized_animation, animation)
        _animation_data_manager_utils.set_data_store(animation_data_store)
        _animation_data_manager_utils.save()
