from datetime import datetime, date


class GameDateAndTime:

    @staticmethod
    def is_in_season(sport):
        date_time = datetime.now()
        today = str(date.today())
        seasons_dict = {"ncaaf": [2024817, 2025127],
                        "ncaam": [20241027, 2025414],
                        "mlb": [2024411, 20241111],
                        }

        today = ''.join(filter(str.isdigit, today))
        if seasons_dict[sport][0] < int(today) < seasons_dict[sport][1]:
            return True
        else:
            return False