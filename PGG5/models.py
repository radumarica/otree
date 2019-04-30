from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

author = 'Barney Garda'

doc = """
PGG 5 - Manager rewards / punishes fix amount
"""


class Constants(BaseConstants):
    name_in_url = 'PGG5'
    players_per_group = 4
    num_rounds = 10
    num_rounds_range = range(num_rounds)

    endowment = c(100)
    multiplier = 2
    reinforcement = 10


class Subsession(BaseSubsession):
    payout_for_player_1 = models.FloatField(min=0)
    payout_for_player_2 = models.FloatField(min=0)
    payout_for_player_3 = models.FloatField(min=0)
    payout_for_player_4 = models.FloatField(min=0)


class Group(BaseGroup):
    total_contribution = models.IntegerField()
    total_payoff = models.IntegerField()

    reinforcement_player_1 = models.IntegerField(
        choices=[-Constants.reinforcement, 0, Constants.reinforcement],
        default=0,
        widget=widgets.RadioSelectHorizontal,
        doc="""Reinforcement for player 1 (punishment / reward) given by the manager"""
    )

    reinforcement_player_2 = models.IntegerField(
        choices=[-Constants.reinforcement, 0, Constants.reinforcement],
        default=0,
        widget=widgets.RadioSelectHorizontal,
        doc="""Reinforcement for player 2 (punishment / reward) given by the manager"""
    )

    reinforcement_player_3 = models.IntegerField(
        choices=[-Constants.reinforcement, 0, Constants.reinforcement],
        default=0,
        widget=widgets.RadioSelectHorizontal,
        doc="""Reinforcement for player 3 (punishment / reward) given by the manager"""
    )

    reinforcement_player_4 = models.IntegerField(
        choices=[-Constants.reinforcement, 0, Constants.reinforcement],
        default=0,
        widget=widgets.RadioSelectHorizontal,
        doc="""Reinforcement for player 4 (punishment / reward) given by the manager"""
    )

    def fill_reinforcement_list(self):
        self.session.vars['reinforcement_player_1'] = self.reinforcement_player_1
        self.session.vars['reinforcement_player_2'] = self.reinforcement_player_2
        self.session.vars['reinforcement_player_3'] = self.reinforcement_player_3
        self.session.vars['reinforcement_player_4'] = self.reinforcement_player_4

    def public_good_per_player(self):
        all_contrib = 0
        for p in self.get_players():
            all_contrib += p.contribution
        return (1 / Constants.players_per_group) * Constants.multiplier * all_contrib

    def calculate_total_contribution(self):
        all_contrib = 0
        for p in self.get_players():
            all_contrib += p.contribution
        self.total_contribution = all_contrib


class Player(BasePlayer):
    def role(self):
        if self.id_in_group == 1:
            return 'manager'
        else:
            return 'peer'

    contribution = models.IntegerField(
        min=0, max=Constants.endowment,
        doc="""The amount contributed by the player""",
    )

    def in_all_rounds_previous_range(self):
        empty_list_tail = [None] * (Constants.num_rounds - len(self.in_previous_rounds()))
        return self.in_previous_rounds() + empty_list_tail

    def in_all_rounds_full_range(self):
        empty_list_tail = [None] * (Constants.num_rounds - len(self.in_all_rounds()))
        return self.in_all_rounds() + empty_list_tail

    def calculate_payoff(self):
        reinforcement_list = [
            self.session.vars['reinforcement_player_1'],
            self.session.vars['reinforcement_player_2'],
            self.session.vars['reinforcement_player_3'],
            self.session.vars['reinforcement_player_4']
        ]
        self.payoff = Constants.endowment - self.contribution \
                      + self.group.public_good_per_player() \
                      + reinforcement_list[self.id_in_group-1] \
                      - (1 / Constants.players_per_group) * sum(reinforcement_list)
