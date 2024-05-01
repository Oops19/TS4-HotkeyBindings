#
# LICENSE
# https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#


import sys
import threading
import traceback

from hotkey_bindings.modinfo import ModInfo
from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry

log: CommonLog = CommonLogRegistry.get().register_log(ModInfo.get_identity().base_namespace, ModInfo.get_identity().name)
log.enable()


class ThreadDump:

    @staticmethod
    def create():
        # noinspection PyBroadException
        try:
            log.debug(f"Thread Dump")
            for thread in threading.enumerate():
                log.debug(f"{thread}")
                thread_details = traceback.extract_stack(sys._current_frames()[thread.ident])
                for thread_detail in thread_details:
                    (filename, number, function, line_text) = thread_detail
                    log.debug(f"    {filename}#{number} '{line_text}' in '{function}()'")
            log.debug(f"")
        except:
            pass
