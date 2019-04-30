from otree.api import (
    models, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c
)

doc = """
PGG1 - basic public goods game
"""


class Constants(BaseConstants):
    name_in_url = 'PGG1'
    players_per_group = 4
    num_rounds = 12
    punishment_amount = 10
    reward_amount = 10

    instructions_template = 'PGG1/Instructions.html'

    endowment = c(100)
    multiplier = 2


class Subsession(BaseSubsession):

    def creating_session(self):
        self.session.vars['assortment'] = 0

    def vars_for_admin_report(self):
        contributions = [p.contribution for p in self.get_players() if p.contribution != None]
        if contributions:
            return {
                'avg_contribution': sum(contributions) / len(contributions),
                'min_contribution': min(contributions),
                'max_contribution': max(contributions),
            }
        else:
            return {
                'avg_contribution': '(no data)',
                'min_contribution': '(no data)',
                'max_contribution': '(no data)',
            }


class Group(BaseGroup):
    total_contribution = models.IntegerField()

    individual_share = models.IntegerField()

    total_payoff = models.IntegerField()

    def set_payoffs(self):
        self.total_contribution = sum([p.contribution for p in self.get_players()])
        self.individual_share = self.total_contribution * Constants.multiplier / Constants.players_per_group
        self.total_payoff = self.total_contribution * Constants.multiplier
        for p in self.get_players():
            p.individual_share_after_PR = self.individual_share
            p.payoff = (Constants.endowment - p.contribution) + self.individual_share


class Player(BasePlayer):
    individual_share_after_PR = models.IntegerField()

    contribution = models.IntegerField(
        min=0, max=Constants.endowment,
        doc="""The amount contributed by the player""",
    )
