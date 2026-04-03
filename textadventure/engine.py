import random
import types

class Game: #Game object is used to create all other objects
    def __init__(self, name):
        self.name
        self.inventory = []
        self.flags = []
        self.story_nodes = {} #all story_nodes
        self.counters = []
        self.start_node = None
        self.current_node = None
        self.flag_manager = FlagManager()
        self.renderer = Renderer()
        self.inventory_manager = InventoryManager()
        
    def print_messages(self, counter, messages: list):
        if counter.count > len(messages) - 1:
            msg = messages[-1]
        else:
            msg = message[counter.count]
        self.current_story_node.set_post_message(msg) 
        
    def get_inventory(self):
        return {str(index) : element for (index, element) in enumerate(self.inventory, start=1)}
        
    def get_choices(self):
        choices = self.current_story_node.get_choices()
        return {str(index): choice for index, choice in enumerate(choices, start=1) if self.check_for_flags(choice)}
        
    def get_description(self):
        descriptions = self.current_story_node.get_descriptions()
        for description in descriptions:
            if self.check_for_flags(description):
                return description
        return self.current_story_node.default_description
        
    def get_post_message(self):
        return self.current_story_node.get_post_message()
        
        
    def get_treasures(self):
        treasures = current_story_node.get_treasures()
        return [treasure for treasure in self.treasures if self.check_for_flags(treasure)]
        
    def get_next_story_node(self):
        all_next_nodes = self.current_story_node.next_nodes
        default = self.current_story_node.default_next_node
        for next_node in all_next_nodes:
            required_flags = next_node["required_flags"]
            forbidden_flags = next_node["forbidden_flags"]
            if required_flags and not self.has_flags(required_flags):
                continue
            if forbidden_flags and self.has_flags(forbidden_flags):
                continue
            return next_node["node"]
        return default
        
    def get_target(self, choice):
        target = random.choice(choice.targets)
        return target
        
    def add_treasure(self, item):
        if not item.taken:
            self.inventory.append(item)
            item.take()
    def update_counters(self):
        for counter in self.counters.values():
            if counter.on:
                counter.update()
        
    #advance story
    def change_story_node(self, story_node):
        if self.current_story_node:
            self.set_flag(self.current_story_node.name) #set flag that the node has been visited
        self.current_story_node = story_node
        self.update_counters()
        self.current_story_node.resolve()
        
    def resolve_choice(self, choice):
        choice.resolve()#
        if choice.flag:
            set_flag(choice.flag) 
        self.change_story_node(choice.target)
        return True
        
     #call this fucntion to reset the game      
    def new_game(self):
        self.change_story_node(self.start_story_node)
        self.inventory.clear()
        self.flags.clear()
        
        #reset story_nodes
        for story_node in self.story_nodes.values():
            story_node.reset()
    def 

    #----------create objects---------------
    def create_story_node(self, *, name, text, **optional_arguments):
        _check_story_node(self, name)
        self.story_nodes[name] = StoryNode(name, text, **optional_arguments)
        
    def create_choice(self, *, node, text: str, target: str, **optional_arguments):
        story_node = _get_story_node(self, node) #get StoryNode object
        choice = Choice(text, target, **optional_arguments)
        story_node.choices.append(choice)
        
    def create_description(self, *, node, text, **optional_arguments):
        story_node = _get_story_node(self, node)
        story_node.descriptions.add_description(Description(text, forbidden_flags, required_flags))
        
    def next_story_node(self, *, node, next_node, **parameters):
        node = _get_story_node(self, node)
        node.store_next_node(next_node, **parameters)
        
    def create_timer(self, *, duration):
        self.timer = Timer(duration)
        
    def create_counter(self, name, max_count, nodes, **optional_arguments):
        self.counters.[name] = Counter(max_count, nodes, **optinal_arguments)
        
    def on_enter(self, node, function, *args):
        story_node = _get_story_node(self, node)
        story_node.on_enter.append(lambda: function(*args))
        
    def on_update(self, node, function):
        story_node = _get_story_node(self, node)
        story_node.on_update = function
        
    def add_callback(self, time, function, *args):
        self.timer.add_callback(time, lambda: function(*args))
            
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
class Renderer:
    def render_node(self, game, node, flags):
        def render_choices(self, choices):
            if choices:
                for key, choice in choices.items():
                    print(f"{key}. {choice.text}")
                    
        node.get_description(game)
        print(node.get_description(flags))
        post_message = node.get_post_message
        if post_message:
            print(post_message)
        choices = node.get_choices(flags)
        self.render_choices(choices)
        
    def render_inventory(self, game, inventory): #render the content of the bag
        self.render_title("Backpack")
        inventory = game.inventory_manager.get_inventory(inventory)
        if inventory:
            for key, item in inventory.items():
                print(f"{key}. {item.name}")
        else:
            print("Backpack is empty")
        print(f"{len(inventory) + 1}. Close backpack")
        
    def render_treasure(self,node):
        treasures = game.current_story_node.get_treasures()
        for treasure in treasures:
            if not treasure.taken:
                success(f"{treasure.name} added to inventory")
                game.add_treasure(treasure)
            
    def render_title(self, title):
        print("*" * (len(title) + 4))
        print(f"* {title.upper()} *")
        print("*" * (len(title) + 4))
        print()
        
