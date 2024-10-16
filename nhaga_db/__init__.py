from sqlalchemy import create_engine
from sqlalchemy.engine import URL


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
