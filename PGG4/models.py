from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Daniel Davidsen'

doc = """
PGG4 -
"""


class Constants(BaseConstants):
    name_in_url = 'PGG4'
    players_per_group = 4  # Remember to add more "payout_from_manager" variables & if-statements in "set_payoffs", in "Group" class if this variable exceeds 4
    num_rounds = 10

    # """Amount allocated to each player"""
    endowment = c(100)
    multiplier = 2

    overview_template = 'PGG4/Overview.html'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution = models.IntegerField()
    individual_share = models.IntegerField()
    total_payoff = models.IntegerField()

    # Add additional variables to this sequence if you want more players
    PR_amount_1 = models.IntegerField(initial=0, blank=True)
    PR_amount_2 = models.IntegerField(initial=0, blank=True)
    PR_amount_3 = models.IntegerField(initial=0, blank=True)
    PR_amount_4 = models.IntegerField(initial=0, blank=True)

    # not important
    punish_1 = models.BooleanField(blank=True)
    punish_2 = models.BooleanField(blank=True)
    punish_3 = models.BooleanField(blank=True)
    punish_4 = models.BooleanField(blank=True)

    reward_1 = models.BooleanField(blank=True)
    reward_2 = models.BooleanField(blank=True)
    reward_3 = models.BooleanField(blank=True)
    reward_4 = models.BooleanField(blank=True)

    def set_poll(self):
        self.total_contribution = sum([p.contribution for p in self.get_players()])
        self.total_payoff = self.total_contribution * Constants.multiplier

    def set_payoffs(self):
        self.individual_share = self.total_contribution * Constants.multiplier / Constants.players_per_group

        # Distributes payoffs to each player (including punishment and reward)
        # This is gonna get changed in a later version
        # Add additional elif statements to this sequence if you want more players
        for p in self.get_players():
            if p.id_in_group == 1:
                p.PR_amount = self.PR_amount_1
                p.individual_share_after_PR = p.fairly_distributed_amount + self.PR_amount_1
            elif p.id_in_group == 2:
                p.PR_amount = self.PR_amount_2
                p.individual_share_after_PR = p.fairly_distributed_amount + self.PR_amount_2
            elif p.id_in_group == 3:
                p.PR_amount = self.PR_amount_3
                p.individual_share_after_PR = p.fairly_distributed_amount + self.PR_amount_3
            elif p.id_in_group == 4:
                p.PR_amount = self.PR_amount_4
                p.individual_share_after_PR = p.fairly_distributed_amount + self.PR_amount_4
            p.total_earnings = p.individual_share_after_PR + (Constants.endowment - p.contribution)


class Player(BasePlayer):
    contribution = models.IntegerField(
        min=0, max=Constants.endowment,
        doc="""The amount contributed by the player""",
    )
    average_player_payoff = models.IntegerField()
    fairly_distributed_amount = models.IntegerField()
    PR_amount = models.IntegerField(initial=0)
    individual_share_after_PR = models.IntegerField()
    total_earnings = models.IntegerField(initial=0)

    def set_fairly_distributed_amount(self):
        self.fairly_distributed_amount = self.contribution * Constants.multiplier

    def calculate_average_payoff(self):
        for o in self.group.get_players():
            remainingEndowment = 0
            for p in o.in_all_rounds():
                remainingEndowment = remainingEndowment + (Constants.endowment - p.contribution)

            o.average_player_payoff = (o.participant.payoff + remainingEndowment) / Constants.num_rounds

    def role(self):
        if self.id_in_group == 1:
            return 'Manager'
        else:
            return 'Worker'
