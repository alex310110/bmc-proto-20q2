""" An example board in a tray
"""

from .card_example_c import CardExampleC
from .card_example_g import CardExampleG
from .card_example_v import CardExampleV
from device_xam2734 import XAM2734
from entity import BmcEntity
from i2c import I2CMux, I2CHwmonDevice, I2CEeprom
from sensor import Sensor


class BoardExampleA(BmcEntity):
    def __init__(self, entity_list):
        BmcEntity.__init__(self, 'board_a', entity_list)

        self.eeprom = I2CEeprom('board_eeprom', 2, 0x40, 'eeprom16bit')
        print(' ', self.name, 'has EEPROM content:', self.eeprom.get_content())

        # init MUXes
        self.i2c_mux = []
        self.i2c_mux.append(I2CMux('pcie_i2c_mux_0', 6, 0x70, 'apc9456'))
        self.i2c_mux.append(I2CMux('pcie_i2c_mux_1', 7, 0x70, 'apc9456'))
        i2c_children = self.i2c_mux[0].get_channels() + \
            self.i2c_mux[1].get_channels()

        self.vr = XAM2734('vdd_0r70', 2, 0x58)
        self.sensor_vr_voltage = Sensor('vdd_0r70', 'voltage')
        self.sensors.append(self.sensor_vr_voltage)
        self.sensor_vr_current = Sensor('vdd_0r70', 'current')
        self.sensors.append(self.sensor_vr_current)

        # init PCIe cards
        for i in range(8):

            eeprom = I2CEeprom('possible_eeprom', i2c_children[i], 0x52,
                               'eeprom8bit')
            if eeprom.get_content() == 'card_g':
                card_g = CardExampleG(entity_list, i, i2c_children[i])
                card_g.eeprom = eeprom
                self.children.append(card_g)
                continue

            elif eeprom.get_content() == 'card_v':
                card_v = CardExampleV(entity_list, i, i2c_children[i])
                card_v.eeprom = eeprom
                self.children.append(card_v)
                continue

            eeprom.delete()
            # The other supported card may have its eeprom behind the channel 2
            # of its I2C MUX. Try applying MUX first, if it is the card,
            # hand over the MUX to the card.
            card_c_mux = I2CMux('possible_card_c_mux', i2c_children[i], 0x71,
                                'apc9456')
            eeprom = I2CEeprom('possible_eeprom', card_c_mux.get_channels()[2],
                               0x54, 'eeprom8bit')
            if eeprom.get_content() == 'card_c':
                card_c = CardExampleC(entity_list, i,
                                      i2c_children[i], card_c_mux)
                card_c.eeprom = eeprom
                self.children.append(card_c)
                continue

            # no valid card recognized
            print("No card detected at slot %d" % i)
            eeprom.delete()
            card_c_mux.delete()


    def update_sensors(self):
        self.sensor_vr_voltage.value = self.vr.get_reading('vout2')
        self.sensor_vr_current.value = self.vr.get_reading('iout2')
