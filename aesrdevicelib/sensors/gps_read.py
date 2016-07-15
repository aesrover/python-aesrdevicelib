import gps
import threading
import time


class GPSRead:
    _VALID_READ_TIME = 3
    
    locationData = None
    timeOfRead = None
    
    def __init__(self, *args, **kwargs):
        # Listen on port 2947 (gpsd) of localhost
        self.session = gps.gps(*args, **kwargs)
        self.session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
        
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = False
        self.running = True
        
        self.thread.start()
    
    def run(self):
        while self.running:
            try:
                report = self.session.next()
                # Wait for a 'TPV' report and display the current time
                #  To see all report data, uncomment the line below
                #  print report
                if report['class'] == 'TPV':
                    if hasattr(report, 'lat'):
                        self.locationData = {"lat": report.lat, "lon": report.lon}
                        self.timeOfRead = time.time()
            except KeyError:
                pass
            except StopIteration:
                self.session = None
                print("GPSD has terminated")

    def close(self):
        self.running = False
        self.thread.join()
    
    def readLocationData(self):
        if self.locationData is None:
            raise ValueError("No successful reads")
        if time.time() - self.timeOfRead > self._VALID_READ_TIME:
            raise ValueError("No recent reads")
        return self.locationData
