import os
import sys
import json
import sqlite3

from track import Track
from event import Event
from skater import Skater


def sync_skaters(cur, json_data):
    # read trough json data and create skater objects
    # skater_dict takes the key id of the skater as key, and the skater object as value
    skater_dict = {}

    # the json is structed like : events -> results -> skater
    # so we need to loop trough the events, then trough the results, and then trough the skaters
    for event in json_data:
        for result in event["results"]:
            skater_dict[result["skater"]["id"]] = result["skater"]
 
    # now all the data is in the skater_dict, so we can loop trough it and insert it into the database
    sqltuples = []

    for skaterid in skater_dict:
        inserttuple = (skater_dict[skaterid]["id"], skater_dict[skaterid]["firstName"], skater_dict[skaterid]["lastName"], skater_dict[skaterid]["country"], skater_dict[skaterid]["gender"], skater_dict[skaterid]["dateOfBirth"])
        sqltuples.append(inserttuple)

    cur.executemany("INSERT INTO skaters VALUES(?,?,?,?,?,?)", sqltuples)


def sync_tracks(cur, json_data):
    track_dict = {}

    for event in json_data:
        track_dict[event["track"]["id"]] = event["track"]

    sql_tuples = []

    for trackid in track_dict:
        inserttuple = (track_dict[trackid]["id"], track_dict[trackid]["name"], track_dict[trackid]["city"], track_dict[trackid]["country"], track_dict[trackid]["isOutdoor"], track_dict[trackid]["altitude"])
        sql_tuples.append(inserttuple)

    cur.executemany("INSERT INTO tracks VALUES(?,?,?,?,?,?)", sql_tuples)


def sync_events(cur, json_data):
    event_dict = {}
    for event in json_data:
        event_dict[event["id"]] = event

    sql_tuples = []
    for eventid in event_dict:

        # tijd kan in seconden.milliseconds of in minuten.seconden.milliseconds.
        # dus als het langer is dan 60 seconden convert naar seconden.milliseconds
        if ":" in event_dict[eventid]["results"][0]["time"]:
            # als dit, dan is dit het formaat : 10:10.10
            # dus we moeten het splitsen op de :
            # en dan de eerste waarde * 60 doen en dan de tweede waarde erbij optellen
            # en dan de derde waarde erbij optellen
            newtime = event_dict[eventid]["results"][0]["time"].split(":")
            amountofsecond_added = float(newtime[0]) * 60
            newtime = float(newtime[1]) + amountofsecond_added
            event_dict[eventid]["results"][0]["time"] = newtime

        inserttuple = (event_dict[eventid]["id"], event_dict[eventid]["title"], event_dict[eventid]["track"]["id"], event_dict[eventid]["start"], 
                        event_dict[eventid]["distance"]["distance"], event_dict[eventid]["results"][0]["time"], event_dict[eventid]["distance"]["lapCount"],
                        event_dict[eventid]["results"][0]["skater"]["id"], event_dict[eventid]["category"])
        sql_tuples.append(inserttuple)
    cur.executemany("INSERT INTO events VALUES(?,?,?,?,?,?,?,?,?)", sql_tuples)


def sync_event_skaters(cur, json_data):
    event_dict = {}
    for event in json_data:
        event_dict[event["id"]] = event

    sql_tuples = []

    placeholder_pk = 0
    for eventid in event_dict:
        tempeventid = eventid
        for result in event_dict[eventid]["results"]:
            placeholder_pk += 1
            sql_tuples.append((placeholder_pk, tempeventid, result["skater"]["id"]))

    cur.executemany("INSERT INTO event_skaters VALUES(?,?,?)", sql_tuples)


def main():
    con = sqlite3.connect(os.path.join(sys.path[0], 'iceskatingapp.db'))

    # first delete all the tables
    con.execute("DROP TABLE IF EXISTS skaters")
    con.execute("DROP TABLE IF EXISTS tracks")
    con.execute("DROP TABLE IF EXISTS events")
    con.execute("DROP TABLE IF EXISTS event_skaters")

    con.execute(
        '''CREATE TABLE IF NOT EXISTS skaters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255) NOT NULL,
            nationality VARCHAR(255) NOT NULL,
            gender CHAR(1) NOT NULL,
            date_of_birth DATE NOT NULL
        );''')

    con.execute(
        '''CREATE TABLE IF NOT EXISTS tracks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL,
            city VARCHAR(255) NOT NULL,
            country VARCHAR(255) NOT NULL,
            outdoor BOOL NOT NULL DEFAULT 0,
            altitude INTEGER NOT NULL DEFAULT 0
        );''')

    con.execute('''
            CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL,
            track_id INTEGER NOT NULL,
            date DATE NOT NULL,
            distance INTEGER NOT NULL,
            duration FLOAT NOT NULL,
            laps INTEGER NOT NULL,
            winner VARCHAR(255) NOT NULL,
            category VARCHAR(255) NOT NULL,
            FOREIGN KEY(track_id) REFERENCES tracks(id)
        );''')

    con.execute('''
            CREATE TABLE IF NOT EXISTS event_skaters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            skater_id INTEGER NOT NULL,
            FOREIGN KEY(event_id) REFERENCES events(id),
            FOREIGN KEY(skater_id) REFERENCES skaters(id)
            );''')

    cur = con.cursor()
    return cur, con


if __name__ == "__main__":
    cur, con = main()
    # first process the data from events.json
    # then give the data as parameters to the sync functions
    json_data = open('events.json')
    json_data = json.load(json_data)

    sync_skaters(cur, json_data)
    sync_tracks(cur, json_data)
    sync_events(cur, json_data)
    sync_event_skaters(cur, json_data)
    con.commit()