from django.db import models


#Game Class
class Game(models.Model):
    #Setup Model
    teams = models.CharField(max_length=200)
    game_date_time = models.CharField(max_length=200)
    team_away = models.CharField(max_length=200)
    team_home = models.CharField(max_length=200)
    spread_away = models.CharField(max_length=10)
    spread_away_payout = models.CharField(max_length=10)
    spread_home = models.CharField(max_length=10)
    spread_home_payout = models.CharField(max_length=10)
    total_points_away = models.CharField(max_length=10)
    total_points_away_payout = models.CharField(max_length=10)
    total_points_home = models.CharField(max_length=10)
    total_points_home_payout = models.CharField(max_length=10)
    money_line_away = models.CharField(max_length=10)
    money_line_home = models.CharField(max_length=10)


class PlacedBet(models.Model):
    user = models.CharField(max_length=200)
    match = models.CharField(max_length=200)
    bet = models.CharField(max_length=200)
    bet_type = models.CharField(max_length=200)
    bet_team = models.CharField(max_length=200)
    bet_payout = models.CharField(max_length=200)
    bet_spread = models.CharField(max_length=200)
    bet_date = models.CharField(max_length=200)
    wager = models.PositiveIntegerField()


class FinisedBet(models.Model):
    user = models.CharField(max_length=200)
    match = models.CharField(max_length=200)
    bet = models.CharField(max_length=200)
    bet_type = models.CharField(max_length=200)
    bet_team = models.CharField(max_length=200)
    bet_payout = models.CharField(max_length=200)
    bet_spread = models.CharField(max_length=200)
    bet_date = models.CharField(max_length=200)
    result = models.CharField(max_length=200)
    wager = models.PositiveIntegerField()

class UserStats(models.Model):
    user = models.CharField(max_length=200)
    bank = models.IntegerField()
    profit = models.IntegerField()
    record = models.CharField(max_length=200)
    wins = models.IntegerField()
    losses = models.IntegerField()
    pushes = models.IntegerField()


class Results(models.Model):
    match = models.CharField(max_length=200)
    team_away = models.CharField(max_length=200)
    team_home = models.CharField(max_length=200)
    team_winner = models.CharField(max_length=200)
    point_diff = models.IntegerField()
    total_points = models.IntegerField()
