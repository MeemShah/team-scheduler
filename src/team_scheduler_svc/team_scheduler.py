from datetime import datetime, date
from ..exceptions import WeekendException,InitialDateAfterQueryDateError,NotFoundError,InternalServerError,EmptyTeamListError
from ..logger.logger import logging
from ..database.db import Database
from ..dto.days import DayToVal,ValToDay
from ..dto.teams import TeamCreationRequest,GetTeamsReq,TeamInfoResponse,AddPairRequest
from ..repository.team_repo import TeamRepo
from ..repository.team_member_repo import TeamMemberRepo
from typing import List, Tuple
from ..config.config import Config
from ..dto.teams import AddWorkingDaysRequest

class TeamScheduler:
    def __init__(self, cnf:Config, team_repo:TeamRepo,team_member_repo: TeamMemberRepo):
        self.cnf= cnf
        self.team_repo = team_repo
        self.team_member_repo = team_member_repo
        self.day_to_val = DayToVal
        self.val_to_date= ValToDay

    def _validate_dates(self, initial_date: date, query_date: date) -> None:
        if initial_date > query_date:
            logging.error(
                f"Initial Date After Query Date Error: Initial Date {initial_date}, Query Date {query_date}"
            )
            raise InitialDateAfterQueryDateError()

    def _is_weekend(self, working_days: List[str], query_date: date) -> bool:
        return query_date.strftime("%A") not in working_days

    def _calculate_total_working_days_count(self, initial_date: date, query_date: date, working_days: List[str]) -> int:
        initial_name = initial_date.strftime("%A")
        query_name = query_date.strftime("%A")
        day_diff = (query_date - initial_date).days + 1

        if day_diff < 7:
            return self._count_within_week(initial_name, day_diff, working_days)
        
        total_working_days = 0

        start_day_index = self.day_to_val[initial_name]
        end_day_index = self.day_to_val[query_name]

        # count working day for the first week
        for day_num in range(start_day_index, 8):
            day_name = self.val_to_date[day_num]
            if day_name in working_days:
                total_working_days += 1

            day_diff-=1

        # count working day for the last week
        for day_num in range(1, end_day_index + 1):
            day_name = self.val_to_date[day_num]
            if day_name in working_days:
                total_working_days += 1

            day_diff-=1

        number_of_working_day_in_week= len(working_days)
        remaining_week=day_diff//7
        total_working_days+=remaining_week*number_of_working_day_in_week

        return total_working_days

    def _count_within_week(self, start_day: str, days: int, working_days: List[str]) -> int:
        count = 0
        day_idx = self.day_to_val[start_day]

        for _ in range(days):
            day_name = self.val_to_date[day_idx]
            
            if day_name in working_days:
                count += 1
            
            day_idx = day_idx % 7 + 1
        
        return count

    def _determine_working_pair(
        self,
        total_working_days: int,
        team_pairs: List[Tuple[str, str]],
    ) -> Tuple[str, str]:
        index = (total_working_days - 1) % len(team_pairs)
        return team_pairs[index]



    def get_schedule(self, team_id: int, query_date: date):
        try:
            team_info = self.team_repo.get_team(team_id)

            if not team_info:
                raise NotFoundError()
            if not team_info.team_pairs:
                raise EmptyTeamListError()

            try:
                self._validate_dates(team_info.initial_start_date,query_date)
                self._is_weekend(team_info.working_days,query_date)
                total_working_days = self._calculate_total_working_days_count( team_info.initial_start_date, query_date,team_info.working_days)
                team = self._determine_working_pair(total_working_days,   team_info.team_pairs)

                return team, total_working_days

            except InitialDateAfterQueryDateError as e:
                logging.error(f"Initial Date After Query Date Error: Initial Date {team_info.initial_start_date}, Query Date {query_date}")
                raise InitialDateAfterQueryDateError()

            except WeekendException:
                logging.warning(f"Query date {query_date} is a weekend.")
                raise WeekendException()

            except Exception as e:
                logging.error(f"Unexpected error in _get_working_pair: {e}")
                raise InternalServerError()
        except EmptyTeamListError:
            raise EmptyTeamListError()
        
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
    
    def create_team(self, team_name: str, team_lead: str, initial_start_date: date, working_days:List[str]):
        try:
            _= self.team_repo.create(TeamCreationRequest(
                team_name=team_name,
                team_lead=team_lead,
                working_days=working_days,
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
        
        except NotFoundError:
            raise NotFoundError()
        
        except Exception as e:
            logging.error(f"Error while adding pairs: {e}", exc_info=True)
            raise InternalServerError()