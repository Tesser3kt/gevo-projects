""" Contains the Timetable class. """

from objects.lesson import Lesson


class Timetable:
    """ Contains a 'days x hours' array of Lesson. """

    def __init__(self):
        self.days = DAYS
        self.hours = HOURS
        self.timetable: list[list[Lesson]] = [
            [None for _ in range(self.hours)] for _ in range(self.days)
        ]

    def add_lesson(self, day: int, hour: int, lesson: Lesson) -> bool:
        """ Adds a lesson to the timetable given day, hour and lesson data.
        Returns True if lesson can be added (not occupied), False if it can't.
        """

        if day > self.days or hour > self.hours:
            return False

        if self.timetable[day][hour]:
            return False

        self.timetable[day][hour] = lesson
        return True

    def remove_lesson(self, day: int, hour: int) -> bool:
        """ Removes a lesson from the timetable. If it existed, returns True,
        otherwise False. """

        if not self.timetable[day][hour]:
            return False

        self.timetable[day][hour] = None
        return True

    def get_timetable_data(self) -> list[list[dict]]:
        """ Returns an object representation of the timetable. """

        return [
            [hour.get_lesson_data() if hour else None for hour in day]
            for day in self.timetable
        ]
