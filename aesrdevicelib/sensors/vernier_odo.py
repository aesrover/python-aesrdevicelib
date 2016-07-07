from . import ads1115


class VernierODO(ads1115.ADS1115):
    def __init__(self, *args, **kwargs):
        super(VernierODO, self).__init__(*args, **kwargs)

    def convertMGL(self, adc):
        c = adc * (5/26665.8528646)  # Converts to a 0-5V range
        output = (c * 4.444) - .4444  # Converts to mg/L based of Vernier's scale
        return output

    def read(self):
        adc = super(VernierODO, self).read()
        oxygenLevel = self.convertMGL(adc)
        return {'rawADC': adc, 'mgL': oxygenLevel}
