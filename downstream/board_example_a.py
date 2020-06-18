from entity import BmcEntity
from .card_example_a import CardExampleA


class BoardExampleA(BmcEntity):
    def __init__(self, entity_list):
        print("Initializing BoardExampleA")
        BmcEntity.__init__(self, entity_list, 'board_a')

        for i in range(10):
            self.children.append(CardExampleA(entity_list, i))
