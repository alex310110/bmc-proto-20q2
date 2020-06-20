""" An example PCIe card populated on a board, initialized with config file
"""

from entity import ConfigBasedEntity


class CardExampleV(ConfigBasedEntity):
    config = {
        'name': 'card v $bus-8',
        'devices': [
            {
                'addr': 0x10,
                'bus': '$bus',
                'hwmon': {
                    'temp1': "card v $bus-8 0 temp1",
                    "temp2": "card v $bus-8 0 temp2",
                },
                'type': 'tpm144',
            },
            {
                'addr': 0x20,
                'bus': '$bus',
                'hwmon': {
                    'temp1': "card v $bus-8 1 temp1",
                    "temp2": "card v $bus-8 1 temp2",
                },
                'type': 'tpm144',
            },
        ]
    }

    def __init__(self, entity_list, i2c_bus):
        ConfigBasedEntity.__init__(self, entity_list, i2c_bus, CardExampleV.config)
