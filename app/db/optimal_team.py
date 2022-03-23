from typing import List

from pydantic import BaseModel
from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import func

from app.db.models import (
    CENTER_ID,
    POINT_GUARD_ID,
    POWER_FORWARD_ID,
    SHOOTING_GUARD_ID,
    SMALL_FORWARD_ID,
    Stat,
    StatPosition,
)


class OptimalTeamPlayer(BaseModel):
    name: str
    performance: float


class OptimalTeam(BaseModel):
    points_per_season: int
    avg_games_in_season: int
    points_per_game: float
    points_per_player: float
    point_guard: OptimalTeamPlayer
    shooting_guard: OptimalTeamPlayer
    small_forward: OptimalTeamPlayer
    power_forward: OptimalTeamPlayer
    center: OptimalTeamPlayer


def get_player_with_the_nearest_performance(
    points_per_player: float,
    player_names: List[str],
    position_id: int,
    session: Session,
) -> Stat:
    player = (
        session.query(Stat)
        .join(StatPosition)
        .filter(
            (StatPosition.position_id == position_id)
            & (Stat.performance <= points_per_player)
            & Stat.name.not_in(player_names)
        )
        .order_by(desc(Stat.performance))
        .limit(1)
        .one()
    )
    return player


def get_optimal_team(session: Session, points: int) -> OptimalTeam:
    avg_games_in_season = session.query(func.avg(Stat.games)).all()[0][0]
    points_per_game = points / avg_games_in_season
    points_per_player = points_per_game / 5
    player_names: List[str] = []

    # I always select player with the specified role whose performance
    # is the nearest to points_per_player
    point_guard = get_player_with_the_nearest_performance(
        points_per_player, player_names, POINT_GUARD_ID, session
    )
    player_names.append(point_guard.name)

    shooting_guard = get_player_with_the_nearest_performance(
        points_per_player, player_names, SHOOTING_GUARD_ID, session
    )
    player_names.append(shooting_guard.name)

    small_forward = get_player_with_the_nearest_performance(
        points_per_player, player_names, SMALL_FORWARD_ID, session
    )
    player_names.append(small_forward.name)

    power_forward = get_player_with_the_nearest_performance(
        points_per_player, player_names, POWER_FORWARD_ID, session
    )
    player_names.append(power_forward.name)

    center = get_player_with_the_nearest_performance(
        points_per_player, player_names, CENTER_ID, session
    )
    player_names.append(center.name)

    optimal_team = OptimalTeam(
        points_per_season=points,
        avg_games_in_season=avg_games_in_season,
        points_per_game=points_per_game,
        points_per_player=points_per_player,
        point_guard=OptimalTeamPlayer(
            name=point_guard.name, performance=point_guard.performance
        ),
        shooting_guard=OptimalTeamPlayer(
            name=shooting_guard.name, performance=shooting_guard.performance
        ),
        small_forward=OptimalTeamPlayer(
            name=small_forward.name, performance=small_forward.performance
        ),
        power_forward=OptimalTeamPlayer(
            name=power_forward.name, performance=power_forward.performance
        ),
        center=OptimalTeamPlayer(name=center.name, performance=center.performance),
    )
    return optimal_team
