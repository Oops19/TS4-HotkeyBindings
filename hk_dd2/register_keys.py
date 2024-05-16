#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#



try:
    import random
    from typing import Union, List, Dict, Tuple
    from deviantcore.animation_system.runnables.animation_runner import DCAnimationRunner
    from deviantcore.animation_system.runnables.animation_runner_registry import DCAnimationRunnerRegistry
    from deviantcore.animation_system.runnables.animation_runner_stop_reason import DCAnimationRunnerStopReason
    from deviantcore.animation_system.runnables.contexts.animation_actor_context import DCAnimationActorContext
    from deviantcore.animation_system.utils.animation_runner_utils import DCAnimationRunnerUtils
    from deviousdesires.sex.utils.swap_utils import DDSwapUtils
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
    from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils
    from ts4lib.classes.coordinates.std_quaternion import StdQuaternion
    from ts4lib.classes.coordinates.std_vector3 import StdVector3

    log: CommonLog = CommonLogRegistry.get().register_log(ModInfo.get_identity(), 'RegisterKeys')
    log.enable()


    class RegisterKeys:

        @staticmethod
        def dd_next_pose():
            try:
                sim_info_swap = CommonSimUtils.get_active_sim_info()
                dc_animation_runner = DCAnimationRunnerUtils().get_animation_runner(sim_info_swap)
                if dc_animation_runner is None:
                    for sim_info_swap in CommonSimUtils.get_sim_info_for_all_sims_generator():
                        dc_animation_runner = DCAnimationRunnerUtils().get_animation_runner(sim_info_swap)
                        if dc_animation_runner:
                            break
                if dc_animation_runner:
                    log.debug(f'Progressing animation for sim {sim_info_swap}.')
                    dc_animation_runner.advance_animation(is_manual_change=True)
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

                sim_info_swap = CommonSimUtils.get_active_sim_info()
                animation_runner = DDSexRunnerUtils().get_sex_animation_runner(sim_info_swap)

                if animation_runner is None:
                    log.debug(f'No animation runner found for active sim {sim_info_swap}.')
                    return
                if animation_runner.context.is_solo:
                    active_sim = True
                if active_sim:
                    target_sim_context = animation_runner.context.get_sim_context(sim_info_swap)
                    if target_sim_context is None:
                        log.debug(f'No Sim Context found for {sim_info_swap}.')
                        return
                    log.debug(f'Setting orgasm_level to 99 for sim {sim_info_swap}.')
                    target_sim_context.get_component(DCRunnableSimComponentType.ORGASM).orgasm_level = 99
                else:
                    for target_sim_context in animation_runner.context.get_other_sim_contexts_gen(sim_info_swap):
                        if target_sim_context is None:
                            log.debug(f'No Sim Context found for {sim_info_swap}.')
                            return
                        sim_info_swap = target_sim_context.sim_info
                        log.debug(f'Setting orgasm_level to 99 for sim {sim_info_swap}.')
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
        def _get_animation_active_sim_v1(dc_animation_runner: DCAnimationRunner, current_actor: bool = True) -> Tuple[SimInfo, Union[DCAnimationActorContext, None]]:
            sim_info_swap = CommonSimUtils.get_active_sim_info()
            actor_contexts: List[DCAnimationActorContext] = list(dc_animation_runner.context.animation_context.actor_contexts)
            random.shuffle(actor_contexts)
            if current_actor:
                for actor_context in actor_contexts:
                    if sim_info_swap == actor_context.assigned_context.sim_info:
                        return sim_info_swap, actor_context
            else:
                for actor_context in actor_contexts:
                    if sim_info_swap != actor_context.assigned_context.sim_info:
                        return actor_context.assigned_context.sim_info, actor_context

            return sim_info_swap, None

        @staticmethod
        def _get_animation_active_sim(dc_animation_runner: DCAnimationRunner, current_actor: bool = True) -> Tuple[int, SimInfo, Union[DCAnimationActorContext, None]]:
            sim_info = CommonSimUtils.get_active_sim_info()
            actor_contexts: Dict[int, DCAnimationActorContext] = dc_animation_runner.context.animation_context.actor_contexts_library
            actor_ids = list(actor_contexts.keys())
            log.debug(f"Sim_info {sim_info} current_actor {current_actor} ... actor_contexts {actor_contexts}")
            if current_actor is True:
                for actor_id in actor_ids:
                    actor_context = actor_contexts.get(actor_id)
                    log.debug(f"CA Sim_info {actor_id} {actor_context.assigned_context.sim_info}")
                    if sim_info == actor_context.assigned_context.sim_info:
                        log.debug(f"==> CA Sim_info {actor_id} {actor_context.assigned_context.sim_info}")
                        return actor_id, sim_info, actor_context
            else:
                random.shuffle(actor_ids)
                for actor_id in actor_ids:
                    actor_context = actor_contexts.get(actor_id)
                    log.debug(f"RND Sim_info {actor_id} {actor_context.assigned_context.sim_info}")
                    if sim_info != actor_context.assigned_context.sim_info:
                        log.debug(f"==> RND Sim_info {actor_id} {actor_context.assigned_context.sim_info}")
                        return actor_id, sim_info, actor_context

            log.debug(f"==> ---")
            return -1, sim_info, None

        @staticmethod
        def _dd_swap_spots(current_animation: bool = True, current_actor: bool = True):
            log.debug(f"_dd_swap_spots(current_animation={current_animation}, current_actor={current_actor})")

            animation_utils = DCAnimationRunnerUtils()
            swap_utils = DDSwapUtils()

            dc_animation_runner = animation_utils.get_animation_runner(CommonSimUtils.get_active_sim_info())
            if dc_animation_runner is None or dc_animation_runner.context.is_solo:
                return

            if current_actor is False:
                actor_id_exclude, sim_info_exclude, actor_context_exclude = RegisterKeys()._get_animation_active_sim(dc_animation_runner, current_actor=True)
            else:
                actor_id_exclude, sim_info_exclude, actor_context_exclude = -1, None, None

            actor_id_swap, sim_info_swap, actor_context_swap = RegisterKeys()._get_animation_active_sim(dc_animation_runner, current_actor)
            actor_contexts_library_swap: Dict[int, DCAnimationActorContext] = dc_animation_runner.context.animation_context.actor_contexts_library
            if not actor_context_swap:
                return
            sexual_organs_swap_sim = list(getattr(actor_context_swap, 'sexual_organs', tuple()))
            # sexual_organs_swap_sim = [so.value for so in getattr(actor_context_swap, 'sexual_organs', tuple())]
            sexual_organs_swap_sim.sort()

            if current_animation:
                if dc_animation_runner.context.is_duo:
                    log.debug(f"DUO")
                    swap_utils.swap_spots(sim_info_swap)
                    return

                # Figure out a spot to use
                log.debug(f"Sim to swap {sim_info_swap} [{CommonSpeciesUtils.get_species(sim_info_swap)} {sexual_organs_swap_sim}], 3+")
                # Figure out a spot to use
                actor_context_fallback: Union[DCAnimationActorContext, None] = None
                actor_contexts: List[DCAnimationActorContext] = list(dc_animation_runner.context.animation_context.actor_contexts)
                random.shuffle(actor_contexts)
                for actor_context in actor_contexts:
                    if (actor_context == actor_context_swap) or (actor_context == actor_context_exclude):
                        continue
                    sim_info_swap_pair = actor_context.assigned_context.sim_info
                    sexual_organs_swap_pair = list(getattr(actor_context, 'sexual_organs', tuple()))
                    # sexual_organs_swap_pair = [so.value for so in getattr(actor_context, 'sexual_organs', tuple())]
                    sexual_organs_swap_pair.sort()
                    log.debug(f"Checking {sim_info_swap_pair} [{CommonSpeciesUtils.get_species(sim_info_swap_pair)} {sexual_organs_swap_pair}]")
                    if CommonSpeciesUtils.are_same_species(sim_info_swap, sim_info_swap_pair):
                        if sexual_organs_swap_sim == sexual_organs_swap_pair:
                            log.debug(f"Swapping {sim_info_swap} <--> {sim_info_swap_pair}")
                            swap_utils._swap_sims(dc_animation_runner, actor_context_swap, actor_context)
                            return
                        else:
                            log.debug(f"Fallback {sim_info_swap_pair}")
                            actor_context_fallback = actor_context
                    else:
                        log.debug(f"Skipping {sim_info_swap_pair}")

                if actor_context_fallback:
                    log.debug(f"Swapping {sim_info_swap} <--> {actor_context_fallback.assigned_context.sim_info} (fallback)")
                    swap_utils._swap_sims(dc_animation_runner, actor_context_swap, actor_context_fallback)
                    return
            else:
                try:
                    # Search a 2nd animation
                    # actor_context_swap_a2: Union[DCAnimationActorContext, None] = None
                    animation_runners: Dict[str, DCAnimationRunner] = DCAnimationRunnerRegistry().registered_animation_runners
                    if len(animation_runners) == 1:
                        log.debug(f"Found only one animation.")
                        return
                    main_animation_runner = 0
                    i = -1
                    for _, dc_animation_runner_2 in animation_runners.items():
                        i += 1
                        dc_animation_runner_2: DCAnimationRunner = dc_animation_runner_2
                        sim_contexts: List[CommonRunnableSimContextType] = dc_animation_runner_2.sim_contexts
                        for sim_context in sim_contexts:
                            if sim_context.sim_info == sim_info_swap:
                                main_animation_runner = i
                                log.debug(f"Main animation ID: {i}")
                                break

                    log.debug(f"Sim to swap {sim_info_swap} [{CommonSpeciesUtils.get_species(sim_info_swap)} {sexual_organs_swap_sim}], 3+")
                    actor_context_fallback: Union[DCAnimationActorContext, None] = None
                    i = -1
                    for _, dc_animation_runner_2 in animation_runners.items():
                        i += 1
                        if i == main_animation_runner:
                            continue
                        log.debug(f"Processing animation: {i}")
                        actor_contexts_library_swap_pair: Dict[int, DCAnimationActorContext] = dc_animation_runner_2.context.animation_context.actor_contexts_library
                        actor_ids = list(actor_contexts_library_swap_pair.keys())
                        random.shuffle(actor_ids)
                        for actor_id_swap_pair in actor_ids:
                            actor_context_swap_pair = actor_contexts_library_swap_pair.get(actor_id_swap_pair)
                            sim_info_swap_pair = actor_context_swap_pair.assigned_context.sim_info
                            sexual_organs_swap_pair = list(getattr(actor_context_swap_pair, 'sexual_organs', tuple()))
                            # sexual_organs_swap_pair = [so.value for so in getattr(actor_context_swap_pair, 'sexual_organs', tuple())]
                            sexual_organs_swap_pair.sort()
                            log.debug(f"Checking {sim_info_swap_pair} [{CommonSpeciesUtils.get_species(sim_info_swap_pair)} {sexual_organs_swap_pair}]")
                            if CommonSpeciesUtils.are_same_species(sim_info_swap, sim_info_swap_pair):
                                if sexual_organs_swap_sim == sexual_organs_swap_pair:
                                    log.debug(f"Swapping {sim_info_swap} <--> {sim_info_swap_pair}")
                                    actor_contexts_library_swap_pair.update({actor_id_swap_pair: actor_context_swap})
                                    actor_contexts_library_swap.update({actor_id_swap: actor_context_swap_pair})
                                    dc_animation_runner.restart(DCAnimationRunnerStopReason.SIM_POSITION_SWAP)

                                    dc_animation_runner_2.restart(DCAnimationRunnerStopReason.SIM_POSITION_SWAP)
                                    return
                                else:
                                    log.debug(f"Fallback {sim_info_swap_pair}")
                                    actor_context_fallback = actor_context_swap
                            else:
                                log.debug(f"Skipping {sim_info_swap_pair}")

                    if actor_context_fallback:
                        log.debug(f"Swapping {sim_info_swap} <--> {actor_context_fallback.assigned_context.sim_info} (fallback)")
                        log.debug(f"Swapping {sim_info_swap} <--> {sim_info_swap_pair}")
                        actor_contexts_library_swap_pair.update({actor_id_swap_pair: actor_context_swap})
                        actor_contexts_library_swap.update({actor_id_swap: actor_context_swap_pair})
                        dc_animation_runner.restart(DCAnimationRunnerStopReason.SIM_POSITION_SWAP)
                        dc_animation_runner_2.restart(DCAnimationRunnerStopReason.SIM_POSITION_SWAP)
                        return
                    log.debug(f"Failed to locate a sim.")
                except Exception as e:
                    log.error(f"Oops {e}")

        @staticmethod
        def dd_save_actor_position(sim_info_swap: SimInfo = None):
            if sim_info_swap is None:
                sim_info_swap = CommonSimUtils.get_active_sim_info()

            animation_instance = DCAnimationRunnerUtils().get_animation_runner(sim_info_swap)
            _animation_data_manager_utils = DDAnimationCustomizationDataManagerUtils()
            animation_with_object = animation_instance.context.object_context
            if not animation_with_object:
                log.warn(f"Empty / Invisible object needed to get the animation position and orientation")
                return

            object_position: Vector3 = animation_with_object.location.transform.translation
            object_orientation: Quaternion = animation_with_object.location.transform.orientation
            object_v = StdVector3(object_position.x, object_position.y, object_position.z)
            object_q = StdQuaternion(object_orientation.w, object_orientation.x, object_orientation.y, object_orientation.z)

            sim = CommonSimUtils.get_sim_instance(sim_info_swap)
            sim_position: Vector3 = sim._location.transform.translation
            sim_orientation: Quaternion = sim._location.transform.orientation
            sim_v = StdVector3(sim_position.x, sim_position.y, sim_position.z)
            sim_q = StdQuaternion(sim_orientation.w, sim_orientation.x, sim_orientation.y, sim_orientation.z)

            r""" Debug code
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
            """

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
            actor = animation_instance.context.animation_context.locate_actor_context_by_assigned_sim(sim_info_swap)
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
except:
    class RegisterKeys:
        @staticmethod
        def dd_next_pose():
            pass

        @staticmethod
        def dd_orgasm_all_sims():
            pass

        @staticmethod
        def dd_happy_active_sim():
            pass

        @staticmethod
        def dd_happy_other_sims():
            pass

        @staticmethod
        def dd_swap_spots():
            pass

        @staticmethod
        def dd_swap_other_spots():
            pass

        @staticmethod
        def dd_swap_poses():
            pass

        @staticmethod
        def dd_swap_other_poses():
            pass

        @staticmethod
        def dd_save_actor_position():
            pass
