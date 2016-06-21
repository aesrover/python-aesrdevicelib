# Link to datasheet of sensor: https://cdn.sparkfun.com/datasheets/Sensors/Weather/ms5803_14ba.pdf
# Link to original source (contains some errors that were fixed in this version): 
#            https://github.com/ControlEverythingCommunity/MS5803-14BA/blob/master/Python/MS5803_14BA.py  

from . import sensor
import time 

class MS5803(sensor.Sensor):
    '''Library for the SparkFun MS5803-12BA Pressure Sensor'''
    
    _DEFAULT_I2C_ADDRESS = 0x76
    
    _REG_START_WRITE = 81    # Register address to take a measurement
    _REG_START_MEASURE = 0   # Register address to read back measurement
    
    def __init__(self, i2cAddress= _DEFAULT_I2C_ADDRESS, *args, **kwargs):
        super(MS5803, self).__init__(i2cAddress, *args, **kwargs)
        
        # MS5803_14BA address, 0x76(118)
        # 0x1E(30)	Reset command
        self.bus.write_byte(i2cAddress, 0x1E) 
    
    # Read function, returns a dictionary of the pressure and temperature values      
    def read(self):
        
        # Read 12 bytes of calibration data
        # Read pressure sensitivity
        data = self.bus.read_i2c_block_data(self.i2cAddress, 0xA2, 2)
        C1 = (data[0] << 8) + data[1]
        
        # Read pressure offset
        data = self.bus.read_i2c_block_data(self.i2cAddress, 0xA4, 2)
        C2 = (data[0] << 8) + data[1]
        
        # Read temperature coefficient of pressure sensitivity
        data = self.bus.read_i2c_block_data(self.i2cAddress, 0xA6, 2)
        C3 = (data[0] << 8) + data[1]
        
        # Read temperature coefficient of pressure offset
        data = self.bus.read_i2c_block_data(self.i2cAddress, 0xA8, 2)
        C4 = (data[0] << 8) + data[1]
        
        # Read reference temperature
        data = self.bus.read_i2c_block_data(self.i2cAddress, 0xAA, 2)
        C5 = (data[0] << 8) + data[1]
        
        # Read temperature coefficient of the temperature
        data = self.bus.read_i2c_block_data(self.i2cAddress, 0xAC, 2)
        C6 = (data[0] << 8) + data[1]
        
        # MS5803_14BA address, 0x76(118)
        # 0x40(64)	Pressure conversion(OSR = 256) command
        self.bus.write_byte(self.i2cAddress, 0x40)
        
        time.sleep(0.5)
        
        # Read digital pressure value
        # Read data back from 0x00(0), 3 bytes
        # D1 MSB2, D1 MSB1, D1 LSB
        value = self.bus.read_i2c_block_data(self.i2cAddress, 0x00, 3)
        D1 = (value[0] << 16)  + (value[1] << 8) + value[2]
        
        # MS5803_14BA address, i2cAddress(118)
        #		0x50(64)	Temperature conversion(OSR = 256) command
        self.bus.write_byte(self.i2cAddress, 0x50)
        
        time.sleep(0.5)
        
        # Read digital temperature value
        # Read data back from 0x00(0), 3 bytes
        # D2 MSB2, D2 MSB1, D2 LSB
        value = self.bus.read_i2c_block_data(self.i2cAddress, 0x00, 3)
        D2 = (value[0] << 16)  + (value[1] << 8) + value[2]
        
        dT = D2 - C5 * (2**8)
        TEMP = 2000 + dT * C6 / (2**23)
        OFF = C2 * (2**16) + (C4 * dT) / (2**7)
        SENS = C1 * (2**15) + (C3 * dT ) / (2**8)
        T2 = 0
        OFF2 = 0
        SENS2 = 0
        
        if TEMP > 2000:
            T2 = 7 * (dT * dT)/ (2**37)
            OFF2 = ((TEMP - 2000)**2) / (2**4)
            SENS2= 0
        elif TEMP < 2000:
            T2 = 3 * (dT ** 2) / (2**33)
            OFF2 = 3 * ((TEMP - 2000) ** 2) / 2
            SENS2 = 5 * ((TEMP - 2000) ** 2) / (2**3)
            if TEMP < -1500:
                OFF2 = OFF2 + 7 * ((TEMP + 1500) ** 2)
                SENS2 = SENS2 + 4 * ((TEMP + 1500) ** 2)
        
        TEMP = TEMP - T2
        OFF = OFF - OFF2
        SENS = SENS - SENS2
        pressure = ((((D1 * SENS) / (2**21)) - OFF) / (2**15)) / 10.0
        cTemp = TEMP / 100.0
                
        # return values in a dictionary
        return {"mbar": pressure, "temp": cTemp, "tempunit": "degC"}
