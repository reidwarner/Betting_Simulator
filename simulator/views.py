from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import PlacedBet, UserStats, FinisedBet
from .forms import BetForm
from django.urls import reverse
from BetScrape import DataScraper, TimeDateChecks

# Constants
ODDS_URL = "https://www.lines.com/betting/"
sport_dict = {'ncaaf': 'cfb',
              'ncaam': 'ncaab',
              'mlb': 'mlb',
              }


def simulator(request, league):
    odds_scraper = DataScraper(ODDS_URL + sport_dict[league] +'/odds' )
    date_check = TimeDateChecks()
    if not date_check.is_in_season(sport=league):
        template = loader.get_template('simulator_not_season.html')
        context = {
            'league': league,
        }
        return HttpResponse(template.render(context, request))
    else:
        upcoming_games = odds_scraper.scrape_odds()
        template = loader.get_template('simulator.html')
        context = {
            'upcoming_games': upcoming_games,
            'league': league,
        }
        return HttpResponse(template.render(context, request))


def game_details(request, league, team_home):
    print(league)
    print(team_home)
    odds_scraper = DataScraper(ODDS_URL + sport_dict[league] + '/odds')
    odds_scraper.scrape_odds()
    game = odds_scraper.get_single_game_data('odds', team_home)

    template = loader.get_template('game_details.html')

    if request.method == 'POST':
        user_bank = UserStats.objects.filter(user=request.user)[0].bank

    if request.method == 'POST' and float(BetForm(request.POST, game=game).data['wager']) < user_bank:
        form = BetForm(request.POST, game=game)

        bet = form.data['bet']
        wager = form.data['wager']
        user = request.user

        match = game['team_away'] + ' vs. ' + game['team_home']

        # The bet type needs to be broken down into more info to be used to calc winnings
        if 'ML' in bet:
            bet_type = 'ML'
            bet_team = bet.split('ML', 1)[0].strip()
            if bet_team == game['team_away']:
                bet_payout = game['ml_away']
            else:
                bet_payout = game['ml_home']
            if '+' in bet_payout:
                bet_payout = int(bet_payout[1:]) * (int(wager) / 100) + int(wager)
            else:
                bet_payout = 100 * (int(wager) / int(bet_payout[1:])) + int(wager)
            bet_date = game['game_time']
            bet_spread = 'None'
        elif 'Total points' in bet:
            bet_type = 'TP'
            if 'u' in bet:
                bet_team = game['team_away']
            else:
                bet_team = game['team_home']
            bet_payout = bet[bet.find("(")+1:bet.find(")")]
            bet_payout = 100 * (int(wager) / int(bet_payout[1:])) + int(wager)
            bet_date = game['game_time']
            bet_spread = game['ou_line_away'][1:]
        else:
            bet_type = 'spread'
            bet_team = bet.split('-|\\+')[0]
            if bet_team == game['team_away']:
                bet_spread = game['ps_line_away']
            else:
                bet_spread = game['ps_line_home']
            bet_payout = bet[bet.find("(")+1:bet.find(")")]
            bet_payout = 100 * (int(wager) / int(bet_payout[1:])) + int(wager)
            bet_date = game['game_time']

        bet_payout = '{0:.2f}'.format(bet_payout)
        new_bet = PlacedBet(user=user, match=match, bet=bet, wager=wager, bet_type=bet_type, bet_team=bet_team,
                            bet_payout=bet_payout, bet_spread=bet_spread, bet_date=bet_date)
        new_bet.save()

        us_update = UserStats.objects.filter(user=user)[0]
        us_update.bank = us_update.bank - int(wager)
        us_update.save()

        return HttpResponseRedirect(reverse('user_dashboard'))
    else:
        form = BetForm(game=game)
        context = {
            'game': game,
            'form': form,
            'league': league,
        }
        return HttpResponse(template.render(context, request))


def user_dashboard(request):
    template = loader.get_template('user_dashboard.html')
    current_user = request.user
    user_bets = PlacedBet.objects.filter(user=current_user)
    finished_bets = FinisedBet.objects.filter(user=current_user)

    # Initialize User Stats on first load of the dashboard
    if UserStats.objects.filter(user=current_user):
        user_stats = UserStats.objects.filter(user=current_user)[0]
    else:
        user_stats = UserStats(user=current_user,
                               bank=100000,
                               profit=0,
                               record='0-0-0',
                               wins=0,
                               losses=0,
                               pushes=0,
                               )
        user_stats.save()

    context = {
        'user': current_user,
        'user_bets': user_bets,
        'user_stats': user_stats,
        'finished_bets': finished_bets,
    }
    return HttpResponse(template.render(context, request))

