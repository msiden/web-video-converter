from fastapi import FastAPI
from scores import Scores


scores = Scores()
app = FastAPI()


@app.get("/score")
def score():
    return scores.get_score()


@app.post("/goal")
def goal(team: str):
    return scores.register_goal(team=team)
