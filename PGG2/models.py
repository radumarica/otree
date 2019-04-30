from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

author = 'Barney Garda'

doc = """
PGG2 - everyone can punish / reward everyone else
"""


class Constants(BaseConstants):
    name_in_url = 'PGG2'
    players_per_group = 4
    num_rounds = 10
    num_rounds_range = range(num_rounds)

    endowment = c(100)
    multiplier = 2


class Subsession(BaseSubsession):
    payout_for_player_1 = models.FloatField(min=0)
    payout_for_player_2 = models.FloatField(min=0)
    payout_for_player_3 = models.FloatField(min=0)
    payout_for_player_4 = models.FloatField(min=0)


class Group(BaseGroup):
    total_contribution = models.IntegerField()
    total_payoff = models.IntegerField()

    payout_from_player_1 = models.FloatField(min=0)
    payout_from_player_2 = models.FloatField(min=0)
    payout_from_player_3 = models.FloatField(min=0)
    payout_from_player_4 = models.FloatField(min=0)


class Player(BasePlayer):
    contribution = models.IntegerField(
        min=0, max=Constants.endowment,
        doc="""The amount contributed by the player""",
    )

    punish_or_reward_other_player_1 = models.IntegerField(
        choices=[-10, 0, 10],
        default=0,
        widget=widgets.RadioSelectHorizontal
    )

    punish_or_reward_other_player_2 = models.IntegerField(
        choices=[-10, 0, 10],
        default=0,
        widget=widgets.RadioSelectHorizontal
    )

    punish_or_reward_other_player_3 = models.IntegerField(
        choices=[-10, 0, 10],
        default=0,
        widget=widgets.RadioSelectHorizontal
    )

    punish_or_reward_other_player_4 = models.IntegerField(
        choices=[-10, 0, 10],
        default=0,
        widget=widgets.RadioSelectHorizontal
    )

    def in_all_rounds_full_range(self):
        empty_list_tail = [None] * (Constants.num_rounds - len(self.in_all_rounds()))
        return self.in_all_rounds() + empty_list_tail
