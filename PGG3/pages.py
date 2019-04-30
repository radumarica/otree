from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class InstructionPage(Page):

    def is_displayed(self):
        return self.round_number == 1


class ContributeFirst(Page):
    template_name = 'PGG3/Contribute.html'
    form_model = 'player'
    form_fields = ['contribution']

    def is_displayed(self):
        if self.session.config['Manager_As_First_Contributor'] is True:
            return self.player.role() == 'Manager'
        else:
            return self.player.role() == 'Worker'

    def vars_for_template(self):
        return {
            'round_num': self.round_number,
            'show_all_manager_data': self.session.config['Manager_As_First_Contributor'],
            'Player_for_all_rounds': self.player.in_rounds(1, Constants.num_rounds),
        }


class ContributeSecond(Page):
    template_name = 'PGG3/Contribute.html'
    form_model = 'player'
    form_fields = ['contribution']

    def is_displayed(self):
        if self.session.config['Manager_As_First_Contributor'] is True:
            return self.player.role() == 'Worker'
        else:
            return self.player.role() == 'Manager'

    def vars_for_template(self):
        return {
            'round_num': self.round_number,
            'show_all_manager_data': self.session.config['Manager_As_First_Contributor'],
            'Player_for_all_rounds': self.player.in_rounds(1, Constants.num_rounds),
        }


class Management(Page):
    form_model = 'group'

    def get_form_fields(self):
        return ['equally_distributed'] + ['payout_from_manager_{}'.format(i) for i in range(1, Constants.players_per_group + 1)]

    def error_message(self, values):
        payouts = self.get_payout_values(values)
        if values['equally_distributed']:
            if self.group.total_payoff - sum(payouts) >= Constants.players_per_group or self.group.total_payoff < sum(payouts):
                if self.group.total_payoff - sum(payouts) > 0:
                    return 'There are ' + str(self.group.total_payoff - sum(payouts)) + ' points left to divide'
                elif self.group.total_payoff - sum(payouts) < 0:
                    return 'You have used ' + str(sum(payouts) - self.group.total_payoff) + 'points over the given amount'
        elif sum(payouts) != self.group.total_payoff:
            if self.group.total_payoff - sum(payouts) > 0:
                return 'You have not distributed all the points'
            elif self.group.total_payoff - sum(payouts) < 0:
                return 'You have used ' + str(sum(payouts) - self.group.total_payoff) + 'points over the given amount'

    def is_displayed(self):
        return self.player.role() == 'Manager'

    def get_payout_values(self, values):
        payouts = []
        for i in range(1, Constants.players_per_group + 1):
            payouts.append(values['payout_from_manager_{}'.format(i)])

        return payouts

    def vars_for_template(self):
        return {
            'round_num': self.round_number,
            'show_all_manager_data': self.session.config['Manager_As_First_Contributor'],
            'Player_for_all_rounds': self.player.in_rounds(1, Constants.num_rounds),
        }

    def before_next_page(self):
        self.group.set_payoffs()
        if self.round_number == Constants.num_rounds:
            self.player.calculate_average_payoff()


class FirstWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_poll()

    body_text = "Waiting for other participants to contribute."


class WaitForContribution(WaitPage):

    body_text = "Waiting for other participants to contribute."


class ResultsWaitPage(WaitPage):

    body_text = "Waiting for other participants to contribute."


class Results(Page):

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        return {
            'average_payoff': self.player.average_player_payoff,
            'round_num': self.round_number,
            'show_all_manager_data': self.session.config['Manager_As_First_Contributor'],
            'Player_for_all_rounds': self.player.in_rounds(1, Constants.num_rounds),
        }


page_sequence = [
    InstructionPage,
    ContributeFirst,
    WaitForContribution,
    ContributeSecond,
    FirstWaitPage,
    Management,
    ResultsWaitPage, #Need new waitpage
    Results
]
