import os
import sys
import sqlite3


class Track:

    def __init__(self, id=1, name="", city="", country="", outdoor=False, altitude=0) -> None:
        self.id = id
        self.name = name
        self.city = city
        self.country = country
        self.outdoor = outdoor
        self.altitude = altitude

    def get_events(self) -> list:
        con = sqlite3.connect(os.path.join(sys.path[0], 'iceskatingapp.db'))
        cursor = con.cursor()
        cursor.execute("SELECT * FROM events WHERE track_id = ?", (self.id,))
        events = cursor.fetchall()
        return events

    # Representation method
    # This will format the output in the correct order
    # Format is @dataclass-style: Classname(attr=value, attr2=value2, ...)
    def __repr__(self) -> str:
        return "{}({})".format(type(self).__name__, ", ".join([f"{key}={value!s}" for key, value in self.__dict__.items()]))
