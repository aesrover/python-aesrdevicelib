import smbus


class I2cDevice(object):
    # Add i2cAddress to parent class calls
    def __getattribute__(self, name):
        # Get attribute (first from the base class, then the current class if
        #   it fails)
        from_bus = False
        try:
            attr = object.__getattribute__(self, name)
        except AttributeError:
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
