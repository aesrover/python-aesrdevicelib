from . import sensor
import time

class MS5837(sensor.Sensor): 
    '''Library for the Blue Robotics MS5837-30BA Pressure Sensor'''
    
    _DEFAULT_I2C_ADDRESS = 0x76
    
    C1 = 0          # Pressure sensitivy
    C2 = 0          # Pressure offset
    C3 = 0          # Temperature coefficient of pressure sensitivity
    C4 = 0          # Temperature coefficient of pressure offset
    C5 = 0          # Reference temperature
    C6 = 0          # Temperature coefficient of the temperature
    
    
    def __init__(self, i2cAddress= _DEFAULT_I2C_ADDRESS, *args, **kwargs):
        super(MS5837, self).__init__(i2cAddress, *args, **kwargs)
        
        # MS5837-30BA address, 0x76(118)
        # 0x1E(30)	Reset command
        self.bus.write_byte(i2cAddress, 0x1E) 
        
        # ---- Read 12 bytes of calibration data ----
        # Read pressure sensitivity
        data = self.bus.read_i2c_block_data(self.i2cAddress, 0xA2, 2)
        self.C1 = (data[0] << 8) + data[1]
        
        # Read pressure offset
        data = self.bus.read_i2c_block_data(self.i2cAddress, 0xA4, 2)
        self.C2 = (data[0] << 8) + data[1]
        
        # Read temperature coefficient of pressure sensitivity
        data = self.bus.read_i2c_block_data(self.i2cAddress, 0xA6, 2)
        self.C3 = (data[0] << 8) + data[1]
        
        # Read temperature coefficient of pressure offset
        data = self.bus.read_i2c_block_data(self.i2cAddress, 0xA8, 2)
        self.C4 = (data[0] << 8) + data[1]
        
        # Read reference temperature
        data = self.bus.read_i2c_block_data(self.i2cAddress, 0xAA, 2)
        self.C5 = (data[0] << 8) + data[1]
        
        # Read temperature coefficient of the temperature
        data = self.bus.read_i2c_block_data(self.i2cAddress, 0xAC, 2)
        self.C6 = (data[0] << 8) + data[1]
    
            
    # Read function, returns a dictionary of the pressure and temperature values      
    def read(self):
        
        #---- Read digital pressure and temperature data ----
        # MS5837-30BA address, 0x76(118)
        # 0x48(72)	Pressure conversion(OSR = 4096) command
        self.bus.write_byte(self.i2cAddress, 0x48)
        
        time.sleep(0.5)
        
        # Read digital pressure value
        # Read data back from 0x00(0), 3 bytes
        # D1 MSB2, D1 MSB1, D1 LSB
        value = self.bus.read_i2c_block_data(self.i2cAddress, 0x00, 3)
        D1 = (value[0] << 16)  + (value[1] << 8) + value[2]
        
        # MS5837-30BA address, i2cAddress(118)
        # 0x58(88)	Temperature conversion(OSR = 4096) command
        self.bus.write_byte(self.i2cAddress, 0x58)
        
        time.sleep(0.5)
        
        # Read digital temperature value
        # Read data back from 0x00(0), 3 bytes
        # D2 MSB2, D2 MSB1, D2 LSB
        value = self.bus.read_i2c_block_data(self.i2cAddress, 0x00, 3)
        D2 = (value[0] << 16)  + (value[1] << 8) + value[2]
        
        # ---- Calculate temperature ----
        dT = D2 - self.C5 * (2**8)
        TEMP = 2000 + dT * self.C6 / (2**23)
        
        # ---- Calculated temperature compensated pressure ----
        OFF = self.C2 * (2**16) + (self.C4 * dT) / (2**7)
        SENS = self.C1 * (2**15) + (self.C3 * dT ) / (2**8)
        
        # Temperature compensated pressure (not the most accurate)
        # Use the flowchart for optimum accuracy
        # Pressure: P = (D1 * SENS / ((2**21) - OFF)) / (2**13)
        
        
        # ---- Second order temperature compensation (flowchart)
        Ti = 0
        OFFi = 0
        SENSi = 0
        
        if ((TEMP/100) < 20):        # Low temperature
            Ti = 3 * (dT**2) / (2**33)
            OFFi = 3 * ((TEMP - 2000) ** 2) / 2
            SENSi = 5 * ((TEMP - 2000) ** 2) / (2**3)
            
            if (TEMP/100) < -15:    # Very Low Temperature
                OFFi = OFFi + 7 * ((TEMP + 1500)**2)
                SENSi = SENSi + 4 * ((TEMP + 1500)**2)
                
        else:                      # High Temperature
            Ti = 2 * (dT ** 2) / (2 ** 37)
            OFFi = ((TEMP - 2000)**2) / (2**4)
            
        # Calculated pressure and temperature 2nd Order    
        OFF2 = OFF - OFFi
        SENS2 = SENS - SENSi
        
        TEMP2 = (TEMP - Ti) / 100
        P2 = (((D1 * SENS2) / (2**21) - OFF2) / (2**31)) / 10
          
                
        # return values in a dictionary
        return {"mbar" : P2, "temp": TEMP2, "tempunit" : "degC"}
