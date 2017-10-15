import time
import math

from ..base.motor import Motor, ControlledMotor


class TimedControlledMotor(ControlledMotor):
    def __init__(self, m: Motor, def_p: float=1):
        """
        Initialize object.

        :arg m: Motor to control
        :arg def_p: The default power when moving motor by seconds
        """
        super().__init__()
        self.m = m
        self.def_p = def_p
        self.cutoff = True
        self.moving = False

    def _send_stop(self):
        self.cutoff = True

    def _set_motor_power(self, p: float):
        """ Direct set of motor power. """
        self.m._set_motor_power(p)

    def _move_tick(self, rel_t, p=None) -> float:
        """
        Move for t seconds, at power p.

        :arg rel_t: Number of seconds to move
        :arg p: Power to move motor at. Defaults to initialized default power (if None)
        """
        self.cutoff = False
        if p is None:
            p = self.def_p

        move_time = 0

        move_sign = math.copysign(1, rel_t)
        p *= move_sign
        try:
            self.m.set_power(p)

            ts = time.time()

            while move_time < abs(rel_t):
                move_time = time.time() - ts
                if self.cutoff:
                    break
                time.sleep(0.05)
        finally:
            self.m.set_power(0)

        return move_time * move_sign
