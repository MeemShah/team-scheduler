from datetime import datetime, date
from config import INITIAL_DATE, TEAM_PAIRS, PAIR_SEQUESNCE

days = {
    "Sunday": 1,
    "Monday": 2,
    "Tuesday": 3,
    "Wednesday": 4,
    "Thursday": 5,
    "Friday": 6,
    "Saturday": 7
}

def get_todays_working_pair(initial_date: date, todays_date: date):
    if initial_date>todays_date:
        return None,-1
    
    today_name = todays_date.strftime("%A")

    initial_weekday_name = initial_date.strftime("%A")

    day_difference = (todays_date - initial_date).days + 1  

    if day_difference < 7: 
        current_team_index = 0
        day = days[initial_weekday_name]
        total_working_days_count = 0

        for _ in range(day_difference):
            if day < 5:
                total_working_days_count += 1
                current_team_index += 1

                if current_team_index >= len(TEAM_PAIRS):
                    current_team_index = 0

            day += 1
            if day > 7:
                day = 1

        return TEAM_PAIRS[current_team_index - 1], total_working_days_count

    days_remaining_in_first_week = 7 - days[initial_weekday_name]
    days_in_last_week = days[today_name]

    working_days_in_between_weeks = (day_difference - (days_remaining_in_first_week + days_in_last_week)) // 7
    total_working_days_count = working_days_in_between_weeks * 4

    total_working_days_count += max(0, days_remaining_in_first_week - 2)
    total_working_days_count += min(days_in_last_week, 4)

    team_need_to_work_today = total_working_days_count % len(TEAM_PAIRS)

    return TEAM_PAIRS[team_need_to_work_today - 1], total_working_days_count


TODAY_DATE = date(2025, 4, 28)
pair, total_working_days = get_todays_working_pair(INITIAL_DATE, TODAY_DATE)

if pair:
    print(f"Today's working pair: {pair}")
    print(f"Total working days: {total_working_days}")