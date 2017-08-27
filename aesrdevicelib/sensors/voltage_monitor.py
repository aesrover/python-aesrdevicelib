from .ads1x15 import ADS1115
from ..base.transducer import Transducer


class VoltageMonitorADS1115(ADS1115, Transducer):
    def __init__(self, diff, *args, itype=None, other_data=None, resistor_p=None, resistor_n=None, adc_gain=1, adc_data_rate=None, **kwargs):
        super().__init__(*args, **kwargs)
        if other_data is None:
            other_data = {}
        Transducer.__init__(self, "PRES", itype, **other_data)

        self.gain = (4.096/adc_gain)/(pow(2, 15)-1)
        if resistor_n is not None and resistor_p is not None:
            self.gain *= (resistor_p+resistor_n)/resistor_n

        self.start_adc_difference(diff, adc_gain, adc_data_rate)  # Start continuous adc conversion

    def _convert(self, dir_volt):
        return dir_volt * self.gain

    def read_voltage(self):
        return self._convert(self.get_last_result())

    def read(self):
        r = self.get_last_result()
        return {'dir_volt': r, 'volt': self._convert(r)}

    def close(self):
        self.stop_adc()
