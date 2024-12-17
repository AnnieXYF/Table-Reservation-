from datetime import datetime, timedelta
from database import SessionLocal
from models import TableInfo

def insert_table_data(table_name):
    session = SessionLocal()
    try:
        # get today
        today = datetime.now().date()
        # calculate the future
        for day_offset in range(90):
            current_date = today + timedelta(days=day_offset)
            # Insert a 2-hour interval from 08:00 to 18:00
            for hour in range(8, 19, 2):
                time_str = f"{hour:02d}:00"
                # create TableInfo object
                new_table_info = TableInfo(
                    table_name=table_name,
                    time_choose=time_str,
                    available_time=True,
                    date_choose=current_date.strftime("%d-%m-%Y"),
                    available_date=True
                )
                # add to session
                session.add(new_table_info)

        # submit
        session.commit()
        print(f"successful！({table_name})")
    except Exception as e:
        # rollback
        session.rollback()
        print(f"failure: {e}")
    finally:
        # close
        session.close()

