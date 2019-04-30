from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Daniel Davidsen'

doc = """
PGG3 - 
"""


class Constants(BaseConstants):
    name_in_url = 'PGG3'
    players_per_group = 4  # Remember to add more "payout_from_manager" variables & if-statements in "set_payoffs", in "Group" class if this variable exceeds 4
    num_rounds = 12


    endowment = c(100)
    multiplier = 2

    overview_template = 'PGG3/Overview.html'
    instructions_template_for_members = 'PGG3/InstructionForGroupMember.html'
    instructions_template_for_manager = 'PGG3/InstructionForGroupManager.html'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution = models.IntegerField()
    total_payoff = models.IntegerField()

    #Add additional variables to this sequence if you want more players
    payout_from_manager_1 = models.FloatField(min=0)
    payout_from_manager_2 = models.FloatField(min=0)
    payout_from_manager_3 = models.FloatField(min=0)
    payout_from_manager_4 = models.FloatField(min=0)

    equally_distributed = models.BooleanField(blank=True)

    def set_poll(self):
        self.total_contribution = sum([p.contribution for p in self.get_players()])
        self.total_payoff = self.total_contribution * Constants.multiplier
        self.set_fairly_distributed_amount()

    def set_fairly_distributed_amount(self):
        for p in self.get_players():
            p.fairly_distributed_amount()

    def set_payoffs(self):
        residuals = (self.total_payoff - (self.payout_from_manager_1 + self.payout_from_manager_2 + self.payout_from_manager_3 + self.payout_from_manager_4))/Constants.players_per_group

        # Add additional elif statements to this sequence if you want more players
        for p in self.get_players():
            if p.id_in_group == 1:
                p.earnings = self.payout_from_manager_1
                p.payoff = self.payout_from_manager_1 + residuals
            elif p.id_in_group == 2:
                p.earnings = self.payout_from_manager_2
                p.payoff = self.payout_from_manager_2 + residuals
            elif p.id_in_group == 3:
                p.earnings = self.payout_from_manager_3
                p.payoff = self.payout_from_manager_3 + residuals
            elif p.id_in_group == 4:
                p.earnings = self.payout_from_manager_4
                p.payoff = self.payout_from_manager_4 + residuals


class Player(BasePlayer):
    contribution = models.IntegerField(
        min=0, max=Constants.endowment,
        doc="""The amount contributed by the player""",
    )
    average_player_payoff = models.IntegerField()
    fairlyDistributedAmount = models.IntegerField()
    earnings = models.IntegerField()

    def fairly_distributed_amount(self):
        self.fairlyDistributedAmount = self.contribution * Constants.multiplier

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

