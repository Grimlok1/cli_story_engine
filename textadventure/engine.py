import random
class Game: #Game object is used to create all other objects
    def __init__(self, name):
        self.inventory = [] #player inventory
        self.story_nodes = {} #all story_nodes
        #self.items = {} #stores all items used for validation
        self.name = name
        self.current_story_node = None
        self.flags = set()
        self.start_story_node = None
        self.timer = None #maybe add option to add multiple timers in the future
    
    
    def has_flag(self, flag):
        if flag.startswith("has:"):
            item_name = flag.split(":", 1)[1]
            return item_name in [item.name for item in self.inventory] #True or False

        return flag in self.flags #True of False
        
    def has_flags(self, flags):
        for flag in flags:
            if not self.has_flag(flag):
                return False
        return True
        
    def get_inventory(self):
        return {str(index) : element for (index, element) in enumerate(self.inventory, start=1)}
        
    def get_choices(self):
        choices = self.current_story_node.get_choices()
        return {str(index): choice for index, choice in enumerate(choices, start=1) if self.has_flags(choice.required_flags)}
        
    def get_treasures(self):
        return self.current_story_node.treasure
        
    def get_current_description(self):
        return self.current_story_node.get_description()
            
    def add_item(self, item):
        if not item.taken:
            self.inventory.append(item)
            item.take()
            
    def node_visited(self):
        flag = f"visited:{self.current_story_node.name}"
        if flag not in self.flags:
            self.flags.add(flag)
        
    #advance story
    def change_story_node(self, story_node):
        if self.current_story_node:
            self.node_visited() #set flag that the node has been visited
            self.current_story_node.reset_description()
        self.current_story_node = story_node.get_story_node(self)
        self.current_story_node.resolve()
        
        if self.timer:
            self.timer.update()
        
    def resolve_choice(self, choice):
        choice.resolve()
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
        
    def start_timer(self):
        self.timer.start()
        
    #----------create objects---------------
    
    def story_node(self, *, name, desc, next_node=None, treasure=None, **directions):
        _check_story_node(self, name)
        self.story_nodes[name] = StoryNode(name, desc, next_node, treasure, **directions)
          
    #StoryNode can have multiple conditional alternatives   
    def alternative(self, *, node, name, desc, next_node=None, required_flags=None):
        story_node = _get_story_node(self, node)
        alternative_node = StoryNode(name, desc, next_node)
        alternative_node.required_flags = _ensure_list(required_flags, "required_flags")
        self.story_nodes[name] = alternative_node
        story_node.alternatives.append(alternative_node)
     
    def choice(self, *, node, text: str, target: str, transition=None, exhaustible=False, required_flags=None, flag=None):
        story_node = _get_story_node(self, node) #get StoryNode object
        choice = Choice(text, target, transition,  exhaustible, required_flags, flag=None)
        story_node.choices.append(choice)
        
    #!!!!!!!!!!!!!!!!!!Maybe rework later
    def treasure(self, *, node, name, desc):
        story_node = _get_story_node(self, node)#get StoryNode object
        treasure = Treasure(name, desc)
        story_node.treasure.append(treasure)
        #self.items[name] = treasure
              
    #add adition description if you want the description to change when you visit the node again
    def description(self, *, node, text, treasure=None):
        story_node = _get_story_node(self, node)
        story_node.store_description(text, treasure)
        
    def create_timer(self, *, duration):
        self.timer = Timer(duration)
        
    def on_enter(self, node, function, *args):
        story_node = _get_story_node(self, node)
        story_node.on_enter.append(lambda: function(*args))
        
    def add_callback(self, time, function, *args):
        self.timer.add_callback(time, lambda: function(*args))
            
    #-----------validate-----------------
    
    def validate(self, start):
        all_choices = [choice for story_node in self.story_nodes.values() for choice in story_node.choices]
        next_story_nodes = [story_node for story_node in self.story_nodes.values() if story_node.next_story_node]
        alternatives = [alternative for story_node in self.story_nodes.values() for alternative in story_node.alternatives]
        
        self.start_story_node = _get_story_node(self, start)
        self.change_story_node(self.start_story_node) #set start node as current_story_node
        
        for story_node in next_story_nodes:
            node = _get_story_node(self, story_node.next_story_node)
            story_node.set_next_story_node(node)
              
        for choice in all_choices:
            if choice.target:
                node = _get_story_node(self, choice.target)
                choice.set_target(node)
                
            #replace this code later
            """    
            for i, item in enumerate(choice.required_items): #required items
                choice.required_items[i] = _get_item(self, item)
            
            for i, story_node in enumerate(choice.visited_nodes): #visited nodes
                choice.visited_nodes[i] = _get_story_node(self, story_node)
            """                

