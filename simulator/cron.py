from django.core.management import call_command
from .management.commands import check_placed_bets, get_game_results, get_new_games


def scheduled_get_new_games_ncaaf():
    call_command('get_new_games', 'ncaaf')


def scheduled_get_new_games_ncaam():
    call_command('get_new_games', 'ncaam')


def scheduled_get_new_games_mlb():
    call_command('get_new_games', 'mlb')


def schedule_get_game_result_ncaaf():
    call_command('get_game_result', 'ncaaf')


def schedule_get_game_result_ncaam():
    call_command('get_game_result', 'ncaam')


def schedule_get_game_result_mlb():
    call_command('get_game_result', 'mlb')


def schedule_check_placed_bets():
    call_command('check_placed_bets')
