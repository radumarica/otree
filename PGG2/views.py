from ._builtin import Page, WaitPage
from .models import Constants


class Instructions(Page):
    def is_displayed(self):
        return self.round_number == 1


class Contribution(Page):
    form_model = 'player'
    form_fields = ['contribution']


class ContributionWaitPage(WaitPage):
    pass


class PunishingOrRewarding(Page):
    form_model = 'player'

    def get_form_fields(self):
        other_player_ids = []
        for others in self.player.group.get_players():
            other_player_ids.append(others.id_in_group)
        return ['punish_or_reward_other_player_{}'.format(i) for i in other_player_ids]


class PunishingOrRewardingWaitPage(WaitPage):
    players_summaries = [0, 0, 0, 0]

    def summarize_punishments_and_rewards(self):
        self.players_summaries = [0, 0, 0, 0]
        index = 0
        for player in self.group.get_players():
            self.players_summaries[0] += player.punish_or_reward_other_player_1
            self.players_summaries[1] += player.punish_or_reward_other_player_2
            self.players_summaries[2] += player.punish_or_reward_other_player_3
            self.players_summaries[3] += player.punish_or_reward_other_player_4
            index += 1

            print('1', player.punish_or_reward_other_player_1)
            print('2', player.punish_or_reward_other_player_2)
            print('3', player.punish_or_reward_other_player_3)
            print('4', player.punish_or_reward_other_player_4)

        for player in self.players_summaries:
            print('x sum: ', player)

    def distribute_earnings(self):
        clean_contribution_sum = 0
        for player in self.group.get_players():
            clean_contribution_sum += player.contribution
        clean_contribution_sum *= Constants.multiplier

        modified_contribution_sum = clean_contribution_sum + sum(self.players_summaries) * -1

        index = 0
        for player in self.group.get_players():
            player.payoff += modified_contribution_sum / 4.0
            print('PAYOFF BEFORE: ', player.id_in_group, player.payoff)
            print('DEDUCT: ', self.players_summaries[index])
            player.payoff += self.players_summaries[index]
            print('PAYOFF: ', player.id_in_group, player.payoff)
            print('------')
            index += 1

    def add_kept_tokens_to_players(self):
        for player in self.group.get_players():
            player.payoff += (100 - player.contribution)

    def after_all_players_arrive(self):
        self.summarize_punishments_and_rewards()
        self.distribute_earnings()
        self.add_kept_tokens_to_players()


class Results(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        total_payoff = 0
        for r in self.player.in_all_rounds():
            total_payoff += r.payoff
        return {'total_payoff': total_payoff}


page_sequence = [
    Instructions,
    Contribution,
    ContributionWaitPage,
    PunishingOrRewarding,
    PunishingOrRewardingWaitPage,
    Results
]
