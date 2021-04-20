from fastapi import HTTPException
from http import HTTPStatus
from enums import Team


class Scores(object):

    def __init__(self):
        self.goals = {Team.AWAY: 0, Team.HOME: 0}

    def register_goal(self, team: str):
        if team not in Team.NAMES:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"{team} is not a valid team name")
        self.goals[team] += 1
        return self.goals

    def get_score(self):
        return self.goals
