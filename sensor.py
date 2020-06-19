""" Abstract classes for sensors
"""


class Sensor:
    """ A baisc abstract for a sensor
    """
    type_to_unit = {
        'temperature': 'C',
        'voltage': 'V',
        'power': 'W',
        'current': 'A',
    }

    def __init__(self, name, sensor_property):
        self.property = sensor_property
        self.name = name + '_' + self.property
        self.value = 0
        self.unit = Sensor.type_to_unit[self.property]

    def get_reading_for_console(self):
        return ' '.join([self.name, str(self.value), self.unit])