class InventoryManager:
    def get_inventory(self, inventory):
        return {str(index) : element for (index, element) in enumerate(inventory, start=1)}
        
    def check_for_item(self, inventory, item_name)
        return item_name in inventory
        
    def add_item(self, item, inventory):
        if item not in inventory:
            inventory.append(item)
            item.take()
    
class FlagManager:
    def set_flag(self, flag):
        if flag not in self.flags:
            self.flags.add(flag)
            
    def has_flags(self, game, flags)
        def has_flag(self, game, flag):
            if flag.startswith("has:"):
                item_name = flag.split("has:")[1]
                if game.inventory_manager.check_for_item(game.inventory, item_name):
                    return True
                        
            elif flag in game.flags:
                return True
            return False
            
        for flag in flags:
            if not self.has_flag(game, flag):
                return False
        return True
                
#StoryNode can have different conditional variants based on flags  
class StoryNode:
    def __init__(self, name, text, default_next_node=None, treasures=None):
        self.name = name
        self.default_description = Description(text)
        self.descriptions = []
        self.default_next_node = default_next_node #next_story_node is a string, change to StoryNode in validation
        self.next_nodes = []
        self.choices = []
        self.treasures = _ensure_list_of_types(treasures, Treasure)
        self.on_enter = []
        self.on_update = None
        self.post_message = ""
        
        #set by game.alternative()
        self.required_flags = list()
        self.message
        
    '''    
    def add_movement(self, directions):
        for key, node in directions.items():
            if key in ["north", "south", "east", "west"]:
                self.choices.append(Choice(f"Move {key}", target=node))
            else:
                raise ValueError(f"{key} is not a valid movement choice")
    '''
    #a function for adding alternative next_nodes
    def  (self, next_node, **parameters):
        for key in parameters.keys():
            if key not in list("required_flags", "forbidden_flags"):
                raise ValueError(f"{key} is not a valid parameter")
            
        required_flags = parameters.get("required_flags", [])
        forbidden_flags = parameters.get("forbidden_flags", [])
        
        required_flags = _ensure_list_of_types(required_flags, str) #make sure input is a list of a specified type/types.
        forbidden_flags = _ensure_list_of_types(forbidden_flags, str)
        if not required_flags or not forbidden_flags:
            raise ValueError("Either forbidden_flags or required_flags must be set")
        
        story_node = {
            "node": next_node,
            "required_flags" : required_flags,
            "forbidden_flags" : forbidden_flags,
        }
        self.next_nodes.append(story_node)
        
    def set_post_message(self, message):
        self.post_message = message
        
    def add_description(self, description):
        self.append(description)
        
    def on_update(self):
        if self.on_update:
            self.on_update()
        
    def resolve(self):
        for function in self.on_enter:
            function()
                
    def reset(self):
        for treasure in self.treasures:
            treasure.reset()
        for choice in self.choices:
            choice.reset()

    def get_post_message(self):
        message = self.post_message
        self.post_message = "" #reset post_message
        return message
        
    def get_choices(self, game):
        return {str(index): choice for index, choice in enumerate(choices, start=1)
            if game.flag_manager.has_flags(game, choice.required_flags) and not game.flag_manager.has_flags(game, choice.forbidden_flags)
        }
        
    def get_description(self, game):
        for description in self.descriptions:
            if game.flag_manager.has_flags(game, description.required_flags) and not game.flag_manager.has_flags(game, description.forbidden_flags):
                return description
        return default_description
        
    def get_treasures(self, game):
        return [treasure for treasure in self.treasures if treasure.take(game)]
    
        
