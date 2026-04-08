import random
import types
from .flag_manager import FlagManager
from .inventory_manager import InventoryManager
from .renderer import Renderer
from .input_handler import InputHandler

class Game: #Game object is used to create all other objects
    def __init__(self, name):
        self.name = name
        self.inventory = []
        self.flags = set()
        self.story_nodes = {} #all story_nodes
        self.counters = []
        self.start_node = None
        self.current_story_node = None
        self.flag_manager = FlagManager()
        self.renderer = Renderer()
        self.inventory_manager = InventoryManager()
        self.input_handler = InputHandler()
        
    #advance story
    def change_node(self, node):
        if self.current_story_node:
            self.flag_manager.set_flag(self.flags, node.name) #set flag that the node has been visited
        self.current_story_node = node
        self.update_counters()
            
     #call this fucntion to reset the game      
    def new_game(self):
        self.change_story_node(self.start_story_node)
        self.inventory.clear()
        self.flags.clear()
        
        #reset story_nodes
        for story_node in self.story_nodes.values():
            story_node.reset()

    #-----------validate-----------------
    
    def validate(self, start):
        all_story_nodes = self.story_nodes.values()
        self.start_story_node = _get_story_node(self, start)
        self.change_story_node(self.start_story_node) #set start node as current_story_node

        for story_node in all_story_nodes:
            if story_node.default_next_node:
                story_node.default_next_node = _get_story_node(self, story_node.default_next_node)
        
            for next_node in story_node.next_nodes:
                next_node["node"] = _get_story_node(self, next_node["node"])
                
            for choice in story_node.choices:
                choice.targets = [
                    _get_story_node(self, target)
                    for target in choice.targets
                ]
