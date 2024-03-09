from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Game, PlacedBet, UserStats, FinisedBet
from django.shortcuts import render
from .forms import BetForm
from django.urls import reverse
from .scripts import data_scrape, result_scrape, check_bets


def simulator(request):
    #data_scrape(url='https://www.lines.com/betting/ncaaf/odds/best-line/0?week=13')
    upcoming_games = Game.objects.all().values()
    template = loader.get_template('simulator.html')
    context = {
        'upcoming_games': upcoming_games
    }
    return HttpResponse(template.render(context, request))


def game_details(request, id):
    game = Game.objects.get(id=id)
    template = loader.get_template('game_details.html')

    if request.method == 'POST':
        user_bank = UserStats.objects.filter(user=request.user)[0].bank

    if request.method == 'POST' and float(BetForm(request.POST, game=game).data['wager']) < user_bank:
        form = BetForm(request.POST, game=game)

        bet = form.data['bet']
        wager = form.data['wager']
        user = request.user
        match = f'{game.team_away} vs. {game.team_home}'

        # The bet type needs to be broken down into more info to be used to calc winnings
        if 'ML' in bet:
            bet_type = 'ML'
            bet_team = bet.split('ML', 1)[0].strip()
            if bet_team == game.team_away:
                bet_payout = game.money_line_away
            else:
                bet_payout = game.money_line_home
            if '+' in bet_payout:
                bet_payout = int(bet_payout[1:]) * (int(wager) / 100) + int(wager)
            else:
                bet_payout = 100 * (int(wager) / int(bet_payout[1:])) + int(wager)
            bet_date = game.game_date_time
            bet_spread = 'None'
        elif 'Total points' in bet:
            bet_type = 'TP'
            if 'u' in bet:
                bet_team = game.team_away
            else:
                bet_team = game.team_home
            bet_payout = bet[bet.find("(")+1:bet.find(")")]
            bet_payout = 100 * (int(wager) / int(bet_payout[1:])) + int(wager)
            bet_date = game.game_date_time
            bet_spread = game.total_points_away[1:]
        else:
            bet_type = 'spread'
            bet_team = bet.split('-|\\+')[0]
            if bet_team == game.team_away:
                bet_spread = game.spread_away
            else:
                bet_spread = game.spread_home
            bet_payout = bet[bet.find("(")+1:bet.find(")")]
            bet_payout = 100 * (int(wager) / int(bet_payout[1:])) + int(wager)
            bet_date = game.game_date_time

        bet_payout = '{0:.2f}'.format(bet_payout)
        new_bet = PlacedBet(user=user, match=match, bet=bet, wager=wager, bet_type=bet_type, bet_team=bet_team,
                            bet_payout=bet_payout, bet_spread=bet_spread, bet_date=bet_date)
        new_bet.save()

        us_update = UserStats.objects.filter(user=user)[0]
        us_update.bank = us_update.bank - int(wager)
        us_update.save()

        return HttpResponseRedirect(reverse('simulator'))
    else:
        form = BetForm(game=game)
        context = {
            'game': game,
            'form': form,
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

    # Temporary call of the script to check if bets won and to update the user stats
    #result_scrape(url='https://www.lines.com/betting/ncaaf/odds/best-line/0?week=9')
    #check_bets()


    context = {
        'user': current_user,
        'user_bets': user_bets,
        'user_stats': user_stats,
        'finished_bets': finished_bets,
    }
    return HttpResponse(template.render(context, request))

