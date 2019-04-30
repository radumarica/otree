from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

author = 'Barney Garda'

doc = """
PGG 0 - Basic public goods game
"""


class Constants(BaseConstants):
    name_in_url = 'PGG0'
    players_per_group = 4
    num_rounds = 10
    num_rounds_range = range(num_rounds)

    endowment = c(100)
    multiplier = 2


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution = models.IntegerField()
    total_payoff = models.IntegerField()

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
    contribution = models.IntegerField(
        min=0, max=Constants.endowment,
        doc="""The amount contributed by the player""",
    )

    def in_all_rounds_full_range(self):
        empty_list_tail = [None] * (Constants.num_rounds - len(self.in_all_rounds()))
        return self.in_all_rounds() + empty_list_tail

    def calculate_payoff(self):
        self.payoff = Constants.endowment - self.contribution \
                      + self.group.public_good_per_player()
