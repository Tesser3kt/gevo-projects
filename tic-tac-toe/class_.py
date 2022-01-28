from abc import ABC, abstractmethod


class Human:
    def __init__(self, name, age, gender, height, weight):
        self.name = name if isinstance(name, str) else ''
        self.age = age if age >= 0 else 0
        self.gender = gender
        self.height = height
        self.weight = weight
        self.nationality = ''

    def become_civilian(self, nationality):
        self.nationality = nationality


human1 = Human('Adam', 25, 'helikoptera', 182, 90)
human1.become_civilian('Czech')

human2 = Human('Dalimil', 48, 'panvicka', 123, 250)


class GameObject(ABC):
    def __init__(self, position):
        self.position = position

    @abstractmethod
    def spawn(self):
        ...


class ImmobileGameObject(GameObject):
    def __init__(self, position):
        self.position = position

    def spawn(self):
        ...


class MobileGameObject(GameObject):
    def __init__(self, position):
        self.position = position

    def spawn(self):
        ...

    def move(self):
        ...


objects = [game_object1, game_object2]
