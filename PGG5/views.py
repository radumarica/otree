from ._builtin import Page, WaitPage
from .models import Constants


class InstructionsPeers(Page):
    def is_displayed(self):
        return self.round_number == 1 and \
               self.player.role() == "peer"


class InstructionsManagers(Page):
    def is_displayed(self):
        return self.round_number == 1 and \
               self.player.role() == "manager"


class Contribution(Page):
    form_model = 'player'
    form_fields = ['contribution']


class ManagerWaitPage(WaitPage):
    def is_displayed(self):
        return self.player.role() == "manager"


class Reinforcement(Page):
    def is_displayed(self):
        return self.player.role() == "manager"

    form_model = 'group'

    def get_form_fields(self):
        player_ids = []
        for players in self.group.get_players():
            player_ids.append(players.id_in_group)
        return ['reinforcement_player_{}'.format(i) for i in player_ids]

    def vars_for_template(self):
        return {'public_good_per_player': self.group.public_good_per_player()}

    def before_next_page(self):
        self.group.calculate_total_contribution()
        self.group.fill_reinforcement_list()
        for p in self.group.get_players():
            p.calculate_payoff()


class ReinforcementWaitPage(WaitPage):
    def is_displayed(self):
        return self.player.role() == "peer"


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        pass


class Results(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        total_payoff = 0
        for r in self.player.in_all_rounds():
            total_payoff += r.payoff
        return {'total_payoff': total_payoff}


page_sequence = [

    InstructionsPeers,
    InstructionsManagers,
    Contribution,
    ManagerWaitPage,
    Reinforcement,
    ReinforcementWaitPage,
    ResultsWaitPage,
    Results

]
