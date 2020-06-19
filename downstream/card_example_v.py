""" An example PCIe card populated on a board.
"""

from entity import BmcEntity
from sensor import Sensor
from i2c import I2CHwmonDevice


class CardExampleV(BmcEntity):
    def __init__(self, entity_list, index, i2c_bus):
        BmcEntity.__init__(self, 'card_v_%d' % index, entity_list)

        self.index = index
        self.i2c_bus = i2c_bus

    def update_sensors(self):
        pass
