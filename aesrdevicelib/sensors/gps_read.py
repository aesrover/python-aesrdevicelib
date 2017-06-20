from gps3 import agps3
import threading
import time


class GPSRead:
    _VALID_READ_TIME = 3
    
    locationData = None
    timeOfRead = None
    
    def __init__(self, *args, **kwargs):
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
    
    def readLocationData(self):
        if self.locationData is None:
            raise ValueError("No successful reads")
        if time.time() - self.timeOfRead > self._VALID_READ_TIME:
            raise ValueError("No recent reads")
        return self.locationData