#StoryNode can have different conditional variants based on flags  
class StoryNode:
    def __init__(self, name, description, next_story_node=None, treasure=None, mode="normal" **directions):
        self.name = name
        self.descriptions = []
        self.next_story_node = next_story_node #next_story_node is a string
        self.alternatives = []
        self.choices = []
        self.treasure = []
        self.on_enter = []
        self.current_step = 0
        self.mode = mode #set random to get radom description
        
        #normalize description to list
        if isinstance(description, list):
            self.description = description
        else:
            self.description = [description]
            
        #Store the first description
        self.store_description(description, treasure)
      
        #set by game.alternative()
        self.required_flags = list()
        #add movement options/choices
        self.add_movement(directions)
        
    def add_movement(self, directions):
        for key, node in directions.items():
            if key in ["north", "south", "east", "west"]:
                self.choices.append(Choice(f"Move {key}", target=node))
            else:
                raise ValueError(f"{key} is not a valid movement choice")
        
    def get_story_node(self, game):
        for alternative in self.alternatives:
            if self.has_flags(alternative.flags):
                return alternative
        return self
        
    def get_descriptions(self): #modified to return all the descriptions
        if mode == "random":
            return self.get_random_description()    
        return self.descriptions
    
    def get_random_description(self):
        return random.choice(self.random_descriptions)
        
    def resolve(self):
        for function in self.on_enter:
            function()
            
    def reset_description(self):
        self.current_step = 0
        
    def reset(self):
        self.reset_description()
        for description in self.descriptions:
            treasure = description["treasure"]
            if treasure:
                treasure.reset()
        for choice in self.choices:
            choice.reset()
            
    def set_next_story_node(self, node): #change str to an actual StoryNode object
        self.next_story_node = node
        
    def store_description(self, text, treasure=None):
        self.descriptions.append({"text" : text, "treasure" : treasure})
        
    def get_choices(self):
        return self.choices
        
class Choice:
    def __init__(self, text: str, targets: str, transition=None, exhaustible=False, required_flags=None, flag=None,):
        self.text = text
        self.targets = [target] #will change to StoryNode object in Game.validation()
        self.required_flags = _ensure_list(required_flags, "requires")
        self.flag = flag #optional flag that will be set
        self.transition = transition #text that will be displayed when you transition to target node
        
        #Only set exhaustible to true if you are going to be returning to the storynode and you don't want the choice to show up again.
        self.exhaustible = exhaustible
        self.exhausted = False
        
    def resolve(self):
        if self.exhaustible:
            self.exhausted = True
        if self.flag:
            self.flags.add(flag)
            
    def set_target(self, node): #change from str to StoryNode
        for target in self.targets:
            self.target = node
            
    def get_target(self):
        return random.choice(self.target)
        
    def reset(self):
        self.exhausted = False
        
class Treasure:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.taken = False
        
    def take(self):
        self.taken = True
        
    def reset(self):
        self.taken = False
        
class Timer:
    def __init__(self, duration):
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
        print(self.time)
        if self.on == False:
            return
            
        if self.time >= self.duration:
            self.stop()
            
        if self.time in self.callbacks.keys():
            for function in self.callbacks[self.time]:
                function()
        self.time += 1
        
#--------------Functions------------------
            
def _ensure_list(value, name):
    if not value:
        return list()
        
    elif not isinstance(value, list):
        raise TypeError(
            f"{name} must be an iterable of strings"
        )
    return list(value)
    
def _get_story_node(game, name):
    try:
        return game.story_nodes[name]
    except KeyError:
        raise ValueError(f"StoryNode {name} does not exist")
        
def _check_story_node(game, name):
    if name in game.story_nodes.keys():
        raise ValueError(f"StoryNode {name} already exists")
        
def _get_item(game, name):
    try:
        return game.items[name]
    except KeyError:
        raise ValueError(f"Item {name} does not exist")
        
def _get_timer(game, name):
    try:
        return game.timer[name]
    except KeyError:
        raise ValueError(f"Timer {name} does not exist")