from skater import Skater
from event import Event
from track import Track


# Test to check if the age of a skater is correct based on the date_of_birth
def test_age_of_skater():
    # test_age = Skater(None,None,None,None,None)
    # resultaat = test_age.get_age()
    # print(resultaat)
    raise NotImplementedError()
    # assert resultaat == 30


# test_age_of_skater()


# Test to check if the amount of events for a specific skater is returned correctly
def test_amount_of_events_of_skater():
    skater = Skater(10, "None", "None", "None", "None", "None")
    assert 6 == len(skater.get_events())


test_amount_of_events_of_skater()


# Test to check if the amount of events for a specific track is returned correctly
def test_amount_of_events_of_track():
    track = Track(22, "None", "None", "None", "None", "None")
    assert 20 == len(track.get_events())


test_amount_of_events_of_track()


# Test to check if the returned date matches the specified format for that event date
def test_event_date_conversion():
    event = Event(5, None, None, "1956-12-31", None, None, None, None, None)
    assert "31-12-1956" == event.convert_date("%d-%m-%Y")


test_event_date_conversion()

# Test to check if the duration is converted from 1H19 to the specified format
def test_event_duration_conversion():
    raise NotImplementedError()


# Test to check the amount of skaters on a specified event
def test_amount_of_skaters_on_event():
    event = Event(1, "None", 1, "None", 1, 1, 1, "None", "None")
    assert 56 == len(event.get_skaters())


test_amount_of_skaters_on_event()


# Test to validate if the given track of a specified event is correct
def test_track_on_event():
    event = Event(None, None, 15, None, None, None, None, None, None)
    track = Track(15, "Ritten Arena", "Collalbo", "ITA", True, 1198)

    assert event.get_track().__dict__ == track.__dict__

test_track_on_event()