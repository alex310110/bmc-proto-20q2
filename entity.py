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
        self.sensors = []

    def __str__(self):
        return self.name

    def on_host_event(self, event):
        """ Called when the host/main 12V rail has an event
        """
        for c in self.children:
            c.on_host_event(event)

    def get_sensors(self):
        """ Returns entity's sensors.
        """
        return self.sensors

    def update_sensors(self):
        """ Telling the entity to update its sensor readings.
        """
        pass
