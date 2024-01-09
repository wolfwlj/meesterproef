from track import Track
from event import Event
from skater import Skater
from datetime import datetime
import os
import sys
import json
import sqlite3

class Reporter:
    def __init__(self) -> None:
        self.con = sqlite3.connect(os.path.join(sys.path[0], 'iceskatingapp.db'))
        self.cursor = self.con.cursor()
    # How many skaters are there? -> int
    def total_amount_of_skaters(self) -> int:
        self.cursor.execute("SELECT COUNT(*) FROM skaters")
        return self.cursor.fetchone()[0]        

    # # What is the highest track? -> Track
    def highest_track(self) -> Track:
        self.cursor.execute("SELECT * FROM tracks ORDER BY altitude DESC LIMIT 1")
        track = self.cursor.fetchone()
        print(track)
        
        answer = Track(track[0], track[1], track[2], track[3], track[4], track[5])
        
        return answer

    # # What is the longest and shortest event? -> tuple[Event, Event]
    def longest_and_shortest_event(self) -> tuple[Event, Event]:
        # this is measured by distance
        self.cursor.execute("SELECT * FROM events ORDER BY distance DESC LIMIT 1")
        longest = self.cursor.fetchone()
        self.cursor.execute("SELECT * FROM events ORDER BY distance ASC LIMIT 1")
        shortest = self.cursor.fetchone()
        
        longest_event = Event(longest[0], longest[1], longest[2], longest[3], longest[4], longest[5], longest[6], longest[7], longest[8])
        shortest_event = Event(shortest[0], shortest[1], shortest[2], shortest[3], shortest[4], shortest[5], shortest[6], shortest[7], shortest[8])
        return (longest_event, shortest_event)
        

    # # Which event has the most laps for the given track_id -> tuple[Event+, ...]
    def events_with_most_laps_for_track(self, track_id: int) -> tuple[Event, ...]:
        self.cursor.execute("SELECT * FROM events WHERE track_id = ? ORDER BY laps DESC LIMIT 1", (track_id,))
        event = self.cursor.fetchone()
        print(event)
        if event is None:
            # dit betekent dat er geen resultaat is voor het gegeven track_id
            return ()
        answer = Event(event[0], event[1], event[2], event[3], event[4], event[5], event[6], event[7], event[8])
        return (answer)

    # Which skaters have made the most events -> tuple[Skater, ...]
    # Which skaters have made the most succesful events -> tuple[Skater, ...]
    def skaters_with_most_events(self, only_wins: bool = False) -> tuple[Skater, ...]:
        #  count most occurences of a skater in the event_skaters table
        skater_id = 0
        # if only_wins is True, we need to check if the skater has won the event.
        # join the event_skaters table with the events table, and check if the skater is the winner
        if only_wins:
            self.cursor.execute("SELECT skater_id, COUNT(*) FROM event_skaters JOIN events ON event_skaters.event_id = events.id WHERE skater_id = winner GROUP BY skater_id ORDER BY COUNT(*) DESC LIMIT 1")
            skater_id = self.cursor.fetchone()[0]
            if skater_id is None:
                # Geen resultaat gevonden
                return ()
            
        else:
            self.cursor.execute("SELECT skater_id, COUNT(*) FROM event_skaters GROUP BY skater_id ORDER BY COUNT(*) DESC LIMIT 1")
            skater_id = self.cursor.fetchone()[0]
            if skater_id is None:
                # Geen resultaat gevonden
                return ()

        self.cursor.execute("SELECT * FROM skaters WHERE id = ?", (skater_id,))
        skater = self.cursor.fetchone()
        answer = Skater(skater[0], skater[1], skater[2], skater[3], skater[4], skater[5])
        return (answer)


    def tracks_with_most_events(self) -> tuple[Track, ...]:
        # count most occurences of a track in the events table
        self.cursor.execute("SELECT track_id, COUNT(*) FROM events GROUP BY track_id ORDER BY COUNT(*) DESC LIMIT 1")
        track_id = self.cursor.fetchone()[0]
        if track_id is None:
            # Geen resultaat gevonden
            return ()
        self.cursor.execute("SELECT * FROM tracks WHERE id = ?", (track_id,))
        track = self.cursor.fetchone()
        answer = Track(track[0], track[1], track[2], track[3], track[4], track[5])
        return (answer)

    # Which track had the first event? -> Event
    # Which track had the first outdoor event? -> Event
    def get_first_event(self, outdoor_only: bool = False) -> Event:
        # browse events table, sort by date, return first result
        if outdoor_only:
            self.cursor.execute("SELECT * FROM events WHERE outdoor = 1 ORDER BY date ASC LIMIT 1")
            event = self.cursor.fetchone()
        else:
            self.cursor.execute("SELECT * FROM events ORDER BY date ASC LIMIT 1")
            event = self.cursor.fetchone()
        
        answer = Event(event[0], event[1], event[2], event[3], event[4], event[5], event[6], event[7], event[8])
        return answer


    # Which track had the latest event? -> event
    # Which track had the latetstoutdoor event? -> event
    def get_latest_event(self, outdoor_only: bool = False) -> Event:
        # vorige functie maar dan andersom
        if outdoor_only:
            self.cursor.execute("SELECT * FROM events WHERE outdoor = 1 ORDER BY date DESC LIMIT 1")
            event = self.cursor.fetchone()
        else:
            self.cursor.execute("SELECT * FROM events ORDER BY date DESC LIMIT 1")
            event = self.cursor.fetchone()
        
        answer = Event(event[0], event[1], event[2], event[3], event[4], event[5], event[6], event[7], event[8])
        return answer

    # Which skaters have raced track Z between period X and Y? -> tuple[Skater, ...]
    # Based on given parameter `to_csv = True` should generate CSV file as  `Skaters on Track Z between X and Y.csv`
    # example: `Skaters on Track Kometa between 2021-03-01 and 2021-06-01.csv`
    # date input always in format: YYYY-MM-DD
    # otherwise it should just return the value as tuple(Skater, ...)
    # CSV example (this are also the headers):
    #   id, first_name, last_name, nationality, gender, date_of_birth
    def get_skaters_that_skated_track_between(self, track: Track, start: datetime, end: datetime, to_csv: bool = False) -> tuple[Skater, ...]:
        pass

    # Which tracks are located in country X? ->tuple[Track, ...]
    # Based on given parameter `to_csv = True` should generate CSV file as  `Tracks in country X.csv`
    # example: `Tracks in Country USA.csv`
    # otherwise it should just return the value as tuple(Track, ...)
    # CSV example (this are also the headers):
    #   id, name, city, country, outdoor, altitude
    def get_tracks_in_country(self, country: str, to_csv: bool = False) -> tuple[Track, ...]:
        pass

    # Which skaters have nationality X? -> tuple[Skater, ...]
    # Based on given parameter `to_csv = True` should generate CSV file as  `Skaters with nationality X.csv`
    # example: `Skaters with nationality GER.csv`
    # otherwise it should just return the value as tuple(Skater, ...)
    # CSV example (this are also the headers):
    #   id, first_name, last_name, nationality, gender, date_of_birth
    def get_skaters_with_nationality(self, nationality: str, to_csv: bool = False) -> tuple[Skater, ...]:
        pass


def main():
    testing = Reporter()
    # print(testing.total_amount_of_skaters())
    # print(testing.highest_track())
    # print(testing.longest_and_shortest_event())
    # print(testing.events_with_most_laps_for_track(15))
    # print(testing.skaters_with_most_events(True))
    # print(testing.tracks_with_most_events())
    # print(testing.get_first_event())
    print(testing.get_latest_event())
    # print(testing.get_skaters_that_skated_track_between())
    # print(testing.get_tracks_in_country())
    # print(get_skaters_with_nationality())

if __name__ == "__main__":
    main()