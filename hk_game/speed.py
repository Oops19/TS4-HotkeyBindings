#
# LICENSE
# https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#


from sims4communitylib.utils.common_time_utils import CommonTimeUtils

from hotkey_bindings.modinfo import ModInfo
from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry

log: CommonLog = CommonLogRegistry.get().register_log(ModInfo.get_identity().base_namespace, ModInfo.get_identity().name)
log.enable()


class Speed:

    @staticmethod
    def set_to(speed: str = 1):
        # noinspection PyBroadException
        try:
            speed = f"{speed}"
            if speed == "0":
                CommonTimeUtils.pause_the_game()
            elif speed == "2":
                CommonTimeUtils.set_game_speed_to_speed_two()
            elif speed == "3":
                CommonTimeUtils.set_game_speed_to_speed_three()
            else:
                CommonTimeUtils.set_game_speed_normal()
            log.debug(f"Changed game speed.")
        except Exception as e:
            log.error(f"Setting game speed to '{speed}' failed ({e}).")