class Choice:
    def __init__(self, text, targets, transition=None, exhaustible=False, forbidden_flags = None, required_flags=None, flag=None,):
        self.text = text
        self.targets = _ensure_list_of_types(targets, str) #will change to StoryNode object in Game.validation()
        self.required_flags = _ensure_list_of_types(required_flags, str)
        self.forbidden_flags = _ensure_list_of_types(forbidden_flags, str)
        self.flag = flag #optional flag that will be set
        self.transition = transition #text that will be displayed when you transition to target node
        
        #Only set exhaustible to true if you are going to be returning to the storynode and you don't want the choice to show up again.
        self.exhaustible = exhaustible
        self.exhausted = False
        
    def resolve(self):
        if self.exhaustible:
            self.exhausted = True
        
    def reset(self):
        self.exhausted = False
        
class Treasure:
    def __init__(self, name, description, forbidden_flags=None, required_flags=None):
        self.name = name
        self.description = description
        self.taken = False
        self.forbidden_flags = _ensure_list_of_types(forbidden_flags, str)
        self.required_flags = _ensure_list_of_types(required_flags, str)
        
    def take(self, game):
        if self.taken:
            return False
        self.taken = True
        if game.flag_manager.has_flags(game, self.required_flags) and not game.flag_manager.has_flags(game, self.forbidden_flags):
            return self
        else:
            return None 
        
    def reset(self):
        self.taken = False
        
class counter:
    def __init__(self, max_count, nodes, on_update=None, on_max=None):
        self.nodes = _ensure_list_of_types(nodes, str) #change to StoryNode objects in validation
        self.counter = 0
        self.max_count = max_count
        self.on_update = _ensure_type(on_update, types.FuntionType) #a function
        self.on_max_count = _ensure_type(on_max, types.FuntionType)
        self.on  = True
         
    def update(self, node):
        if not self.on:
            return
            
        if node in self.nodes:
            self.increase_count
            if on_update:
                self.on_update()
                       
    def increase_count(self):
        self.counter += 1
        if self.count == max_count:
            if self.on_max_count:
                self.on_max_count()
            self.stop()
            self.counter = 0
            
    def validate(self):
        for index, node in enumerate(self.nodes):
            self.nodes[index] = _get_story_node(self, )
                  
    def stop(self):
        self.on = False
        
    def start(self):
        self.on = True
        
class Timer:
    def __init__(self, duration, nodes):
        self.duration = duration
        self.callbacks = {}
        self.time = 0
        self.on = False
        
    def start(self):
        self.on = True
        
    def stop(self):
        self.on = False
        
    def reset(self):
        self.time = 0
        
    def add_callback(self, time, function):
        if time in self.callbacks.keys():
            self.callbacks[time].append(function)
        else:
            self.callbacks[time] = [function]
            
    def update(self):
        if self.on == False:
            return
            
        if self.time >= self.duration:
            self.stop()
            
        if self.time in self.callbacks.keys():
            for function in self.callbacks[self.time]:
                function()
        self.time += 1
        
class Description:
    def __init__(self, text, forbidden_flags=None, required_flags=None):
        self.text = text
        self.forbidden_flags = _ensure_list_of_types(forbidden_flags, str)
        self.required_flags = _ensure_list_of_types(required_flags, str)
#--------------Functions------------------
def _ensure_list_of_types(value, value_types):
    if not value:
        return []
        
    elif isinstance(value, value_types):
        return [value]
        
    elif isinstance(value, list):
        if not all(isinstance(elem, value_types) for elem in value):
            TypeError(f"Element must be of types:{value_types} not {type(eleme)}")
        return value 
        
    else:
        raise TypeError(f"value must be of types:{value_types} or list not {type(value)}")
        
def _ensure_list(value, name):
    if not value:
        value = []
        
    elif not isinstance(value, list):
        
        raise TypeError(
            f"{name} must be an iterable of strings"
        )
    return value
    
def _ensure_type(value, value_types):
    if value and not isintance(value, value_types):
        raise ValueError(f"{value} is not a valid type")
        
def _get_story_node(game, name):
    try:
        return game.story_nodes[name]
    except KeyError:
        raise ValueError(f"StoryNode {name} does not exist")
        
def _check_story_node(game, name):
    if name in game.story_nodes.keys():
        raise ValueError(f"StoryNode {name} already exists")