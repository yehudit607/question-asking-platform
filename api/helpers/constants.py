from enum import Enum


class Choice(Enum):
    @classmethod
    def choices(cls):
        return tuple((field.name, field.value) for field in cls)

    @classmethod
    def values(cls):
        return [field.value for field in cls]

    @classmethod
    def has_value(cls, value):
        return value in cls.__members__.values()


class QuestionType(Choice):
    POLL = "Poll"
    TRIVIA = "Trivia"
