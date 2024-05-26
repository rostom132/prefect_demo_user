from enum import Enum

class Gender(str, Enum):
    male = 'male'
    female = 'female'

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_
    
class DataType(str, Enum):
    failed = 'failed'
    correct = 'correct'
    incorrect = 'incorrect'
    corrupted = 'corrupted'

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_
    