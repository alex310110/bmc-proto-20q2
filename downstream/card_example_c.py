""" An example PCIe card populated on a board
    with its EEPROM behind channel 2 of its I2C MUX.
"""

from entity import BmcEntity
from sensor import Sensor
from i2c import I2CHwmonDevice


class CardExampleC(BmcEntity):
    def __init__(self, entity_list, index, i2c_bus, mux):
        BmcEntity.__init__(self, 'card_c_%d' % index, entity_list)

        self.index = index
        self.i2c_bus = i2c_bus
        self.i2c_mux = mux

    def update_sensors(self):
        pass
