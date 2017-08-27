from .ads1x15 import ADS1115
from ..base.transducer import Transducer


class VoltageMonitor(Transducer):
    def __init__(self, itype=None, gain: float=1., resistor_p=None, resistor_n=None, **other_data):
        super().__init__("VOLT_MON", itype, **other_data)

        self.gain = gain
        if resistor_n is not None and resistor_p is not None:
            self.res_gain = (resistor_p+resistor_n)/resistor_n
        else:
            self.res_gain = 1

    def _convert(self, dir_volt):
        return dir_volt * self.gain * self.res_gain

    def _read_dir_voltage(self):
        raise NotImplementedError

    def read_voltage(self):
        return self._convert(self._read_dir_voltage())

    def read(self):
        r = self._read_dir_voltage()
        return {'dir_volt': r, 'volt': self._convert(r)}


class VoltageMonitorADS1115(ADS1115, VoltageMonitor):
    def __init__(self, diff, *args, itype=None, other_data=None, resistor_p=None, resistor_n=None, adc_gain=1,
                 adc_data_rate=None, **kwargs):
        super().__init__(*args, **kwargs)
        if other_data is None:
            other_data = {}
        gain = (4.096 / adc_gain) / (pow(2, 15) - 1)
        VoltageMonitor.__init__(self, itype, gain, resistor_p=resistor_p, resistor_n=resistor_n, **other_data)

        self.start_adc_difference(diff, adc_gain, adc_data_rate)  # Start continuous adc conversion

    def _read_dir_voltage(self):
        return self.get_last_result()

    def close(self):
        self.stop_adc()
