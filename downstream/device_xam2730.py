""" An example wrapper class of proprietary device under NDA.
"""

from i2c import I2CHwmonDevice


class XAM2730(I2CHwmonDevice):
    """ Oops! Our vendor told us we need to calibrate the output current
        reading using temperature! However, this is not suitable to do in
        the kernel driver...
    """

    def __init__(self, name, bus, addr):
        I2CHwmonDevice.__init__(self, name, bus, addr, 'xam2730')

    def get_reading(self, label):
        reading = super().get_reading(label)
        if label != 'iout2':
            return reading

        # some sick mock...
        temp = super().get_reading('temp1')
        return round(reading + temp, 2)
