from datetime import datetime, date
from ..exceptions import WeekendError,InitialDateAfterQueryDateError
import logging
from ..database.db import Database
from ..dto.days import days
from ..repository.team_repo import TeamRepo
from ..repository.team_member_repo import TeamMemberRepo



class TeamScheduler:
    def __init__(self, db: Database, team_repo:TeamRepo,team_member_repo: TeamMemberRepo):
        self.Db= db
        self.days = days
        self.team_repo = team_repo
        self.team_member_repo =team_member_repo


    def _get_working_pair(
            self, 
            initial_date: date, 
            query_date: date, 
            team_pairs: list[tuple[str, str]], 
):
        if initial_date > query_date:
            logging.error(f"Initial Date After Query  Date Error: Inittial Date {initial_date}, query_date {query_date}")
            raise InitialDateAfterQueryDateError(initial_date,query_date)
        
        today_name = query_date.strftime("%A")

        if self.days[today_name] > 4:
            logging.info("Happy Weekend")
            raise WeekendError()

        initial_weekday_name = initial_date.strftime("%A")
        day_difference = (query_date - initial_date).days + 1

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

            return team_pairs[(current_team_index - 1) % len(team_pairs)], total_working_days_count

        days_remaining_in_first_week = 7 - self.days[initial_weekday_name]
        days_in_last_week = self.days[today_name]

        working_days_in_between_weeks = (day_difference - (days_remaining_in_first_week + days_in_last_week)) // 7
        total_working_days_count = working_days_in_between_weeks * 4

        total_working_days_count += max(0, days_remaining_in_first_week - 2)
        total_working_days_count += min(days_in_last_week, 4)

        team_need_to_work_today = total_working_days_count % len(team_pairs)

        return team_pairs[(team_need_to_work_today - 1) % len(team_pairs)], total_working_days_count


    def get_schedule(self, team_id: int,query_date: date):
        team_info =self.team_repo.get_team(team_id)
        todays_working_pair,total_working_days=self._get_working_pair(
            team_info.initial_start_date,
            query_date,
            team_info.team_pairs
        )

        return todays_working_pair,total_working_days
    
    def get_team(self, team_id: int):
        return self.team_repo.get_team(team_id)

