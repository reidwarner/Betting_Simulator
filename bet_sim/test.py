from datetime import datetime

def is_game_started(game_dt):
    game_dt.strip()
    game_date_time_split = game_dt.split(' ', 1)
    game_date = game_date_time_split[0]
    game_time = game_date_time_split[1]
    game_date_split = game_date_time_split[0].split('/', 1)
    game_month = int(game_date_split[0])
    game_day = int(game_date_split[1])
    game_time_split = game_time.split(':', 1)
    game_hour = int(game_time_split[0])
    game_minute_noon = game_time_split[1]
    game_minute = int(game_minute_noon.split(' ', 1)[0])

    if 'PM' in game_dt:
        game_hour += 12

    now = datetime.now()

    if game_month < now.month:
        return True
    if game_day < now.day:
        return True
    if game_hour < now.hour:
        return True
    if game_minute < now.minute:
        return True
    else:
        return False
