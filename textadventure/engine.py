from .flag_manager import FlagManager
from .inventory_manager import InventoryManager
from .renderer import Renderer
from .input_handler import InputHandler

class Game: #Game object is used to create all other objects
    def __init__(self, *, name, data):
        self.name = name
        self.inventory = []
        self.flags = set()
        self.nodes = data #get data from factory
        self.counters = []
        self.start_node = None
        self.current_node = None
        self.flag_manager = FlagManager()
        self.renderer = Renderer()
        self.inventory_manager = InventoryManager()
        self.input_handler = InputHandler()
        
    #Change current node
    def change_node(self, node):
        if self.current_node:
            self.flag_manager.set_flag(self.flags, node.name) #set flag that the node has been visited
        self.current_node = node
        self.update_counters()
            
     #call this fucntion to reset the game      
    def new_game(self):
        self.change_story_node(self.start_node)
        self.inventory.clear()
        self.flags.clear()
        
        #reset story_nodes
        for node in self.nodes.values():
            node.reset()