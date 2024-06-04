from django import forms
from django.forms import ModelForm
from.models import PlacedBet, UserStats


class BetForm(forms.Form):
    bet = forms.MultipleChoiceField(choices=(), widget=forms.Select)
    wager = forms.IntegerField(label="Wager")

    def __init__(self, *args, **kwargs):
        game = kwargs.pop('game', None)
        team_away = game['team_away']
        team_home = game['team_home']
        spread_away = game['ps_line_away']
        spread_home = game['ps_line_home']
        spread_away_payout = game['ps_payout_away']
        spread_home_payout = game['ps_payout_home']
        money_line_away = game['ml_away']
        money_line_home = game['ml_home']
        total_points_away = game['ou_line_away']
        total_points_away_payout = game['ou_payout_away']
        total_points_home = game['ou_line_home']
        total_points_home_payout = game['ou_payout_home']


        super(BetForm, self).__init__(*args, **kwargs)
        bet_choices = (
            (f'{team_away} {spread_away} {spread_away_payout}',
             f'{team_away} {spread_away} {spread_away_payout}'),
            (f'{team_away} ML {money_line_away}', f'{team_away} ML {money_line_away}'),
            (f'{team_home} {spread_home} {spread_home_payout}',
             f'{team_home} {spread_home} {spread_home_payout}'),
            (f'{team_home} ML {money_line_home}', f'{team_home} ML {money_line_home}'),
            (f'Total points {total_points_away} {total_points_away_payout}',
             f'Total points {total_points_away} {total_points_away_payout}'),
            (f'Total points {total_points_home} {total_points_home_payout}',
             f'Total points {total_points_home} {total_points_home_payout}'),
        )
        self.fields['bet'].choices = bet_choices








