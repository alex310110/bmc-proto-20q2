""" Abstract classes for I2C
"""

import random

# Mock bus number iterator
highest_i2c_bus = 7
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
        print('  Init I2C device %s type %s at bus %d addr 0x%02x' %
              (name, device, bus, addr))

    def delete(self):
        """ For various reasons, you may want to remove the driver...
            This can be implemented by:
            # echo ${addr} > /sys/bus/i2c/devices/i2c-${bus}/delete_device
        """
        print('  Remove I2C device %s type %s at bus %d addr 0x%02x' %
              (self.name, self.device, self.bus, self.addr))

    def transfer(self, write_bytes, read_byte_num):
        """ Interact with I2C interface directly.
            This assumes the BMC app is the only one initiates any I2C
            interactions, or there may be a race in I2C transactions.
        """
        print('  i2ctransfer -f -y %d w%d@0x%02x %s r%d' %
            (self.bus, len(write_bytes), self.addr, str(write_bytes), read_byte_num))


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

        if device == 'apc9456':
            num_of_channels = 4
        elif device == 'apc9457':
            num_of_channels = 8
        else:
            num_of_channels = 2

        highest_i2c_bus = channel_0_bus + num_of_channels - 1
        self.channels = list(
            range(channel_0_bus, channel_0_bus + num_of_channels))
        print('  I2C MUX created logical buses', self.channels)

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
        print('  Created hwmon directory hwmon%d' % self.hwmon_num)

    def get_reading(self, label):
        """ Mocks hwmon readings
        """
        if label.startswith('temp'):
            return round(random.uniform(25, 40), 2)
        elif label.startswith('curr') or label.startswith('iout'):
            return round(random.uniform(4, 8), 2)
        elif label.startswith('power'):
            return round(random.uniform(20, 60), 2)
        elif label.startswith('in') or label.startswith('vout'):
            if '12v' in self.name:
                return round(random.uniform(12, 13), 2)
            else:
                return round(random.uniform(0.6, 0.9), 2)

    def set_attribute(self, label, value):
        """ Set an attribute in hwmon interface
        """
        print('  Set hwmon%d attr %s to %d' % (self.hwmon_num, label, value))


class I2CEeprom(I2CDevice):
    def __init__(self, name, bus, addr, device):
        """ An I2C EEPROM device
        """
        I2CDevice.__init__(self, name, bus, addr, device)

    def get_content(self):
        """ Mocks EEPROM content for hardware recognition
        """
        if self.addr == 0x52:
            remainder = self.bus % 4
            return ['card_g', 'card_v', '', ''][remainder]
        elif self.addr == 0x54:
            return 'card_c'
        elif self.addr == 0x40:
            return 'board_a'
        return ''
