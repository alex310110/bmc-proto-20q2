#!/usr/bin/python3
""" This is the main entry of this demo prototype.
"""

import downstream
import inspect
import os
from topology_entry import TopologyEntry


class BmcMain:
    """ The main class of this prototype.
        Act as BMC software core and provide logics for demo.
    """

    def __init__(self):
        """ BMC software core initialization
        """
        # topology_entry_list tracks the roots of the hardware topology discoveries.
        self.topology_entry_list = []
        # entity_list tracks the entities discovered.
        self.entity_list = []

        # Scan for any classes stored in folder 'downstream' which are
        # identified as a TopologyEntry. Then perform topology discovery based
        # on these entires.
        for _, downstream_class in inspect.getmembers(downstream, inspect.isclass):
            if issubclass(downstream_class, TopologyEntry):
                topology_entry = downstream_class(self.entity_list)
                self.topology_entry_list.append(topology_entry)

        # Print discovered entities for this demo
        print('\nList of entities:')
        print('\n'.join([str(e) for e in self.entity_list]))
        print()

    def sensor_console(self):
        """ The sensor polling should be implemented as a service thread,
            but I simplify things here as a demo, where the protocol layer also
            initiates the sensor polling.
        """
        print("Host powering up")
        for e in self.entity_list:
            e.on_host_event('on')

        print("\nCtrl-C to exit, Enter to refresh sensor readings")
        while True:
            print()

            # Poll all the sensors in all entities identified.
            for e in self.entity_list:
                e.update_sensors()

            # read all the sensors
            for e in self.entity_list:
                for sensor in e.get_sensors():
                    print(e.name, sensor.get_reading_for_console())

            break
            # input()


if __name__ == '__main__':
    bmc = BmcMain()
    bmc.sensor_console()
