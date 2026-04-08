import random
#StoryNode can have different conditional variants based on flags  
class Node:
    def __init__(self, name, text, default_next_node=None, treasures=None):
        self.name = name
        self.default_description = Description(text)
        self.default_next_node = default_next_node #next_story_node is a string, change to StoryNode in validation
        self.descriptions = []
        self.next_nodes = []
        self.choices = []
        self.treasures = _ensure_list_of_types(treasures, Treasure)
        
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
    def __init__(self, text, target_nodes, transition_text=None, exhaustible=False, forbidden_flags = None, required_flags=None, flag=None,):
        self.text = text
        self.target_nodes = _ensure_list_of_types(target_nodes, str)# target_nodes will be changed into Node objects in the Validation
        self.required_flags = _ensure_list_of_types(required_flags, str)
        self.forbidden_flags = _ensure_list_of_types(forbidden_flags, str)
        self.flag = flag #optional flag that will be set
        self.transition_text = transition_text #text that will be displayed when you transition to target node
        
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