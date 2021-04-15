from enum import unique, Enum


@unique
class Version(Enum):
    value: int
    HIRO_5 = 5
    HIRO_6 = 6
    HIRO_7 = 7
