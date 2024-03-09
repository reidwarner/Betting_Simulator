from bs4 import BeautifulSoup
import requests
import json
from .models import Game, Results, PlacedBet, UserStats, FinisedBet


def data_scrape(url):

    # If upcoming games exist in the db, delete them so only the upcoming games are in there
    future_games = Game.objects.all()
    if future_games:
        future_games.delete()

    # Web Scraper for upcoming week of games
    #url = "https://www.lines.com/betting/ncaaf/odds"
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")
    script = doc.find_all('script')[5].text.strip()

    # game_data is a json file. The relevant fields are ['name'], ['location']['name'], ['awayTeam']['name'],
    # ['homeTeam']['name'], ['startDate']
    game_data = json.loads(script)

    # odds is a list with a bunch of the betting values staggered in the following way: P/S away, P/S payout away, P/S home,
    # P/S payout home, etc.
    odds = doc.find_all('div', {'class': "odds-list-val"})
    teams = doc.find_all('div', {'class': "odds-list-team-title"})
    game_date_times = doc.find_all('div', {'class': "odds-list-section-title"})

    # Loop through to establish all of our variable and add them to the database
    data_dict = {}
    j = 0
    k = 0

    for i in range(0, len(odds), 6):
        # gets team (index 0) and record (index -1)
        team_away = teams[j].text.strip()[:-6].strip()
        team_home = teams[j + 1].text.strip()[:-6].strip()
        game = f'{team_away} vs. {team_home}'
        game_time = game_date_times[k].text.strip()[:-9].strip()
        j += 2
        k += 1

        ps_away = odds[i].text.rsplit('(')
        ps_line_away = ps_away[0].strip()
        ps_payout_away = "(" + ps_away[1].strip()

        ps_home = odds[i + 1].text.rsplit('(')
        ps_line_home = ps_home[0].strip()
        ps_payout_home = "(" + ps_home[1].strip()

        ou_away = odds[i + 2].text.rsplit('(')
        ou_line_away = ou_away[0].strip()
        ou_payout_away = "(" + ou_away[1].strip()

        ou_home = odds[i + 3].text.rsplit('(')
        ou_line_home = ou_home[0].strip()
        ou_payout_home = "(" + ou_home[1].strip()

        ml_away = odds[i + 4].text
        ml_home = odds[i + 5].text

        data_dict[game] = {'date and time': game_time,
                           'away team': team_away,
                           'home team': team_home,
                           'spread away': ps_line_away,
                           'spread away payout': ps_payout_away,
                           'spread home': ps_line_home,
                           'spread home payout': ps_payout_home,
                           'total points away': ou_line_away,
                           'total points away payout': ou_payout_away,
                           'total points home': ou_line_home,
                           'total points home payout': ou_payout_home,
                           'money line away': ml_away,
                           'money line home': ml_home,
                           }

        # Populate the game database

        game_db = Game(teams=game,
                       game_date_time=data_dict[game]['date and time'],
                       team_away=data_dict[game]['away team'],
                       team_home=data_dict[game]['home team'],
                       spread_away=data_dict[game]['spread away'],
                       spread_away_payout=data_dict[game]['spread away payout'],
                       spread_home=data_dict[game]['spread home'],
                       spread_home_payout=data_dict[game]['spread home payout'],
                       total_points_away=data_dict[game]['total points away'],
                       total_points_away_payout=data_dict[game]['total points away payout'],
                       total_points_home=data_dict[game]['total points home'],
                       total_points_home_payout=data_dict[game]['total points home payout'],
                       money_line_away=data_dict[game]['money line away'],
                       money_line_home=data_dict[game]['money line home'],
                       )
        game_db.save()

def result_scrape(url):
    # Web scraper to get the results of games

    # url = "https://www.lines.com/betting/ncaaf/odds/best-line/0?week=10"
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")

    # odds is a list with a bunch of the betting values staggered in the following way: P/S away, P/S payout away, P/S home,
    # P/S payout home, etc.
    odds = doc.find_all('div', {'class': "odds-list-val"})
    teams = doc.find_all('div', {'class': "odds-list-team-title"})
    scores = doc.find_all('div', {'class': 'team-score team-score-passed'})
    game_date_times = doc.find_all('div', {'class': "odds-list-section-title"})

    # Loop through to establish all of our variable and add them to the database
    data_dict = {}
    j = 0
    k = 0

    for i in range(0, len(odds), 6):
        # gets team (index 0) and record (index -1)
        team_away = teams[j].text.strip()[:-6].strip()
        team_home = teams[j + 1].text.strip()[:-6].strip()
        game = f'{team_away} vs. {team_home}'
        score_away = int(scores[k].text.strip())
        score_home = int(scores[k + 3].text.strip())
        j += 2
        k += 4

        win_team = ''
        if score_away > score_home:
            win_team = team_away
        else:
            win_team = team_home

        point_diff = abs(score_home - score_away)

        total_points = score_away + score_home

        data_dict[game] = {'match': game,
                           'away team': team_away,
                           'home team': team_home,
                           'win team': win_team,
                           'point diff': point_diff,
                           'total points': total_points,
                           }

        result_db = Results(match=data_dict[game]['match'],
                            team_away=data_dict[game]['away team'],
                            team_home=data_dict[game]['home team'],
                            team_winner=data_dict[game]['win team'],
                            point_diff=data_dict[game]['point diff'],
                            total_points=data_dict[game]['total points'],
                            )

        result_db.save()

def check_bets():
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
            if bet.bet_spread[0] == '-' and bet.bet_team == res_obj.team_winner and float(bet.bet_spread[1:]) > res_obj.point_diff:
                won = True
            elif bet.bet_spread[0] == '+' and bet.bet_team != res_obj.team_winner and float(bet.bet_spread[1:]) < res_obj.point_diff:
                won = True
            elif bet.bet_spread[0] == '+' and bet.bet_team != res_obj.team_winner:
                won = True
            elif bet.bet_spread[0] == '+' and bet.bet_team != res_obj.team_winner and (float(bet.bet_spread[1:]) - res_obj.point_diff) == 0:
                push = True
            elif bet.bet_spread[0] == '-' and bet.bet_team == res_obj.team_winner and (float(bet.bet_spread[1:]) - res_obj.point_diff) == 0:
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

        #Calculate Record
        us_update.record = f'{us_update.wins}-{us_update.losses}-{us_update.pushes}'
        us_update.save()

        #Transfer Placed bet to finished bit before deleting from placed bet
        finished_bet = FinisedBet(user=bet.user, match=bet.match, bet=bet.bet, wager=bet.wager, bet_type=bet.bet_type,
                                     bet_team=bet.bet_team, bet_payout=bet.bet_payout, bet_spread=bet.bet_spread,
                                     bet_date=bet.bet_date, result=result)
        finished_bet.save()

        #Delete bet from Placed Bet model
        bet.delete()



    # Move placed bet to bet history and delete from PlacedBets


