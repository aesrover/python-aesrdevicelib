import smbus


class I2cDevice(object):
    # Add i2cAddress to parent class calls
    def __getattribute__(self, name):
        # Get attribute (first from the base class, then the current class if
        #   it fails)
        fromBus = False
        try:
            attr = object.__getattribute__(self, name)
        except AttributeError:
            try:
                attr = getattr(self.bus, name)
                fromBus = True
            except AttributeError:
                textClass = self.__class__
                raise AttributeError("{}.{} object has no attribute '{}'"
                                     .format(textClass.__module__,
                                             textClass.__name__, name))

        # Return a modified function if the attribute is a function:
        if hasattr(attr, '__call__'):
            def newfunc(*args, **kwargs):
                if fromBus and 'addr' in attr.__code__.co_varnames:
                    result = attr(*args, addr=self.i2cAddress, **kwargs)

                else:
                    result = attr(*args, **kwargs)
                return result

            # Return a function or the original attribute depending on what
            #   type the requested attribute was
            return newfunc
        else:
            return attr

    def __init__(self, i2cAddress, bus=1, testDevice=True):
        self.bus = smbus.SMBus(bus)
        self.i2cAddress = i2cAddress

        # Test if device is connected by transmitting just the slave address
        # and checking for an ACK from the device:
        if testDevice:
            self.bus.write_quick(i2cAddress)
