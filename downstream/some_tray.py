from .board_example_a import BoardExampleA
from topology_entry import TopologyEntry


class SomeTray(TopologyEntry):
    def __init__(self, entity_list):
        print("Initializing SomeTray")
        self.children = []
        self.children.append(BoardExampleA(entity_list))
