from datetime import datetime, date
from ..exceptions import WeekendError,InitialDateAfterTodayError
import logging
class TeamScheduler:
    def __init__(self):
        self.days = {
            "Sunday": 1,
            "Monday": 2,
            "Tuesday": 3,
            "Wednesday": 4,
            "Thursday": 5,
            "Friday": 6,
            "Saturday": 7
        }

    def get_todays_working_pair(
            self, 
            initial_date: date, 
            today_date: date, 
            team_pairs: list[tuple[str, str]], 
            pair_sequence: list[int],
):
        if initial_date > today_date:
            logging.error(f"Initial Date After Today Error: Inittial Date {initial_date}, today_date {today_date}")
            raise InitialDateAfterTodayError(initial_date,today_date)
        
        today_name = today_date.strftime("%A")

        if self.days[today_name] > 4:
            logging.info("Happy Weekend")
            raise WeekendError()

        initial_weekday_name = initial_date.strftime("%A")
        day_difference = (today_date - initial_date).days + 1

        if day_difference < 7:
            current_team_index = 0
            day = self.days[initial_weekday_name]
            total_working_days_count = 0

            for _ in range(day_difference):
                if day < 5:
                    total_working_days_count += 1
                    current_team_index += 1

                    if current_team_index >= len(team_pairs):
                        current_team_index = 0

                day += 1
                if day > 7:
                    day = 1

            return team_pairs[pair_sequence[(current_team_index - 1) % len(pair_sequence)]], total_working_days_count

        days_remaining_in_first_week = 7 - self.days[initial_weekday_name]
        days_in_last_week = self.days[today_name]

        working_days_in_between_weeks = (day_difference - (days_remaining_in_first_week + days_in_last_week)) // 7
        total_working_days_count = working_days_in_between_weeks * 4

        total_working_days_count += max(0, days_remaining_in_first_week - 2)
        total_working_days_count += min(days_in_last_week, 4)

        team_need_to_work_today = total_working_days_count % len(team_pairs)

        return team_pairs[pair_sequence[(team_need_to_work_today - 1) % len(pair_sequence)]], total_working_days_count

