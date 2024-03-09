from django import forms
from django.forms import ModelForm
from.models import PlacedBet, UserStats


class BetForm(forms.Form):
    bet = forms.MultipleChoiceField(choices=(), widget=forms.Select)
    wager = forms.IntegerField(label="Wager")

    def __init__(self, *args, **kwargs):
        game = kwargs.pop('game', None)
        super(BetForm, self).__init__(*args, **kwargs)
        bet_choices = (
            (f'{game.team_away} {game.spread_away} {game.spread_away_payout}',
             f'{game.team_away} {game.spread_away} {game.spread_away_payout}'),
            (f'{game.team_away} ML {game.money_line_away}', f'{game.team_away} ML {game.money_line_away}'),
            (f'{game.team_home} {game.spread_home} {game.spread_home_payout}',
             f'{game.team_home} {game.spread_home} {game.spread_home_payout}'),
            (f'{game.team_home} ML {game.money_line_home}', f'{game.team_home} ML {game.money_line_home}'),
            (f'Total points {game.total_points_away} {game.total_points_away_payout}',
             f'Total points {game.total_points_away} {game.total_points_away_payout}'),
            (f'Total points {game.total_points_home} {game.total_points_home_payout}',
             f'Total points {game.total_points_home} {game.total_points_home_payout}'),
        )
        self.fields['bet'].choices = bet_choices








