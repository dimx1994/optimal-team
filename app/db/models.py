import logging
import time

from sqlalchemy import Column, ForeignKey, Integer, PrimaryKeyConstraint, String
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.types import Float

from app.db import Base, engine

POINT_GUARD_ID = 1
SHOOTING_GUARD_ID = 2
SMALL_FORWARD_ID = 3
POWER_FORWARD_ID = 4
CENTER_ID = 5

POSITION_TO_DB_MAPPING = {
    "F": [SMALL_FORWARD_ID, POWER_FORWARD_ID],
    "G": [POINT_GUARD_ID, SHOOTING_GUARD_ID],
    "C": [CENTER_ID],
    "PG": [POINT_GUARD_ID],
    "SG": [SHOOTING_GUARD_ID],
    "SF": [SMALL_FORWARD_ID],
    "PF": [POWER_FORWARD_ID],
}


class Player(Base):
    __tablename__ = "player"
    id = Column(Integer, primary_key=True)
    name = Column(String(80))
    height = Column(Integer)
    weight = Column(Integer)
    college = Column(String(80))
    born = Column(Integer)
    birth_city = Column(String(40))
    birth_state = Column(String(40))

    def __repr__(self):
        return f"Player({self.name}, {self.born})"


class Position(Base):
    __tablename__ = "position"
    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True)

    def __repr__(self):
        return f"Position({self.id}, {self.name})"


class StatPosition(Base):
    __tablename__ = "stat_position"
    position_id = Column(Integer, ForeignKey("position.id"))
    stat_id = Column(Integer, ForeignKey("stat.id"))

    __table_args__ = (
        PrimaryKeyConstraint(
            position_id,
            stat_id,
        ),
    )

    def __repr__(self):
        return f"StatPosition({self.position_id}, {self.stat_id})"


class Stat(Base):
    __tablename__ = "stat"
    id = Column(Integer, primary_key=True)
    name = Column(String(80))
    age = Column(Integer)
    games = Column(Integer)
    points = Column(Float)
    positions = relationship("StatPosition")

    @hybrid_property
    def performance(self):
        return self.points / self.games

    def __repr__(self):
        return f"Stat({self.id}, {self.name}, {self.points})"


def create_all_waiting_postgres() -> None:
    """
    Postgres initialization in docker could take some time so we have to wait
    """
    for _ in range(10):
        try:
            logging.info("Creating all dbs")
            Base.metadata.create_all(bind=engine)
            break
        except OperationalError:
            logging.info("Waiting for postres")
            time.sleep(1)
