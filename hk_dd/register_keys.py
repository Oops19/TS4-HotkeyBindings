#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#


import random
from typing import Union, List, Dict

from hotkey_bindings.modinfo import ModInfo
from sims4communitylib.classes.runnables.common_runnable_with_sims import CommonRunnableSimContextType
from sims4communitylib.utils.common_log_registry import CommonLogRegistry, CommonLog
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils

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
        RegisterKeys._dd_swap_spots(current_animation=True)

    @staticmethod
    def dd_swap_poses():
        RegisterKeys._dd_swap_spots(current_animation=False)

    @staticmethod
    def _dd_swap_spots(current_animation: bool = True):
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