from typing import Tuple
from threading import Thread

import time


class Motor:
    def _set_motor_power(self, p: float):
        raise NotImplementedError

    def set_power(self, p: float):
        if abs(p) > 1:
            raise ValueError("Power value needs to be in range [-1,1].")
        return self._set_motor_power(p)


class Thruster(Motor):
    def __init__(self, v: Tuple[float, float], a: float):
        self.v = v
        self.a = a

    def _set_motor_power(self, p: float):
        raise NotImplementedError


class ControlledMotor(Motor, Thread):
    """ A motor capable of relative movement by tick number. """
    def __init__(self):
        self.curr_tick = 0
        self.curr_job = None
        self.moving = False

        Thread.__init__(self, target=self._move_thread)
        self.running = True
        self.start()

    def _move_thread(self):
        while self.running:
            if self.curr_job is not None:
                last_job = self.curr_job
                self.curr_tick += self._move_tick(*last_job)

                self.curr_job = None
                self.moving = False

    def _set_job(self, rel_t, p):
        # Stop any previous movements (will wait for moving to be set to false)
        self.stop()

        # NOTE: Will not be effected by the set of these variables in the thread, as moving == False is waited for
        self.moving = True
        self.curr_job = (rel_t, p)

        # Wait for the motor to start moving:
        while not self.is_moving():
            pass

    def stop(self):
        """ Stop the motor. """
        self._send_stop()

        # Hang until stopped moving:
        while self.is_moving():
            pass

    def close(self):
        self.running = False
        self.join()

    def _send_stop(self):
        """ Send stop to motor. """
        raise NotImplementedError

    def is_moving(self) -> bool:
        """ Returns bool to signal if motor is moving. """
        return self.moving

    def _move_tick(self, rel_t, p=None) -> float:
        """ Move by some number of ticks, at speed p. To be implemented by subclasses. """
        raise NotImplementedError

    def move_rel_tick(self, rel_t, p=None, t=False):
        """ Move rel_t ticks (relatively), at speed p. Use default p if not given. """
        if t:
            self._set_job(rel_t, p)
        else:
            self.moving = True
            self.curr_tick += self._move_tick(rel_t, p)
            self.moving = False

    def move_abs_tick(self, abs_t, p=None, t=False):
        """ Move to an absolute tick position, abs_t, at speed p. Use default p if not given. """
        rel_t = abs_t - self.curr_tick
        self.move_rel_tick(rel_t, p, t)

    def get_curr_tick(self):
        return self.curr_tick
