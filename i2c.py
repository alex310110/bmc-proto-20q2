""" Abstract classes for I2C
"""

import random

# Mock bus number iterator
highest_i2c_bus = 8
highest_hwmon_num = -1


class I2CDevice:
    def __init__(self, name, bus, addr, device):
        """ 'bus' here is the logical bus number provided by Linux kernel.
        """
        self.name = name
        self.bus = bus
        self.addr = addr
        self.device = device

        # Apply I2C driver to sysfs
        # echo ${device_name} ${addr} > /sys/bus/i2c/devices/i2c-${bus}/new_device
        print("  Init I2C device %s type %s at bus %d addr 0x%02x" %
              (name, device, bus, addr))


class I2CMux(I2CDevice):
    def __init__(self, name, bus, addr, device):
        """ An I2C MUX
        """
        I2CDevice.__init__(self, name, bus, addr, device)

        # After applying the MUX driver, by looking at which bus channel-? is
        # linked to in sysfs, we get the logical bus number of MUX channels.
        # Assign mock numbers here:
        global highest_i2c_bus
        channel_0_bus = highest_i2c_bus + 1

        if device == 'pca9546':
            num_of_channels = 4
        elif device == 'pca9547':
            num_of_channels = 8
        else:
            num_of_channels = 2

        highest_i2c_bus = channel_0_bus + num_of_channels - 1
        self.channels = list(
            range(channel_0_bus, channel_0_bus + num_of_channels))
        print("  I2C MUX created logical buses", self.channels)

    def get_channels(self):
        """ Returns the logical bus numbers of MUX channels
        """
        return self.channels


class I2CHwmonDevice(I2CDevice):
    def __init__(self, name, bus, addr, device):
        """ An I2C sysfs hwmon device
        """
        I2CDevice.__init__(self, name, bus, addr, device)

        # After applying the device driver, by looking inside the hwmon
        # directory, we can get the hwmon directory number.
        # Assign mock numbers here:
        global highest_hwmon_num
        self.hwmon_num = highest_hwmon_num + 1
        highest_hwmon_num = self.hwmon_num
        print("  Created hwmon directory hwmon%d" % self.hwmon_num)

    def get_reading_from_label(self, label):
        """ Mocks hwmon readings
        """
        if label.startswith('temp'):
            return round(random.uniform(25, 40), 2)
        elif label.startswith('curr'):
            return round(random.uniform(4, 8), 2)
        elif label.startswith('power'):
            return round(random.uniform(20, 60), 2)
        elif label.startswith('in'):
            if '12v' in self.name:
                return round(random.uniform(12, 13), 2)
            else:
                return round(random.uniform(0.6, 0.9), 2)
