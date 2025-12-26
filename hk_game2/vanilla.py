#
# LICENSE
# https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#


import time

import services
from hk_game2.speed import Speed
from services.persistence_service import SaveGameData
from sims4communitylib.utils.save_load.common_save_utils import CommonSaveUtils

from hotkey_bindings.modinfo import ModInfo
from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry
from ts4lib.utils.simple_ui_notification import SimpleUINotification

log: CommonLog = CommonLogRegistry.get().register_log(ModInfo.get_identity(), ModInfo.get_identity().name)
log.enable()
log.debug(f"vanilla ...")


class Vanilla:

    @staticmethod
    def quick_exit():
        # noinspection PyBroadException
        try:
            from ts4l_ctypes import windll
            PROCESS_TERMINATE = 0x0001
            FALSE = 0
            dwProcessID = windll.kernel32.GetCurrentProcessId()
            hProcess = windll.kernel32.OpenProcess(PROCESS_TERMINATE, FALSE, dwProcessID)
            if hProcess != 0:
                windll.kernel32.TerminateProcess(hProcess, -1)
                windll.kernel32.CloseHandle(hProcess)
        except Exception as e:
            log.error(f"Exit failed '{e}'")

    @staticmethod
    def quick_save():
        # noinspection PyBroadException
        try:
            send_save_message = True
            check_cooldown = True  # False -> broken paintings/photos
            t = int((86400 + time.time()) / 10_000)  # every 4 hours +1
            save_game_data = SaveGameData(CommonSaveUtils.get_save_slot_id(), 'quick', True, t)
            persistence_service = services.get_persistence_service()
            persistence_service.save_using(persistence_service.save_game_gen, save_game_data, send_save_message=send_save_message, check_cooldown=check_cooldown)
            log.debug(f"Saving game as 'Slot_{t:08x}.save'")
            SimpleUINotification().show('Saving Game', f"Saving game as 'Slot_{t:08x}.save'")
        except Exception as e:
            log.error(f"Save failed '{e}'")

    @staticmethod
    def quickie(action: str = ''):
        log.debug(f"quickie({action})")
        if 'save' in action:
            Vanilla.quick_save()
        if 'exit' in action:
            Vanilla.quick_exit()
        if 'pause' in action:
            Speed.set_to('0')
