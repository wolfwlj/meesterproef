class Event:

    def __init__(self, id=0, name="", track_id=0, date="", distance=0, duration=0.0, laps=0, winner="", category="") -> None:
        self.id = id
        self.name = name
        self.track_id = track_id
        self.date =  date
        self.distance = distance
        self.duration = duration
        self.laps = laps
        self.winner = winner
        self.category = category

    def add_skater(skater):
        pass

    def get_skaters() -> list:
        pass

    def get_track():
        pass

    def convert_date(to_format: str) -> str:
        pass

    def convert_duration(to_format: str) -> str:
        pass
    # Representation method
    # This will format the output in the correct order
    # Format is @dataclass-style: Classname(attr=value, attr2=value2, ...)
    def __repr__(self) -> str:
        return "{}({})".format(type(self).__name__, ", ".join([f"{key}={value!s}" for key, value in self.__dict__.items()]))
