from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Introduction(Page):
    """Description of the game: How to play and returns expected"""

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'round_num': self.round_number,
            'experiment_name': self.session.config['experimentName']
        }


class Contribute(Page):
    """Player: Choose how much to contribute"""

    form_model = 'player'
    form_fields = ['contribution']

    timeout_submission = {'contribution': c(Constants.endowment / 2)}

    def vars_for_template(self):
        contributions = [p.contribution for p in self.player.in_all_rounds()]
        return {
            'col_num': Constants.num_rounds + 1,
            'round_num': self.round_number,
            'experiment_name': self.session.config['experimentName'],
            'Player_for_all_rounds': self.player.in_rounds(1, Constants.num_rounds),
        }
    

class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()

    body_text = "Waiting for other participants to contribute."


class GroupingWaitPage(WaitPage):
    group_by_arrival_time = True

    def is_displayed(self):
        return self.round_number == 1


    #Sorts participants into groups of 2 males and 2 females
    # def get_players_for_group(self, waiting_players):
    #     m_players = [p for p in waiting_players if p.participant.vars['gender'] == 'Male']
    #     f_players = [p for p in waiting_players if p.participant.vars['gender'] == 'Female']
    #
    #     # print(m_players) # for debugging
    #     # print(f_players) # for debugging
    #
    #     if len(m_players) >= 2 and len(f_players) >= 2:
    #         assortment = self.session.vars.get('assortment')
    #
    #         if assortment == 0:
    #             self.session.vars['assortment'] = 1
    #             return [m_players[0], m_players[1], f_players[0], f_players[1]]
    #         elif assortment == 1:
    #             self.session.vars['assortment'] = 0
    #             return [f_players[0], f_players[1], m_players[0], m_players[1]]
    #         else:
    #             print("there is a problem with the assortment")

    body_text = "Waiting for other participants to arrive."


class Results(Page):
    """Players payoff: How much each has earned"""

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        return {
            'total_earnings': self.group.total_contribution * Constants.multiplier,
            'round_num': self.round_number,
            'experiment_name': self.session.config['experimentName']
        }


class Payoff(Page):

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        return {
            'experiment_name': self.session.config['experimentName']
        }


page_sequence = [
    GroupingWaitPage,
    Introduction,
    Contribute,
    ResultsWaitPage,
    Results,
    Payoff
]
