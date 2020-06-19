""" An example PCIe card populated on a board.
"""

from entity import BmcEntity
from i2c import I2CMux, I2CHwmonDevice


class CardExampleA(BmcEntity):
    def __init__(self, entity_list, index, i2c_bus):
        BmcEntity.__init__(self, 'card_a_%d' % index, entity_list)

        self.index = index
        self.i2c_bus = i2c_bus

        # init MUX
        self.i2c_mux = I2CMux('card_a_mux', i2c_bus, 0x71, 'pca9547')
        self.i2c_children = self.i2c_mux.get_channels()

        # init devices
        self.pcie_12v = I2CHwmonDevice('pcie_12v', i2c_bus, 0x20, 'ina230')
        self.devices.append(self.pcie_12v)

        self.asic = []
        for i in range(2):
            self.asic.append(
                I2CHwmonDevice('asic_%d' % i, self.i2c_children[i], 0x10 + i, 'asiccodename'))
        self.devices += self.asic

        self.vr = I2CHwmonDevice('vdd_0r80', self.i2c_children[7], 0x56, 'max20730')
        self.devices.append(self.vr)
