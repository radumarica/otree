from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class InstructionPage(Page):

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'name': Constants.name_in_url
        }


class ContributeFirst(Page):
    template_name = 'PGG4/Contribute.html'
    form_model = 'player'
    form_fields = ['contribution']

    def is_displayed(self):
        if self.session.config['Manager_As_First_Contributor'] is True:
            return self.player.role() == 'Manager'
        else:
            return self.player.role() == 'Worker'

    def before_next_page(self):
        self.player.set_fairly_distributed_amount()

    def vars_for_template(self):
        return {
            'col_num': Constants.num_rounds + 1,
            'show_all_manager_data': self.session.config['Manager_As_First_Contributor'],
            'Player_for_all_rounds': self.player.in_rounds(1, Constants.num_rounds),
        }


class ContributeSecond(Page):
    template_name = 'PGG4/Contribute.html'
    form_model = 'player'
    form_fields = ['contribution']

    def is_displayed(self):
        if self.session.config['Manager_As_First_Contributor'] is True:
            return self.player.role() == 'Worker'
        else:
            return self.player.role() == 'Manager'

    def before_next_page(self):
        self.player.set_fairly_distributed_amount()

    def vars_for_template(self):
        return {
            'col_num': Constants.num_rounds + 1,
            'round_num': self.round_number,
            'show_all_manager_data': self.session.config['Manager_As_First_Contributor'],
            'Player_for_all_rounds': self.player.in_rounds(1, Constants.num_rounds),
        }


class Management(Page):
    form_model = 'group'

    def get_form_fields(self):
        return ['PR_amount_{}'.format(i) for i in range(1, Constants.players_per_group + 1)]

    def error_message(self, values):
        payouts = self.get_payout_values(values)
        if sum(payouts) != 0:
            return 'You have to equal out the punishment and reward amount'

    def is_displayed(self):
        return self.player.role() == 'Manager'

    def get_payout_values(self, values):
        payouts = []
        for i in range(1, Constants.players_per_group + 1):
            if values['PR_amount_{}'.format(i)]:
                payouts.append(values['PR_amount_{}'.format(i)])

        return payouts

    def vars_for_template(self):
        return {
            'col_num': Constants.num_rounds + 1,
            'round_num': self.round_number,
            'value': ['punishment_reward_for_player{}'.format(i) for i in range(1, Constants.players_per_group + 1)],
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
            'average_payoff': self.player.average_player_payoff
        }


page_sequence = [
    #InstructionPage,
    ContributeFirst,
    WaitForContribution,
    ContributeSecond,
    FirstWaitPage,
    Management,
    ResultsWaitPage, #Need new waitpage
    Results
]
