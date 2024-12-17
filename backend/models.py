from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from database import Base, engine

# TableInfo store table info, date, time
class TableInfo(Base):
    __tablename__ = "table_info"
    __table_args__ = {'extend_existing': True}
    table_id = Column(Integer, primary_key=True, autoincrement=True, comment="table_id")
    table_name = Column(String(20), index=True, comment="table_name")
    time_choose = Column(String(5), comment="table_time_choose")
    available_time = Column(Boolean, comment="available_time")
    date_choose = Column(String(10), comment="table_date_choose")
    available_date = Column(Boolean, comment="available_date")

# Reservation store successful booking information
class Reservation(Base):
    __tablename__ = "reservation"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, comment="reservation_id")
    table_name = Column(String(20), ForeignKey("table_info.table_name"), comment="reservation_table_name")
    book_time = Column(String(5), comment="reservation_book_time")
    book_date = Column(String(10), comment="reservation_book_date")

# create the table through sqlalchemy
Base.metadata.create_all(engine)

# from sqlalchemy import Column, Integer, String, ForeignKey,Boolean
# from backend.database import Base,engine
#
# # TableInfo store table info, date, time
# class TableInfo(Base):
#     __tablename__ = "table_info"
#     table_id = Column(Integer, primary_key=True, autoincrement=True,comment="table_id")
#     table_name = Column(String(20), index=True,comment="table_name")
#     time_choose=Column(String(5),comment="table_time_choose")
#     available_time=Column(Boolean,comment="available_time")
#     date_choose=Column(String(10),comment="table_date_choose")
#     available_date = Column(Boolean, comment="available_date")
#
# # Reservation store successful booking information
# class Reservation(Base):
#     __tablename__ = "reservation"
#     id = Column(Integer, primary_key=True, autoincrement=True, index=True,comment="reservation_id")
#     table_name = Column(String(20),ForeignKey("table_info.table_name"),comment="reservation_table_name")
#     book_time = Column(String(5),comment="reservation_book_time")
#     book_date = Column(String(10),comment="reservation_book_date")
#
# # create the table through sqlalchemy
# Base.metadata.create_all(engine)

