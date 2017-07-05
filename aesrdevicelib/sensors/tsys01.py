from . import i2c_device
import time

class TSYS01(i2c_device.I2cDevice):
    '''Library for the Blue Robotics TSYSO1 Fast-Response Temperature Sensor'''
    
    _DEFAULT_I2C_ADDRESS = 0x77          # CSB = 0 (GND)
    
    RESET                = 0x1E
    PROM_READ            = 0xA0
    ADC_READ             = 0x00
    ACD_TEMP_CONV        = 0x48
    
    # Calibration Parameters
    # C[0] = k0       address = 0xAA
    # C[1] = k1       address = 0xA8
    # C[2] = k2       address = 0xA6
    # C[3] = k3       address = 0xA4
    # C[4] = k4       address = 0xA2
    C = []
        
    def __init__(self, i2cAddress= _DEFAULT_I2C_ADDRESS, *args, **kwargs):
        super(TSYS01, self).__init__(i2cAddress, *args, **kwargs)
        
        # --- Reset Sequence ---
        # TSYS01 address, 0x77(119)
        # 0x1E(30)	Reset command
        self.write_byte(self.RESET)
        
        time.sleep(0.01)
        
        # --- Prom Read Sequence ---
        for i in range(5):            
            data = self.read_i2c_block_data(self.PROM_READ+(10-i*2), 2)
            self.C.append((data[0] << 8) + data[1])
            
    def read(self):
        
        self.write_byte(self.ACD_TEMP_CONV)
        
        time.sleep(0.01)
        
        data = self.read_i2c_block_data(self.ADC_READ, 3)
        D1 = (data[0] << 16) + (data[1] << 8) + data[2]
        
        TEMP = self.calculate(D1)
        
        return TEMP
        
    def calculate(self, adc24):
        adc16 = adc24/256
        
        TEMP = ( (-2) * self.C[4] * (10 ** -21) * (adc16 ** 4) + 
                    4 * self.C[3] * (10 ** -16) * (adc16 ** 3) +
                 (-2) * self.C[2] * (10 ** -11) * (adc16 ** 2) + 
                    1 * self.C[1] * (10 ** -6)  * (adc16 ** 1) +
               (-1.5) * self.C[0] * (10 ** -2) )
               
        return TEMP
