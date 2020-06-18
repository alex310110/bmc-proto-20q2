class BmcEntity:
    def __init__(self, entity_list, name):
        print("Initializing %s" % name)
        entity_list.append(self)
        self.name = name
        self.children = []
        self.sensors = []

    def __str__(self):
        return self.name

    def get_sensors(self):
        return self.sensors

    def update_sensors(self):
        pass