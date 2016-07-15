from . import ads1115


class VernierODO(ads1115.ADS1115):
    def __init__(self, *args, **kwargs):
        super(VernierODO, self).__init__(*args, **kwargs)

    def convertMGL(self, adc):
        c = 6.144 * adc / (pow(2, 15) - 1)  # Converts to a voltage
        output = (c * 4.444) - .4444  # Converts to mg/L based of Vernier's scale
        return output

    def read(self):
        adc = super(VernierODO, self).read()
        oxygenLevel = self.convertMGL(adc)
        return {'rawADC': adc, 'mgL': oxygenLevel}
