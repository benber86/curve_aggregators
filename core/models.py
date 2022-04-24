from dataclasses import dataclass
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, ForeignKey, DateTime, Integer, Float, Sequence
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import create_engine
import os


db_path = "sqlite:////" + os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "trades.db"
)
engine = create_engine(db_path)

# typing issue : https://github.com/python/mypy/issues/2477
Base = declarative_base()  # type: Any


@dataclass
class Token:
    symbol: str
    address: str
    decimals: int


@dataclass
class Route:
    exchange: str
    amount_out: int


@dataclass
class PreRecord:
    exchange: str
    amount_out: int
    rank: int
    loss_pct: float


class Trade(Base):
    __tablename__ = "trades"
    id = Column(Integer, Sequence("id_seq"), primary_key=True, autoincrement=True)
    pair = Column(String)
    amount = Column(Integer)
    timestamp = Column(DateTime, server_default=func.now())
    records = relationship("Record")


class Record(Base):
    __tablename__ = "records"
    id = Column(Integer, Sequence("id_seq"), primary_key=True, autoincrement=True)
    exchange = Column(String)
    amount_out = Column(Float)
    rank = Column(Integer)
    original_rank = Column(Integer)
    loss_pct = Column(Float)
    trade = Column(Integer, ForeignKey("trades.id"))

    def __init__(
        self,
        exchange: str,
        amount_out: int,
        rank: int,
        original_rank: int,
        loss_pct: float,
        trade: Trade,
    ):

        self.exchange = exchange
        self.amount_out = amount_out
        self.rank = rank
        self.original_rank = original_rank
        self.loss_pct = loss_pct
        self.trade = trade


Base.metadata.create_all(engine)
