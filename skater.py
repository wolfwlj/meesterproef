# # id : int
# - first_name : str
# - last_name : str
# - nationality : str
# - gender: str
# - date_of_birth: date
import os
import sys
import sqlite3
from datetime import date, datetime


class Skater:

    def __init__(self, id=1, first_name="", last_name="", nationality="", gender="", date_of_birth="") -> None:
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.nationality = nationality
        self.gender = gender
        self.date_of_birth = date_of_birth

    def get_age(self, date: date = datetime.now()) -> int:
        # return the age of the skater in years.
        # if no date is given, the current date is used.
        # get the difference between the current date and the date of birth
        delta = date - self.date_of_birth
        # return the age in years
        return int(delta.days / 365.25)

    # return a list of events the skater is participating in
    def get_events(self) -> list:
        con = sqlite3.connect(os.path.join(sys.path[0], 'iceskatingapp.db'))
        cursor = con.cursor()
        cursor.execute("SELECT * FROM event_skaters WHERE skater_id = ?", (self.id,))
        events = cursor.fetchall()
        return events

    # Representation method
    # This will format the output in the correct order
    # Format is @dataclass-style: Classname(attr=value, attr2=value2, ...)
    def __repr__(self) -> str:
        return "{}({})".format(type(self).__name__, ", ".join([f"{key}={value!s}" for key, value in self.__dict__.items()]))
