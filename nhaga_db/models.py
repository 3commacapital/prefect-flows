from sqlalchemy.orm import declarative_base
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
    ForeignKey,
    Date,
    Float,
    JSON,
)
from sqlalchemy.orm import relationship
from nhaga_db import engine

Base = declarative_base()


class Wallet(Base):
    __tablename__ = "wallets"

    address = Column(String(), primary_key=True, unique=True)
    name = Column(String(100))

    valuations = relationship("Valuation", back_populates="wallet")
    snapshots = relationship("Snapshot", back_populates="wallet")

    def __repr__(self):
        return f"<Wallet(address={self.address})>"


class Valuation(Base):
    __tablename__ = "wallet_valuation"

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    value = Column(Float, nullable=False)
    wallet_address = Column(String, ForeignKey("wallets.address"), nullable=False)

    # Relationship to the Wallet model
    wallet = relationship("Wallet", back_populates="valuations")

    def __repr__(self):
        return f"<Valuation(id={self.id}, date={self.date}, value={self.value}, wallet_address={self.wallet_address})>"


class Snapshot(Base):
    __tablename__ = "wallet_snapshots"

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    wallet_address = Column(String, ForeignKey("wallets.address"), nullable=False)
    tokens = Column(JSON, nullable=True)
    projects = Column(JSON, nullable=True)

    wallet = relationship("Wallet", back_populates="snapshots")

    def __repr__(self):
        return f"<Snapshot(id={self.id}, date={self.date}, wallet_address={self.wallet_address})>"


Base.metadata.create_all(engine)
