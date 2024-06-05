from datetime import datetime, date


class TimeDateChecks:

    def __init__(self):
        self._date_time = datetime.now()
        self._date = str(date.today())
        self._seasons_dict = {"ncaaf": [2024817, 2025127],
                              "ncaam": [20241027, 2025414],
                              "mlb": [2024411, 20241111],
                              }

    @staticmethod
    def is_in_season(self, sport):
        today = ''.join(filter(str.isdigit, self._date))
        if self._seasons_dict[sport][0] < int(today) < self._seasons_dict[sport][1]:
            return True
        else:
            return False