""" An example board in a tray
"""

from entity import BmcEntity
from i2c import I2CMux, I2CHwmonDevice
from .card_example_g import CardExampleG


class BoardExampleA(BmcEntity):
    def __init__(self, entity_list):
        BmcEntity.__init__(self, 'board_a', entity_list)

        # init MUXes
        self.i2c_mux = []
        self.i2c_mux.append(I2CMux('pcie_i2c_mux_0', 7, 0x70, 'apc9456'))
        self.i2c_mux.append(I2CMux('pcie_i2c_mux_1', 8, 0x70, 'apc9456'))
        self.devices += self.i2c_mux
        i2c_children = self.i2c_mux[0].get_channels() + \
            self.i2c_mux[1].get_channels()

        # init PCIe cards
        for i in range(8):
            self.children.append(
                CardExampleG(entity_list, i, i2c_children[i]))
