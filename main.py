#!/usr/bin/python3

import downstream
import inspect
import os
from topology_entry import TopologyEntry


class BmcMain:
    def __init__(self):
        self.topology_entry_list = []
        self.entity_list = []

        for _, downstream_class in inspect.getmembers(downstream, inspect.isclass):
            if issubclass(downstream_class, TopologyEntry):
                topology_entry = downstream_class(self.entity_list)
                self.topology_entry_list.append(topology_entry)

        print('\nList of entities:')
        print('\n'.join([str(e) for e in self.entity_list]))
        print()

    def sensor_console(self):
        print("Ctrl-C to exit, Enter to refresh sensor readings")
        while True:
            for e in self.entity_list:
                e.update_sensors()

            break
            # input()


if __name__ == '__main__':
    bmc = BmcMain()
    bmc.sensor_console()
