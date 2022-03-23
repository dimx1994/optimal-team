import os

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import FileResponse

from app.db import SessionLocal
from app.db.optimal_team import OptimalTeam, get_optimal_team

TEMPLATES = os.path.join(os.path.dirname(__file__), "templates")

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_class=FileResponse)
def index_get():
    return FileResponse(os.path.join(TEMPLATES, "index.html"))


@router.get("/api/v1/optimal-team", response_model=OptimalTeam)
def optimal_team_get(points: int, db: Session = Depends(get_db)):
    return get_optimal_team(db, points)
