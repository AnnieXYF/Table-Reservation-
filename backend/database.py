from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# change SQLite database address
SQLALCHEMY_DATABASE_URL = "sqlite:///./table_reservation.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

# sessionmaker interact with CRUD
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base(name='Base')


# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
#
#
# # clarify database address
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:Wsxedcrfvtgb10!@127.0.0.1:3306/TableReservation"
# engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True) # log function has been used
#
# # sessionmaker is used to establish session worked by "CRUD" for database DLL and DML
# SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=True)
#
#
# Base = declarative_base(name='Base')
