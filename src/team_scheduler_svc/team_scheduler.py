from datetime import datetime, date
from ..exceptions import WeekendException,InitialDateAfterQueryDateError,NotFoundError,InternalServerError
from ..logger.logger import logging
from ..database.db import Database
from ..dto.days import days
from ..dto.teams import TeamCreationRequest,GetTeamsReq,TeamInfoResponse,AddPairRequest
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
            raise InitialDateAfterQueryDateError()
        
        today_name = query_date.strftime("%A")

        if self.days[today_name] > 4:
            raise WeekendException()

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


    def get_schedule(self, team_id: int, query_date: date):
        try:
            team_info = self.team_repo.get_team(team_id)

            if not team_info:
                raise NotFoundError()

            try:
                todays_working_pair, total_working_days = self._get_working_pair(
                    team_info.initial_start_date,
                    query_date,
                    team_info.team_pairs
                )

                return todays_working_pair, total_working_days

            except InitialDateAfterQueryDateError as e:
                logging.error(f"Initial Date After Query Date Error: Initial Date {team_info.initial_start_date}, Query Date {query_date}")
                raise InitialDateAfterQueryDateError()

            except WeekendException:
                logging.warning(f"Query date {query_date} is a weekend.")
                raise WeekendException()

            except Exception as e:
                logging.error(f"Unexpected error in _get_working_pair: {e}")
                raise InternalServerError()
        except WeekendException :
            raise WeekendException()

        except InitialDateAfterQueryDateError :
            raise InitialDateAfterQueryDateError()

        except NotFoundError as e:
            logging.warning(f"Team with ID {team_id} not found: {e}")
            raise NotFoundError(f"Team with ID {team_id} not found.")

        except Exception as e:
            logging.error(f"Unexpected error while fetching schedule for team {team_id}: {e}")
            raise InternalServerError() 
    
    def get_team(self, team_id: int):
        try: 
            team_info = self.team_repo.get_team(team_id)
            if not team_info:
                raise NotFoundError() 

            return team_info
        except NotFoundError:
            raise
        except Exception as e:
            logging.error(f"Error fetching team with ID {team_id}: {e}", exc_info=True)
            raise InternalServerError()
    
    def create_team(self, team_name: str, team_lead: str, initial_start_date: date):
        try:
            _= self.team_repo.create(TeamCreationRequest(
                team_name=team_name,
                team_lead=team_lead,
                initial_start_date=initial_start_date
            ))

            return None
        
        except Exception:
            raise InternalServerError()
        
    def get_teams(self, req: GetTeamsReq):
        try:
            teams = self.team_repo.get_teams(req)
            return teams
        
        except Exception as e:
            logging.error(f"Failed to fetch teams: {e}")
            raise InternalServerError()
        
    def add_team_pair(self, member_1: str, member_2: str, team_id: int):
        try:
            _= self.team_member_repo.add_pair(AddPairRequest(
                member_1=member_1,
                member_2=member_2,
                team_id=team_id
            ))

            return None
        
        except Exception:
            raise InternalServerError()
