"""
Import all data from CSV from data directory to db
"""
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

import pandas as pd
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.db.models import (
    CENTER_ID,
    POINT_GUARD_ID,
    POSITION_TO_DB_MAPPING,
    POWER_FORWARD_ID,
    SHOOTING_GUARD_ID,
    SMALL_FORWARD_ID,
    Player,
    Position,
    Stat,
    StatPosition,
)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

KG_IN_POUND = 0.453592
CM_IN_INCH = 2.54
INCH_IN_FEET = 12


def convert_height_to_cm(height: str) -> Optional[int]:
    if height is None:
        return None
    height = list(map(int, height.split("-")))
    return round((height[0] * INCH_IN_FEET + height[1]) * CM_IN_INCH)


def player_already_added(x: Dict, players_1: List[Player]) -> bool:
    for player in players_1:
        if x["Player"] == player.name and x["born"] == player.born:
            return True
    return False


def get_positions_ids(positions: str) -> List[int]:
    res = []
    for x in positions.split("-"):
        res.extend(POSITION_TO_DB_MAPPING[x])
    return res


def na_to_none(l: List[Dict]) -> List[Dict]:
    """
    Convert all pandas NA to None in pandas list of dicts
    """
    for elem in l:
        for k, v in elem.items():
            if pd.isna(v):
                elem[k] = None
    return l


def create_positions(session: Session) -> None:
    positions = [
        Position(id=POINT_GUARD_ID, name="Point Guard"),
        Position(id=SHOOTING_GUARD_ID, name="Shooting Guard"),
        Position(id=SMALL_FORWARD_ID, name="Small Forward"),
        Position(id=POWER_FORWARD_ID, name="Power Forward"),
        Position(id=CENTER_ID, name="Center"),
    ]
    session.bulk_save_objects(positions)
    session.commit()
    logging.info("Added %s positions", len(positions))


def import_player_data(session: Session) -> List[Player]:
    player_data_df = pd.read_csv(os.path.join(DATA_DIR, "player_data.csv"))
    player_data_df["name"] = player_data_df["name"].apply(
        lambda x: x.replace("*", "")
    )  # player name could end with *
    player_data_df = player_data_df[player_data_df["name"].notna()]

    players_1 = [
        Player(
            name=x["name"],
            height=convert_height_to_cm(x["height"]),
            weight=round(x["weight"] * KG_IN_POUND)
            if x["weight"] is not None
            else None,
            college=x["college"],
            born=datetime.strptime(x["birth_date"], "%B %d, %Y").year
            if x["birth_date"] is not None
            else None,
        )
        for x in na_to_none(player_data_df.to_dict("records"))
    ]
    session.bulk_save_objects(players_1)
    session.commit()
    logging.info("Added %s players", len(players_1))
    return players_1


def import_players(players_1: List[Player], session: Session) -> None:
    players_df = pd.read_csv(os.path.join(DATA_DIR, "Players.csv"))
    players_df = players_df[players_df["Player"].notna()]
    players_df["Player"] = players_df["Player"].apply(
        lambda x: x.replace("*", "")
    )  # player name could end with *

    players_2 = [
        Player(
            name=x["Player"],
            height=x["height"],
            weight=x["weight"],
            college=x["collage"],
            born=int(x["born"]) if not None else None,
            birth_city=x["birth_city"],
            birth_state=x["birth_state"],
        )
        for x in na_to_none(players_df.to_dict("records"))
        if not player_already_added(x, players_1)
    ]
    session.bulk_save_objects(players_2)
    session.commit()
    logging.info("Added %s more players", len(players_2))


def import_seasons_stats(session: Session) -> None:
    stats_df = pd.read_csv(os.path.join(DATA_DIR, "Seasons_Stats.csv"))
    stats_df = stats_df[stats_df["Pos"].notna()]

    stats_df["Player"] = stats_df["Player"].apply(
        lambda x: x.replace("*", "")
    )  # player name could end with *
    stats_dicts = na_to_none(stats_df.to_dict("records"))

    stats = [
        Stat(name=x["Player"], age=x["Age"], games=x["G"], points=x["PTS"])
        for x in stats_dicts
    ]
    session.bulk_save_objects(stats, return_defaults=True)
    session.commit()
    logging.info("Added %s stats", len(stats))

    stat_positions = []
    for i, x in enumerate(stats_dicts):
        stat_position = [
            StatPosition(position_id=position_id, stat_id=stats[i].id)
            for position_id in get_positions_ids(x["Pos"])
        ]
        stat_positions.extend(stat_position)

    session.bulk_save_objects(stat_positions)
    session.commit()
    logging.info("Added %s stat_positions", len(stat_positions))


def import_data() -> None:
    with SessionLocal() as session:

        if session.query(Position).count():
            logging.info("Data already created")
            return

        create_positions(session)
        players_1 = import_player_data(session)
        import_players(players_1, session)
        import_seasons_stats(session)
