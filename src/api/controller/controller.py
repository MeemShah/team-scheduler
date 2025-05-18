from src.team_scheduler_svc.team_scheduler import TeamScheduler
from ...config.config import Config

class Controller():
    def __init__(self,cnf:Config,team_svc: TeamScheduler):
        self.cnf = cnf
        self.team_scheduler_svc= team_svc