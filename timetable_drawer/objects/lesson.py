""" Contains the Lesson class. """


class Lesson:
    """ Contains information about a lesson - class, teacher, room and subject.
    """

    def __init__(self, **data: dict[str, str]):
        self.groups = data['groups']
        self.classes = data['classes']
        self.teacher_short = data['teacher_short']
        self.teacher_long = data['teacher_long']
        self.room = data['room']
        self.subject = data['subject']

    def get_lesson_data(self) -> dict[str, str]:
        """ Returns lesson data as a dictionary. """
        lesson_data = {
            'groups': self.groups,
            'classes': self.classes,
            'teacher_short': self.teacher_short,
            'teacher_long': self.teacher_long,
            'room': self.room,
            'subject': self.subject
        }

        return lesson_data
