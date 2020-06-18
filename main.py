#!/usr/bin/python3

import downstream
import inspect
import os
from glob import glob
from topology_entry import TopologyEntry


class BmcMain:
    def __init__(self):
        super().__init__()
        for name, downstream_class in inspect.getmembers(downstream, inspect.isclass):
            if issubclass(downstream_class, TopologyEntry):
                downstream_class()


    def sensor_console(self):
        print("Ctrl-C to exit, Enter to refresh sensor readings")
        while True:
            input()


if __name__ == '__main__':
    bmc = BmcMain()
    bmc.sensor_console()
