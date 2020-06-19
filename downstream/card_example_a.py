""" An example PCIe card populated on a board.
"""

from entity import BmcEntity
from sensor import Sensor
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
        # example of writing hwmon attribute
        self.pcie_12v.set_attribute('shunt_resistor', 2000)
        self.devices.append(self.pcie_12v)

        self.asic = []
        for i in range(2):
            self.asic.append(
                I2CHwmonDevice('asic_%d' % i, self.i2c_children[i], 0x10 + i, 'asiccodename'))
        self.devices += self.asic

        self.vr = I2CHwmonDevice('vdd_0r80', self.i2c_children[7], 0x56, 'max20730')
        self.devices.append(self.vr)

        self._setup_sensors()

    def _setup_sensors(self):
        sensor_table = [
            ('pcie_12v', 'voltage'),
            ('pcie_12v', 'current'),
            ('pcie_12v', 'power'),
            ('asic_package', 'temperature'),
            ('vdd_0r80', 'temperature'),
            ('vdd_0r80', 'voltage'),
            ('vdd_0r80', 'current'),
        ]

        for name, sensor_property in sensor_table:
            sensor = Sensor(name, sensor_property)
            self.sensors[sensor.name] = sensor

    def update_sensors(self):
        self.sensors['pcie_12v_voltage'].value = self.pcie_12v.get_reading('in1')
        self.sensors['pcie_12v_current'].value = self.pcie_12v.get_reading('curr1')
        self.sensors['pcie_12v_power'].value = self.pcie_12v.get_reading('power1')

        # perform sensor aggregation
        self.sensors['asic_package_temperature'].value = \
            max(self.asic[0].get_reading('temp1'),
                self.asic[1].get_reading('temp1'))

        self.sensors['vdd_0r80_temperature'].value = self.vr.get_reading('temp1')
        self.sensors['vdd_0r80_voltage'].value = self.vr.get_reading('vout2')
        self.sensors['vdd_0r80_current'].value = self.vr.get_reading('iout2')
