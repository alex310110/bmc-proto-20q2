""" The abstract class for BMC entities
"""

from i2c import I2CHwmonDevice
from sensor import Sensor


class BmcEntity:
    def __init__(self, name, entity_list):
        """ Entity initialization
        """
        print("Initializing %s" % name)
        entity_list.append(self)
        self.name = name
        self.children = []
        self.sensors = []

    def __str__(self):
        return self.name

    def on_host_event(self, event):
        """ Called when the host/main 12V rail has an event
        """
        pass

    def get_sensors(self):
        """ Returns entity's sensors.
        """
        return self.sensors

    def update_sensors(self):
        """ Telling the entity to update its sensor readings.
        """
        pass


class ConfigBasedEntity(BmcEntity):
    """ A simple example to make this demo backward-compatible to the existing
        JSON-based config in some way...
    """

    def __init__(self, entity_list, bus, config):
        # parse name
        def eval_var(s):
            if s[0] == '$':
                s = eval(s.replace('$bus', str(bus)))
            return s

        def eval_name(s):
            return '_'.join(map(str, map(eval_var, s.split())))

        name = eval_name(config['name'])
        BmcEntity.__init__(self, name, entity_list)

        # parse sensors
        self.devices = []
        for device_cfg in config['devices']:
            device = I2CHwmonDevice('', eval_var(device_cfg['bus']),
                                    device_cfg['addr'], device_cfg['type'])

            # attach a hwmon entry to sensor mapping to the device
            hwmon_map = dict()
            for label, name in device_cfg['hwmon'].items():
                # use temp for example only
                sensor = Sensor(eval_name(name), 'temperature')
                hwmon_map[label] = sensor
                self.sensors.append(sensor)

            device.hwmon_map = hwmon_map
            self.devices.append(device)

    def update_sensors(self):
        for device in self.devices:
            for label, sensor in device.hwmon_map.items():
                sensor.value = device.get_reading(label)
