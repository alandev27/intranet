class Event:
    def __init__(self, start_year: int, start_day: int, day: int, start_hour: int, start_minute: int, duration_hour: int, duration_minute: int, weeks_repeating=1):
        self.start_date = start_year * 1000 + start_day
        self.start_time = start_hour + start_minute / 60
        self.duration = duration_hour + duration_minute / 60
        self.end_time = self.start_time + self.duration
        self.weeks_repeating = weeks_repeating
        self.day = day
