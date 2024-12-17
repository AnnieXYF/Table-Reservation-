from fastapi import FastAPI,Depends,HTTPException
from pydantic import BaseModel, constr, validator
from database import SessionLocal
from sqlalchemy.orm import Session
from crud import ReservationService, unavailable_date, unavailable_time
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from insert_db import insert_table_data

app=FastAPI()

insert_table_data("Table1")
insert_table_data("Table2")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# pydantic will carry out basemodel verification of the front-end transmitted data to ensure that the data
# can be effectively converted into the required format
class ReservationModel(BaseModel):
    date: str
    time: str

def format_date(date: datetime.date) -> str:
    return date.strftime("%d-%m-%Y")

def format_time(time: datetime.time) -> str:
    return time.strftime("%H:%M")

# table reservation
@app.post("/reserve")
def reserve_table(request:ReservationModel,db:Session=Depends(get_db)):
    # if no date or time, a tips will be feedback
    if not request.date or not request.time:
        raise HTTPException(status_code=400, detail="Missing necessary information")
    service=ReservationService(db)
    reservation= service.make_reservation(request.date,request.time)
    return reservation

# get unavailble date
@app.get("/unavailable_dates")
def get_unavailable_dates(db:Session=Depends(get_db)):
    unavailable_date_service=unavailable_date(db)
    # use get_unavailble_date method
    unavailable_dates=unavailable_date_service.get_unavailable_date()
    return unavailable_dates

@app.get("/unavailable_times/{date}")
def get_unavailable_times(date:str, db:Session=Depends(get_db)):
    # Convert date_str from "DD-MM-YYYY" to "YYYY-MM-DD"
    # date_obj = datetime.datetime.strptime(date, "%d-%m-%Y").date()
    unavailable_time_service=unavailable_time(db)
    unavailable_times=unavailable_time_service.get_unavailable_time(date)
    return unavailable_times

origins = [
    "http://localhost:5137",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:5137",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all source
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("user_router:app", host="0.0.0.0", port=8000)

