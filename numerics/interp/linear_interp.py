from abc import ABC
from numerics.interp.base_interp import BaseInterp1d
import numpy as np


class LinearInterp1d(BaseInterp1d, ABC):
    def __init__(self, x: list, y: list, mode='flat', fill_value: tuple = None):
        super().__init__(x, y)
        if fill_value is None:
            fill_value = []
        self.mode = mode
        assert len(fill_value) <= 2, "invalid fill value input"
        self.fill_value = fill_value

        if self.mode == "flat":
            if self.fill_value is None or len(self.fill_value) == 0:
                self.left_fill_val = self._y_vals[0]
                self.right_fill_val = self._y_vals[-1]
            elif len(self.fill_value) == 1:
                self.left_fill_val = self.fill_value[0]
                self.right_fill_val = self.fill_value[0]
            else:
                self.left_fill_val, self.right_fill_val = self.fill_value
        else:
            raise NotImplemented

    def interp(self, x_) -> float:
        if x_ <= self._x_vals[0]:
            return self.left_fill_val
        elif x_ >= self._x_vals[-1]:
            return self.right_fill_val
        else:
            index = np.searchsorted(self._x_vals, x_)
            y_low = self._y_vals[index - 1]
            y_high = self._y_vals[index]
            x_low = self._x_vals[index - 1]
            x_high = self._x_vals[index]
            return y_low + (y_high - y_low) / (x_high - x_low) * (x_ - x_low)
