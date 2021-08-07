from datetime import datetime
import re
from reading import Reading


class ReadingPlan(object):
    def __init__(self, reading_day: int):
        self.reading_day = reading_day
        self.readings = []

    @staticmethod
    def is_reading_plan(line: str) -> bool:
        return "Readings" in line

    def add_reading(self, line: str):
        if Reading.is_reading(line):
            new_reading = Reading(line)
            self.readings.append(new_reading)

    def get_reading_day_str(self) -> str:
        return f"Day {self.reading_day}"
