class Game: #Game object is used to create all other objects
    def __init__(self, name):
        self.flags = set()
        self.inventory = []
        self.scenes = {}
        self.events = []
        self.options = []
        self.name = name
        self.current_scene = None
        self.current_event = None
        self.start_scene = None
        
    #check if scene already exits
    def check_scene(self, name):
        if name in self.scenes.keys():
            ValueError(f"Scene {name} already exists")
            
    def check_for_items(self, items): #return true if flags is empty
        ls = set([treasure.name for treasure in self.inventory])
        return items.issubset(ls)
        
    def check_for_flags(self, flags): #return true if flags is empty
        flags = set(flags)
        return flags.issubset(self.flags)

    def get_inventory(self):
        return {str(index) : element for (index, element) in enumerate(self.inventory, start=1)}
        
    
        
    #----------create objects---------------
    
    def scene(self, name, description):
        self.check_scene(name)
        self.scenes[name] = self.Scene(description)
     
    def option(self, source, target, description, *, event="default", required_flags=None, required_items=None, flag=None):
        scene = _get_scene(self, source) #get scene function
        target_scene =  _get_scene(self, target)
        
        option = self.Option(description, target_scene, required_flags, required_items, flag)
        scene.events[event].options.append(option)
        self.options.append(option) #for validation
    
    def treasure(self, source, *, event="default"):
        scene = _get_scene(self, source) #get scene
        
        treasure = self.Treasure(name, description)
        scene.events[event].treasure.append(treasure)
        self.treasures.append(treasure) #for validation
        
    def event(self, source, name, description, *, required_flags=None, required_items=None):
        if required_flags is None and required_items is None:
            ValueError("At least of of 'required_flags' or 'required_items' must be provided")
        scene = _get_scene(self, source)
        event = Event(description, required_flags, required_items)
        scene.events[name] = event
        self.events.append(event)
        
    #-----------validate-----------------
    
    def validate(self, start):
        
        if start not in self.scenes.keys():
            raise ValueError(f"Start event '{start}' does not exist")
        else:
            self.start_scene = self.scenes[start]
 
        for option in self.options:
            if option.target not in self.scenes.values():
                raise ValueError(f"Option point to a unknown scene: {option.target}")
                
        for event in self.events:
            if event.treasure not in self.treasure:
                    raise ValueError(f"{event.tresure} is not a valid Treasure object")
        
    class Scene:
        def __init__(self, description):
            self.events = {}
            self.events["default"] = self.Event(description)
            
        def set_current_event(self, game): #ota pelkästää alternative eventit
            current_event = self.events["default"]
            for key, event in self.events.items():
                if event.check_event(game) and key != "default":
                    current_event = event
            game.current_event = current_event
                

        class Event:
            #lisää myöhemmin mahdollisuus lisätä monta kuvausta... ehkä
            def __init__(self, description, required_flags=None, required_items=None):
                self.description = description
                self.required_flags = _ensure_set(required_flags, "required_flags")
                self.required_items = _ensure_set(required_items, "required_items")
                self.options = []
                self.treasure = []
                self.visited = False
                    
            def check_event(self, game):
                if game.check_for_flags(self.required_flags) and game.check_for_items(self.required_items):
                    return True
                    
            def resolve(self, game):
                #add items to inventory
                if not self.visited:
                    for treasure in self.treasure:
                        game.inventory.append(treasure)
                    self.visited = True
              
            def get_options(self, game): 
                available_options = {}
                i = 1
                for option in self.options:
                    if option.check_option(game):
                        available_options[str(i)] = option
                        i += 1
                return available_options

    class Option:
        def __init__(self, description, target, required_flags=None, required_items=None, flag=None):
            self.description = description
            self.target = target #scene ->
            self.flag = flag
            self.required_flags = _ensure_set(required_flags, "required_flags")
            self.required_items = _ensure_set(required_items, "required_items")
            
            
        def check_option(self, game):
            if game.check_for_flags(self.required_flags) and game.check_for_items(self.required_items):
                return True
        
    class Treasure:
        def __init__(self, name, description):
            self.name = name
            self.description = description
                
def _ensure_set(value, name):
    if value is None:
        return set()
    if isinstance(value, str):
        raise TypeError(
            f"{name} must be an iterable of strings, not a string"
        )
    return set(value)
    
def _get_scene(game, name):
    try:
        return game.scenes[name]
    except KeyError:
        raise ValueError(f"Event {name} does not exist")