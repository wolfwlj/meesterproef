import os
import sys
import sqlite3
from datetime import datetime
from track import Track

class Event:

    def __init__(self, id=0, name="", track_id=0, date="", distance=0, duration=0.0, laps=0, winner="", category="") -> None:
        self.id = id
        self.name = name
        self.track_id = track_id
        self.date = date
        self.distance = distance
        self.duration = duration
        self.laps = laps
        self.winner = winner
        self.category = category

    def add_skater(skater):
        pass

    def get_skaters(self) -> list:
        con = sqlite3.connect(os.path.join(sys.path[0], 'iceskatingapp.db'))
        cursor = con.cursor()
        cursor.execute("SELECT * FROM event_skaters WHERE event_id = ?", (self.id,))
        skaters = cursor.fetchall()
        return skaters

    def get_track(self):
        con = sqlite3.connect(os.path.join(sys.path[0], 'iceskatingapp.db'))
        cursor = con.cursor()
        cursor.execute("SELECT * FROM tracks WHERE id = ?", (self.track_id,))
        track = cursor.fetchone()
        track = Track(track[0], track[1], track[2], track[3], track[4], track[5])
        return track 


    def convert_date(self, to_format: str) -> str:
        # convert 1956-12-31 to 31-12-1956
        self.date = datetime.strptime(self.date,"%Y-%m-%d")
        self.date = self.date.strftime(f"{to_format}")
        return self.date

    def convert_duration(to_format: str) -> str:
        pass

    # Representation method
    # This will format the output in the correct order
    # Format is @dataclass-style: Classname(attr=value, attr2=value2, ...)
    def __repr__(self) -> str:
        return "{}({})".format(type(self).__name__, ", ".join([f"{key}={value!s}" for key, value in self.__dict__.items()]))
