from abc import ABC, abstractmethod


class BaseInterp1d(ABC):
    def __init__(self, x: list, y: list):
        assert sorted(x) == x, "the x-axis must be sorted"
        self.__x = x
        self.__y = y

    @abstractmethod
    def interp(self, x_) -> float:
        raise NotImplemented
