# Type Hints:
from typing import Tuple

# Local:
from .transducer import Transducer


class PositionTransducer(Transducer):
    def __init__(self, atype, itype=None, **other):
        super().__init__(atype, itype=itype, **other)

    def read(self):
        raise NotImplementedError

    def diff_scale(self, x1, y1, x2, y2):
        return x1-x2, y1-y2

    def scale(self, x, y):
        return self.diff_scale(x, y, 0, 0)

    def read_xy_pos(self) -> Tuple[float, float]:
        raise NotImplementedError

    def read_xy_diff_scaled(self, dx, dy):
        return self.diff_scale(*self.read_xy_pos(), dx, dy)


class HeadingTransducer(Transducer):
    def __init__(self, atype, itype=None, **other):
        super().__init__(atype, itype=itype, **other)

    def read(self):
        raise NotImplementedError

    def read_heading(self) -> float:
        raise NotImplementedError
