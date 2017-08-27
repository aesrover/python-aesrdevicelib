from .ads1115 import ADS1115


class VernierODO(ADS1115):
    def __init__(self, *args, **kwargs):
        super(VernierODO, self).__init__(*args, **kwargs)

    def convertMGL(self, adc):
        c = 6.144 * adc / (pow(2, 15) - 1)  # Converts to a voltage
        output = (c * 4.444) - .4444  # Converts to mg/L based of Vernier's scale
        return output

    def read(self):
        d = super().read()
        d['mgL'] = self.convertMGL(d['adc_val'])
        return d
