from src.team_scheduler.team_scheduler import TeamScheduler

class Controller():
    def __init__(self,team_svc: TeamScheduler):
        self.team_scheduler_svc= team_svc