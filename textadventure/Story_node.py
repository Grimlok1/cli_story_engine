import random
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
        
    '''    
    def add_movement(self, directions):
        for key, node in directions.items():
            if key in ["north", "south", "east", "west"]:
                self.choices.append(Choice(f"Move {key}", target=node))
            else:
                raise ValueError(f"{key} is not a valid movement choice")
    '''
    #a function for adding alternative next_nodes
    def  add_next_node(self, next_node, **parameters):
        for key in parameters.keys():
            if key not in list("required_flags", "forbidden_flags"):
                raise ValueError(f"{key} is not a valid parameter")
            
        required_flags = parameters.get("required_flags", [])
        forbidden_flags = parameters.get("forbidden_flags", [])
        required_flags = _ensure_list_of_types(required_flags, str) #make sure input is a list of a specified type/types.
        forbidden_flags = _ensure_list_of_types(forbidden_flags, str)
        if not required_flags or not forbidden_flags:
            raise ValueError("Either forbidden_flags or required_flags must be set")
        
        node = {
            "node": next_node,
            "required_flags" : required_flags,
            "forbidden_flags" : forbidden_flags,
        }
        self.next_nodes.append(node)
        
    def set_post_message(self, message):
        self.post_message = message
        
    def add_description(self, description):
        self.append(description)
        
    def on_update(self):
        if self.on_update:
            self.on_update()
        
    def resolve(self, game):
        description = self.get_description(game)
        game.renderer.render_text(description)
        choices = self.get_choices(game)
        for choice in choices:
            game.renderer.render_text(choice.text)
        post_message = self.get_post_message()
        game.renderer.render_text(post_message)
        return choices

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
        return {str(index): choice for index, choice in enumerate(self.choices, start=1)
            if game.flag_manager.has_flags(game, choice.required_flags) and game.flag_manager.no_flags(game, choice.forbidden_flags)
        }
        
    def get_description(self, game):
        for description in self.descriptions:
            text = description.get_description(game)
            if text:
                return text
        return self.default_description.get_description(game)
        
    def get_treasures(self, game):
        return [treasure for treasure in self.treasures if treasure.take(game)]
    
    def get_next_node(self, game):
        for next_node in self.next_nodes:
            required_flags = next_node["required_flags"]
            forbidden_flags = next_node["forbidden_flags"]
            if game.flag_manager.has_flags(game, required_flags) and game.flag_manager.no_flags(game, forbidden_flags):
                return next_node
        return self.default_next_node
    
    
        
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
    
    def resolve(self, game):
        if self.transition:
            game.renderer.render_text(self.transition)
            input("Continue...")

        if self.exhaustible:
            self.exhausted = True
        game.change_node(self.get_target())

    def get_target(self):
        return random.target
  
    def reset(self):
        self.exhausted = False
        
class Treasure:
    def __init__(self, name, description, forbidden_flags=None, required_flags=None):
        self.name = name
        self.description = description
        self.taken = False
        self.forbidden_flags = _ensure_list_of_types(forbidden_flags, str)
        self.required_flags = _ensure_list_of_types(required_flags, str)

    def add_treasure(self, game):
        if not self.taken:
            game.renderer.render_text((f"{self.name} added to inventory"))
            game.add_treasure(self)
        
    def take(self, game):
        if self.taken:
            return False
        self.taken = True
        
        if game.flag_manager.has_flags(game, self.required_flags) and not game.flag_manager.has_flags(game, self.forbidden_flags):
            self.add_treasure(game)
            return self

        else:
            return None 
        
    def reset(self):
        self.taken = False
        
class Counter:
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
            if self.on_update:
                self.on_update()
                       
    def increase_count(self):
        self.counter += 1
        if self.count == self.max_count:
            if self.on_max_count:
                self.on_max_count()
            self.stop()
            self.counter = 0

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

    def get_description(self, game):
        if game.flag_manager.has_flags(game.flags, self.required_flags) and game.flag_manager.no_flags(game.flags, self.forbidden_flags):
            return self.text
        
#--------------Functions------------------
def _ensure_list_of_types(value, value_types):
    if not value:
        return []
        
    elif isinstance(value, value_types):
        return [value]
        
    elif isinstance(value, list):
        if not all(isinstance(elem, value_types) for elem in value):
            TypeError(f"Element must be of types:{value_types}")
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
    if value and not isinstance(value, value_types):
        raise ValueError(f"{value} is not a valid type")
        
def _get_story_node(game, name):
    try:
        return game.story_nodes[name]
    except KeyError:
        raise ValueError(f"StoryNode {name} does not exist")