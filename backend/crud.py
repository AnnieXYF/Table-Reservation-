from sqlalchemy.orm import Session
from sqlalchemy import and_
from models import Reservation,TableInfo
from fastapi import HTTPException


# reservation function
class ReservationService:
    def __init__(self, db: Session):
        self.db = db
    # date and time are the data transmit from fontend

    def make_reservation(self,date,time):
        # Filter the first data that both the time and date match as available table information
        available_table = self.db.query(TableInfo).filter(
            and_(
                TableInfo.available_time==True,
                TableInfo.available_date==True,
                TableInfo.time_choose==time,
                TableInfo.date_choose==date
        )).first()
        # if no available table, return the message
        if not available_table:
            raise HTTPException(status_code=400, detail="No available table")

        # create data in reservation table
        reservation=Reservation(
                table_name=available_table.table_name,
                book_time=available_table.time_choose,
                book_date=available_table.date_choose
        )
        # Update the available_time status of the corresponding table number in the TableInfo table
        available_table.available_time=False

        # Add the reservation data to the Reservation table
        self.db.add(reservation)
        self.db.commit()
        self.db.refresh(reservation)
        # return successful reservation information
        return {"status": "success", "message": f'reservation made for {reservation.book_date} at {reservation.book_time}'}

#unavailble date selection
class unavailable_date:
    def __init__(self,db:Session):
        self.db = db

    def get_unavailable_date(self):
        # Filter a specific date with a false (that is, unavailable) date, and only one is reserved for deduplication
        unavailble_dates=(self.db.query(TableInfo.date_choose).filter(
            TableInfo.available_date==False)
         .distinct()
         .all()
        )
        # Converts the obtained unavailable dates into a list
        unavailble_dates_list=[date[0] for date in unavailble_dates]
        # get all table information
        table_names=self.db.query(TableInfo.table_name).filter().distinct()
        # Turn the table name into a list
        table_names_list=[table[0] for table in table_names]
        final_unavailble_dates_list=[]
        # Filter table names for each date in the unavailable date list
        for date in unavailble_dates_list:
            # Keep only those table names that are not available on the specified date
            table_name_with_date=(self.db.query(TableInfo.table_name).filter(
                and_(
                TableInfo.available_date==False,
                TableInfo.date_choose==date))
                .distinct()
                .all()
            )
            # Converts table names under unavailable dates to a list
            table_names_with_date_list=[table[0] for table in table_name_with_date]
            if set(table_names_with_date_list)==set(table_names_list):
                final_unavailble_dates_list.append(date)
        return {"unavailable_dates":final_unavailble_dates_list}

# unavailable time selection
class unavailable_time:
    def __init__(self,db:Session):
        self.db = db

    def get_unavailable_time(self,target_date):
        # Get the unavailable time passed in date, remove the repeat item
        unavailable_times_by_date=(self.db.query(TableInfo.time_choose).filter(
            and_(
            TableInfo.date_choose==target_date,
            TableInfo.available_time==False))
            .distinct()
            .all()
        )
        # create unavilable time list
        unavailable_times_by_date_list=[time[0] for time in unavailable_times_by_date]
        print(unavailable_times_by_date_list,"unavailable_times_by_date_list")
        final_unavailable_times = []
        table_names = self.db.query(TableInfo.table_name).filter().distinct()
        table_names_list = [table[0] for table in table_names]
        print(table_names_list,"table_names_list")
        # Perform a secondary filter for the unavailable time under the specified date, and reserve the corresponding table name
        for time in unavailable_times_by_date_list:
            table_name_with_time_and_date=(self.db.query(TableInfo.table_name).filter(
                and_(
                TableInfo.time_choose==time,
                TableInfo.available_time==False,
                TableInfo.date_choose==target_date
            )).distinct().
            all())
            table_name_with_time_and_date_list=[table[0] for table in table_name_with_time_and_date]
            print(table_name_with_time_and_date_list,"table_name_with_time_and_date_list")
            # Unavailable time If the table name is equal to the complete set, the time is listed as the unavailable time under the date
            if set(table_name_with_time_and_date_list)==set(table_names_list):
                final_unavailable_times.append(time)
        return {"unavailable_times":final_unavailable_times}
