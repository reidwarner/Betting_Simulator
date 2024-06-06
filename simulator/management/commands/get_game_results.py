from django.core.management import BaseCommand
from bs4 import BeautifulSoup
import requests
from simulator.models import Results


class Command(BaseCommand):
    help = 'Scrape the given URL for the results of the games.'

    def add_arguments(self, parser):
        parser.add_argument('league', type=str)

    def handle(self, *args, **options):
        # Web Scraper for upcoming week of games
        league = options.get('league')
        if league == 'ncaam':
            league = 'ncaab'
        url = "https://www.lines.com/betting/" + league + "/odds"
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