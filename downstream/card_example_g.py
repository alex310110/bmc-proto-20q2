""" An example PCIe card populated on a board.
"""

from .device_xam2730 import XAM2730
from entity import BmcEntity
from sensor import Sensor
from i2c import I2CMux, I2CHwmonDevice


class CardExampleG(BmcEntity):
    """ When translating to C/C++ source code, we may declare the device
        variables like self.pcie_12v, self.vr, self.asic and sensor variables
        in the header file. Then it would be very clear that what entity
        children, devices and sensors the entity has.
    """

    def __init__(self, entity_list, index, i2c_bus):
        BmcEntity.__init__(self, 'card_g_%d' % index, entity_list)

        self.index = index
        self.i2c_bus = i2c_bus
        self.sensor_map = dict()

        # init MUX
        self.i2c_mux = I2CMux('card_g_mux', i2c_bus, 0x71, 'apc9457')
        self.i2c_children = self.i2c_mux.get_channels()

        # init devices
        self.pcie_12v = I2CHwmonDevice('pcie_12v', i2c_bus, 0x20, 'ain203')
        # example of writing hwmon attribute
        self.pcie_12v.set_attribute('shunt_resistor', 2000)

        self.asic = []
        for i in range(2):
            self.asic.append(
                I2CHwmonDevice('asic_%d' % i, self.i2c_children[i], 0x10 + i, 'asic-i2c-drv'))

        self.vr = XAM2730('vdd_0r80', self.i2c_children[7], 0x56)

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
            self.sensor_map[name + '_' + sensor_property] = sensor
            self.sensors.append(sensor)

    def on_host_event(self, event):
        if event not in ['on', 'reset']:
            return
        # example of setting VR voltage output
        self.vr.transfer([0x21, 0x95, 0x01], 0)

    def update_sensors(self):
        self.sensor_map['pcie_12v_voltage'].value = self.pcie_12v.get_reading('in1')
        self.sensor_map['pcie_12v_current'].value = self.pcie_12v.get_reading('curr1')
        self.sensor_map['pcie_12v_power'].value = self.pcie_12v.get_reading('power1')

        # example of sensor aggregation
        self.sensor_map['asic_package_temperature'].value = \
            max(self.asic[0].get_reading('temp1'),
                self.asic[1].get_reading('temp1'))

        self.sensor_map['vdd_0r80_temperature'].value = self.vr.get_reading('temp1')
        self.sensor_map['vdd_0r80_voltage'].value = self.vr.get_reading('vout2')
        self.sensor_map['vdd_0r80_current'].value = self.vr.get_reading('iout2')
