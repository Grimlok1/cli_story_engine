class Game: #Game object is used to create all other objects
    def __init__(self, name):
        self.inventory = []
        self.story_nodes = {} #all story_nodes
        self.items = {} #hold all the items
        self.visited_nodes = set() #list of StoryNode.name. Same function as flags
        self.name = name
        self.current_story_node = None
        self.start_story_node = None
        
        
    #check if story_node already exits
    def check_story_node(self, name):
        if name in self.story_nodes.keys():
            raise ValueError(f"StoryNode {name} already exists")
            
    def check_for_items(self, items: set):
        for item in items:
            if item not in self.inventory:
                return False
        return True
        
    def check_visited_nodes(self, nodes: set):
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
    def alternative(self, *, node, name, desc, next_node=None, required_items=None, visited_nodes=None): #stop alternative or conditional alternative node form having a conditional alternative node. Somehow?
    
        if visited_nodes is None and required_items is None:
            raise ValueError("At least one of 'visited_nodes' or 'required_items' must be provided")
            
        story_node = _get_story_node(self, node)
        alternative_node = StoryNode(name, desc, next_node)
        alternative_node.required_items = _ensure_list(required_items, "required_items")
        alternative_node.visited_nodes = _ensure_list(visited_nodes, "visited_nodes")
        self.story_nodes[name] = alternative_node
        story_node.alternatives.append(alternative_node)
     
    def choice(self, *, node, desc: str, target: str, visited_nodes=None, required_items=None, exhaustible=False):
        story_node = _get_story_node(self, node) #get StoryNode object
        choice = Choice(desc, target, visited_nodes, required_items, exhaustible)
        story_node.choices.append(choice)
        
    #!!!!!!!!!!!!!!!!!!Maybe rework later
    def treasure(self, *, node, name, description):
        story_node = _get_story_node(self, node)#get StoryNode object
        treasure = Treasure(name, description)
        story_node.treasure.append(treasure)
        self.items[name] = treasure

    #-----------validate-----------------
    
    def validate(self, start):
      
        all_choices = [choice for story_node in self.story_nodes.values() for choice in story_node.choices]
        next_story_nodes = [story_node for story_node in self.story_nodes.values() if story_node.next_story_node]
        alternatives = [alternative for story_node in self.story_nodes.values() for alternative in story_node.alternatives]
        
        self.start_story_node = _get_story_node(self, start)
        
        for story_node in next_story_nodes:
            story_node.next_story_node = _get_story_node(self, story_node.next_story_node)
        
        for alternative in alternatives:
            for i, item in enumerate(alternative.required_items):
                alternative.required_items[i] = _get_item(self, item)
        
            for i, node in enumerate(alternative.visited_nodes):
                alternative.visited_nodes[i] = _get_story_node(self, node)
                
        for choice in all_choices:
            if choice.target: #targets
                choice.target = _get_story_node(self, choice.target)
            for i, item in enumerate(choice.required_items): #required items
                choice.required_items[i] = _get_item(self, item)
            
            for i, story_node in enumerate(choice.visited_nodes): #visited nodes
                choice.visited_nodes[i] = _get_story_node(self, story_node)
        #
       

#StoryNode can have different variants  
class StoryNode:
    def __init__(self, name, description, next_story_node=None):
        self.name = name
        self.description = description
        self.next_story_node = next_story_node #next_story_node is a string
        self.alternatives = []
        self.choices = []
        self.treasure = []
          
        #set by game.alternative()
        self.required_items = list()
        self.visited_nodes = list ()
   
    def get_story_node(self, game):
        for alternative in self.alternatives:
            if alternative.check_alternative(game):
                return alternative
        return self

    def get_choices(self, game): 
        available_choices = {}
        i = 1
        for choice in self.choices:
            if choice.check_choice(game):
                available_choices[str(i)] = choice
                i += 1
        return available_choices
            
    def check_alternative(self, game): #check return true if empty
        return game.check_visited_nodes(self.visited_nodes) and game.check_for_items(self.required_items)
     
        
        
#StoryNode can have multiple Choices
##MOVE FLAG TO STORYNODE!
class Choice:
    def __init__(self, description: str, target: str, visited_nodes=None, required_items=None, exhaustible=False):
        self.description = description
        self.target = target #game.story_nodes[target] -> StoryNode
        
        self.visited_nodes = _ensure_list(visited_nodes, "visited_nodes") #
        self.required_items = _ensure_list(required_items, "required_items")# 
        
        #Only set exhaustible to true if you are going to be returning to the storynode and you don't want the choice to show up again.
        self.exhaustible = exhaustible
        self.exhausted = False
          
    def check_choice(self, game):
        return game.check_visited_nodes(self.visited_nodes) and game.check_for_items(self.required_items) and not self.exhausted
       
class Treasure:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        


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
        
def _get_item(game, name):
    try:
        return game.items[name]
    except KeyError:
        raise ValueError(f"Item {name} does not exist")