from gps3 import agps3
import threading
import time
import math
import numpy as np

from typing import Tuple

from ..base.navigation import PositionTransducer


class GPSRead(PositionTransducer):
    _VALID_READ_TIME = 3
    
    locationData = None
    timeOfRead = None
    
    def __init__(self, itype=None, **other):
        super().__init__("GPS", itype=None, **other)
        # Setup gps connection and data stream:
        self.sock = agps3.GPSDSocket()
        self.stream = agps3.DataStream()
        self.sock.connect()
        self.sock.watch()

        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = False
        self.running = True
        
        self.thread.start()
    
    def run(self):
        while self.running:
            new_data = self.sock.__next__(1)
            if new_data:
                self.stream.unpack(new_data)
                self.locationData = {"lat": self.stream.lat, "lon": self.stream.lon}
                self.timeOfRead = time.time()

    def close(self):
        self.running = False
        self.thread.join()
        self.sock.close()

    def read(self):
        if self.locationData is None:
            raise ValueError("No successful reads")
        if time.time() - self.timeOfRead > self._VALID_READ_TIME:
            raise ValueError("No recent reads")
        return dict(self.locationData)

    def read_xy_pos(self) -> Tuple[float, float]:
        p = self.read()
        return p['lon'], p['lat']

    def diff_scale(self, x1, y1, x2, y2):
        return np.subtract((x1, y1), (x2, y2)) * np.array((math.cos(math.radians(y2)) * 111320., 110540.))

    def scale(self, x, y):
        return self.diff_scale(0, 0, -x, -y)
