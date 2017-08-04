import smbus


class I2cDevice(object):
    # Add i2cAddress to parent class calls
    def __getattr__(self, name):
        # Get attribute (first from the base class, then the current class if
        #   it fails)
        from_bus = False
        try:
            attr = getattr(self.bus, name)
            if name.startswith('__'):
                raise AttributeError
            from_bus = True
        except AttributeError:
            text_class = self.__class__
            raise AttributeError("{}.{} object has no attribute '{}'"
                                 .format(text_class.__module__,
                                         text_class.__name__, name))

        # Return a modified function if the attribute is a function:
        if hasattr(attr, '__call__'):
            def newfunc(*args, **kwargs):
                if from_bus:
                    result = attr(self.i2cAddress, *args, **kwargs)

                else:
                    result = attr(*args, **kwargs)
                return result

            # Return a function or the original attribute depending on what
            #   type the requested attribute was
            return newfunc
        else:
            return attr

    def __init__(self, i2cAddress, bus=1, test_device=True):
        self.bus = smbus.SMBus(bus)
        self.i2cAddress = i2cAddress

        # Test if device is connected by transmitting just the slave address
        # and checking for an ACK from the device:
        if test_device:
            self.bus.write_quick(i2cAddress)

    def read_word_data(self, cmd, little_endian=True, signed=False):
        d = self.bus.read_word_data(self.i2cAddress, cmd)

        if not little_endian:  # If not little endian, flip the bytes
            d = ((d & (0xff << 8)) >> 8) + ((d & 0xff) << 8)  # Flip byte order
        if signed:  # Convert to signed int, if required
            if d > 2**15-1:
                d -= 2**16
        return d

    def read_byte_data(self, cmd, signed=False):
        d = self.bus.read_byte_data(self.i2cAddress, cmd)

        if signed:
            if d > 2**7-1:
                d -= 2**8
        return d
