""" The abstract class for BMC entities
"""

class BmcEntity:
    def __init__(self, name, entity_list):
        """ Entity initialization
        """
        print("Initializing %s" % name)
        entity_list.append(self)
        self.name = name
        self.children = []
        self.devices = []
        self.sensors = []

    def __str__(self):
        return self.name

    def get_sensors(self):
        """ Returns a list of entity's sensors.
        """
        return self.sensors

    def update_sensors(self):
        """ Telling the entity to update its sensor readings.
        """
        pass
