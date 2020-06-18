class BmcEntity:
    def __init__(self, entity_list, name):
        entity_list.append(self)
        self.name = name
        self.children = []

    def __str__(self):
        return self.name
