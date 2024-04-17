#
# LICENSE
# https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#


import services
import sims4
import sims4.commands
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CAS:

    @staticmethod
    def edit_in_cas():
        sim = CommonSimUtils.get_active_sim()
        # noinspection PyBroadException
        try:
            client_id = services.client_manager().get_first_client().id
        except:
            client_id = 1
        sims4.commands.client_cheat(f'sims.exit2caswithhouseholdid {sim.id} {sim.household_id}', client_id)
