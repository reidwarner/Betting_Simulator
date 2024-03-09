from django.core.management import BaseCommand

from simulator.models import Results, PlacedBet, UserStats, FinisedBet


class Command(BaseCommand):
    help = 'Scrape the given URL for the upcoming game data.'

    def add_arguments(self, parser):
        ...

    def handle(self, *args, **options):
        # Initialize the check bet variables
        won = False
        push = False

        # Get Placed Bet
        for bet in PlacedBet.objects.all():

            # Compare against the actual result
            res_obj = Results.objects.filter(match=bet.match)[0]

            # Check for each bet type: Spread, TP, ML
            if bet.bet_type == 'ML':
                if bet.bet_team == res_obj.team_winner:
                    won = True
            elif bet.bet_type == 'TP':
                if bet.bet_team == res_obj.team_away and float(bet.bet_spread) < res_obj.total_points:
                    won = True
                elif float(bet.bet_spread) == res_obj.total_points:
                    push = True
            else:
                if bet.bet_spread[0] == '-' and bet.bet_team == res_obj.team_winner and float(
                        bet.bet_spread[1:]) > res_obj.point_diff:
                    won = True
                elif bet.bet_spread[0] == '+' and bet.bet_team != res_obj.team_winner and float(
                        bet.bet_spread[1:]) < res_obj.point_diff:
                    won = True
                elif bet.bet_spread[0] == '+' and bet.bet_team != res_obj.team_winner:
                    won = True
                elif bet.bet_spread[0] == '+' and bet.bet_team != res_obj.team_winner and (
                        float(bet.bet_spread[1:]) - res_obj.point_diff) == 0:
                    push = True
                elif bet.bet_spread[0] == '-' and bet.bet_team == res_obj.team_winner and (
                        float(bet.bet_spread[1:]) - res_obj.point_diff) == 0:
                    push = True
            user = bet.user
            # Update the user stats model
            us_update = UserStats.objects.filter(user=user)[0]
            if won == True:
                us_update.bank += float(bet.bet_payout)
                us_update.profit += float(bet.bet_payout)
                us_update.wins += 1
                result = 'Won'
            elif push == True:
                us_update.bank += bet.wager
                us_update.pushes += 1
                result = 'Push'
            else:
                us_update.profit -= bet.wager
                us_update.losses += 1
                result = 'Lost'

            # Calculate Record
            us_update.record = f'{us_update.wins}-{us_update.losses}-{us_update.pushes}'
            us_update.save()

            # Transfer Placed bet to finished bit before deleting from placed bet
            finished_bet = FinisedBet(user=bet.user, match=bet.match, bet=bet.bet, wager=bet.wager,
                                      bet_type=bet.bet_type,
                                      bet_team=bet.bet_team, bet_payout=bet.bet_payout, bet_spread=bet.bet_spread,
                                      bet_date=bet.bet_date, result=result)
            finished_bet.save()

            # Delete bet from Placed Bet model
            bet.delete()