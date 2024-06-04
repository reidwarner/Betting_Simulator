from bs4 import BeautifulSoup

import requests


class DataScraper:

    def __init__(self, url):
        self._url = url
        self._odds_dict = {}
        self._scores_dict = {}

    def scrape_odds(self):

        # Web Scraper for upcoming week of games
        soup = requests.get(self._url)
        doc = BeautifulSoup(soup.text, "html.parser")

        # odds is a list with a bunch of the betting values staggered in the following way: P/S away, P/S payout away,
        # P/S home, P/S payout home, etc.
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
            game_time = game_date_times[k].text.strip()[:-5].strip()
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

            data_dict[game] = {'game_time': game_time,
                               'team_away': team_away,
                               'team_home': team_home,
                               'ps_line_away': ps_line_away,
                               'ps_payout_away': ps_payout_away,
                               'ps_line_home': ps_line_home,
                               'ps_payout_home': ps_payout_home,
                               'ou_line_away': ou_line_away,
                               'ou_payout_away': ou_payout_away,
                               'ou_line_home': ou_line_home,
                               'ou_payout_home': ou_payout_home,
                               'ml_away': ml_away,
                               'ml_home': ml_home,
                               }

        self._odds_dict = data_dict
        return data_dict

    def scrape_scores(self):

        result = requests.get(self._url)
        doc = BeautifulSoup(result.text, "html.parser")

        # odds is a list with a bunch of the betting values staggered in the following way: P/S away, P/S payout away,
        # P/S home, P/S payout home, etc.
        odds = doc.find_all('div', {'class': "odds-list-val"})
        teams = doc.find_all('div', {'class': "odds-list-team-title"})
        scores = doc.find_all('div', {'class': 'team-score team-score-passed'})
        game_date_times = doc.find_all('div', {'class': "odds-list-section-title"})

        # Loop through to establish all of our variable and add them to the database
        data_dict = {}
        j = 0
        k = 0
        m = 0

        for i in range(0, len(odds), 6):
            game_time = game_date_times[m].text.strip()[:-5].strip()

            if game_time == 'Final':
                # gets team (index 0) and record (index -1)
                team_away = teams[j].text.strip()[:-6].strip()
                team_home = teams[j + 1].text.strip()[:-6].strip()
                game = f'{team_away} vs. {team_home}'
                score_away = int(scores[k].text.strip())
                score_home = int(scores[k + 2].text.strip())

                j += 2
                k += 4
                m += 1

                if score_away > score_home:
                    win_team = team_away
                else:
                    win_team = team_home

                point_diff = abs(score_home - score_away)

                total_points = score_away + score_home

                data_dict[game] = {'game': game,
                                   'team_away': team_away,
                                   'team_home': team_home,
                                   'score_away': score_away,
                                   'score_home': score_home,
                                   'win_team': win_team,
                                   'point_diff': point_diff,
                                   'total_points': total_points,
                                   }

            else:
                j += 2
                m += 1
        self._scores_dict = data_dict
        return data_dict

    def get_single_game_data(self, data_type, team_home):
        if data_type == 'odds':
            for game in self._odds_dict:
                if self._odds_dict[game]['team_home'] == team_home:
                    return self._odds_dict[game]
        if data_type == 'scores':
            for game in self._scores_dict:
                if self._scores_dict[game]['match'] == team_home:
                    return self._scores_dict[game]
