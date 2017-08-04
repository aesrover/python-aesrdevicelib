from .ads1x15 import ADS1115


class VoltageMonitorADS1115(ADS1115):
    def __init__(self, diff, *args, resistor_p=None, resistor_n=None, adc_gain=1, adc_data_rate=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.gain = (4.096/adc_gain)/(pow(2, 15)-1)
        if resistor_n is not None and resistor_p is not None:
            self.gain *= (resistor_p+resistor_n)/resistor_n

        self.start_adc_difference(diff, adc_gain, adc_data_rate)

    def read_voltage(self):
        return self.get_last_result() * self.gain

    def close(self):
        self.stop_adc()
