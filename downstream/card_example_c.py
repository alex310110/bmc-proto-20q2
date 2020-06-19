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
        self.temp_device = I2CHwmonDevice(
            'temp_sensor', mux.get_channels()[0], 0x30, 'xam3170')

        self.sensor_board_1 = Sensor('board_pos_1', 'temperature')
        self.sensor_board_2 = Sensor('board_pos_2', 'temperature')
        self.sensor_asic = Sensor('asic', 'temperature')
        self.sensors += [self.sensor_board_1, self.sensor_board_2, self.sensor_asic]

    def update_sensors(self):
        self.sensor_board_1.value = self.temp_device.get_reading('temp2')
        self.sensor_board_2.value = self.temp_device.get_reading('temp3')
        self.sensor_asic.value = self.temp_device.get_reading('temp4')
