class Game: #Game object is used to create all other objects
    def __init__(self, name):
        self.inventory = []
        self.story_nodes = {}
        self.visited_nodes = set() #list of StoryNode.name. Same function as flags
        self.name = name
        self.current_story_node = None
        self.start_story_node = None
        
    #check if story_node already exits
    def check_story_node(self, name):
        if name in self.story_nodes.keys():
            raise ValueError(f"StoryNode {name} already exists")
            
    def check_for_items(self, items: set): #return true if flags are empty
        if not items:
            return  True
            
        for item in items:
            if item not in self.inventory:
                return False
        return True
        
    def check_visited_nodes(self, nodes: set): #return true if node is visited
        if not nodes:
            return True
            
        for node in nodes:
            if node not in self.visited_nodes:
                return False
        return True

    def get_inventory(self):
        return {str(index) : element for (index, element) in enumerate(self.inventory, start=1)}
            
    
        
    #----------create objects---------------
    
    def story_node(self, *, name, desc, next_node=None):
        self.check_story_node(name)
        self.story_nodes[name] = StoryNode(name, desc, next_node)
        
    #StoryNode can have multiple conditional alternatives   
    def alternative(self, *, node, name, desc, next_node=None, required_items=None, visited_nodes=None):
    
        if visited_nodes is None and required_items is None:
            raise ValueError("At least one of 'visited_nodes' or 'required_items' must be provided")
            
        story_node = _get_story_node(self, node)
        alternative_node = StoryNode(name, desc, next_node)
        alternative_node.required_items = _ensure_set(required_items, "required_items")
        alternative_node.visited_nodes = _ensure_set(visited_nodes, "visited_nodes")
        story_node.alternatives.append(alternative_node)
     
    def choice(self, *, node, desc: str, target: str, visited_nodes=None, required_items=None, exhaustible=False):
        story_node = _get_story_node(self, node) #get StoryNode object
        choice = Choice(desc, target, visited_nodes, required_items, exhaustible)
        story_node.choices.append(choice)
        

    def treasure(self, *, node, name, description):
        story_node = _get_story_node(self, node)#get StoryNode object
        story_node.treasure.append(Treasure(name, description))

    #-----------validate-----------------
    
    def validate(self, start):
        
        if start not in self.story_nodes.keys():
            raise ValueError(f"Start state '{start}' does not exist")
        else:
            self.start_story_node = self.story_nodes[start]
  
        all_choices = [choice for story_node in self.story_nodes.values() for choice in story_node.choices]
        all_flags = [story_node.name for story_node in self.story_nodes.values()] #same as the story_node names
       
                    
        for story_node in self.story_nodes.values():
            if story_node.next_story_node and story_node.next_story_node not in self.story_nodes.keys():
                    raise ValueError(f"{story_node.name} variable next_story_node. Doesn't point to a valid StoryNode")
                    
        for choice in all_choices:
            for node in choice.visited_nodes:
                if node not in self.story_nodes:
                    raise ValueError(f"{node} is not a valid StoryNode")
                    
        for choice in all_choices:
            if choice.target not in self.story_nodes.keys():
                raise ValueError(f"{choice.target} is not a valid StoryNode")
        

#StoryNode can have different variants  
class StoryNode:
    def __init__(self, name, description, next_story_node=None):
        self.name = name
        self.description = description
        self.next_story_node = next_story_node
        self.alternatives = [] #hold alternative StoryNodes
        self.choices = []
        self.treasure = []
          
        #set by game.alternative()
        self.required_items = None
        self.visited_nodes = None
   
    def get_story_node(self, game):
        for alternative in self.alternatives:
            if alternative.check_alternative(game):
                return alternative
        return self

    def get_choices(self, game): 
        available_choices = {}
        i = 1
        for choice in self.choices:
            if choice.get_choice(game):
                available_choices[str(i)] = choice
                i += 1
        return available_choices
            
    def check_alternative(self, game):
        return (game.check_visited_nodes(self.visited_nodes) and game.check_for_items(self.required_items))
        
        
#StoryNode can have multiple Choices
##MOVE FLAG TO STORYNODE!
class Choice:
    def __init__(self, description: str, target: str, visited_nodes=None, required_items=None, exhaustible=False):
        self.description = description
        self.target = target #game.story_nodes[target] -> StoryNode
        
        self.visited_nodes = _ensure_set(visited_nodes, "visited_nodes")
        self.required_items = _ensure_set(required_items, "required_items")
        
        #Only set exhaustible to true if you are going to be returning to the storynode and you don't want the choice to show up again.
        self.exhaustible = exhaustible
        self.exhausted = False
          
    def get_choice(self, game):
        if game.check_visited_nodes(self.visited_nodes) and game.check_for_items(self.required_items) and not self.exhausted:
            return True
        else:
            return False
 
class Treasure:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        


#--------------Functions------------------
            
def _ensure_set(value, name):
    if value is None:
        return set()
    if isinstance(value, str):
        raise TypeError(
            f"{name} must be an iterable of strings, not a string"
        )
    return set(value)
    
def _get_story_node(game, name):
    try:
        return game.story_nodes[name]
    except KeyError:
        raise ValueError(f"StoryNode {name} does not exist")