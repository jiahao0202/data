from enum import Enum


class SurfaceTypeEnum(Enum):
    Const = 'const'
    Term = 'term'


class CurveTypeEnum(Enum):
    Const = 'const'
    Term = 'term'


class OptionTypeEnum(Enum):
    Call = "Call"
    Put = "Put"
