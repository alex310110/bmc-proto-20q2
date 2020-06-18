from entity import BmcEntity


class CardExampleA(BmcEntity):
    def __init__(self, entity_list, index):
        BmcEntity.__init__(self, entity_list, 'card_a_%d' % index)

        self.index = index
