""" An example of entry for topology discovery. The __init__ may do nothing if
    this class is found to be not for the actual tray it's running. This
    creates opportunity for single BMC image supporting multiple platforms.
"""

from .board_example_a import BoardExampleA
from topology_entry import TopologyEntry


class SomeTray(TopologyEntry):
    def __init__(self, entity_list):
        print("Initializing SomeTray")
        self.children = []
        self.children.append(BoardExampleA(entity_list))
