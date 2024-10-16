from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float, JSON
from sqlalchemy.orm import relationship, sessionmaker

url = URL.create(
    drivername="postgresql",
    username="root",
    host="nhaga.xyz",
    port="2665",
    password="apassemerda",
    database="nhaga_DB",
)

engine = create_engine(url)
connection = engine.connect()

Base = declarative_base()

class Asset(Base):
    __tablename__ = "assets"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    values = relationship("AssetValue", back_populates="asset")


class AssetValue(Base):
    __tablename__ = "asset_values"
    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    date = Column(Date, nullable=False)
    value = Column(Float, nullable=False)
    asset = relationship("Asset", back_populates="values")



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

Session = sessionmaker(bind=engine)
session = Session()
