class Game:
    def __init__(self, name):
        self.flags = set()
        self.inventory = []
        self.events = {}
        self.conditional_events = {}
        self.name = name
        self.current_event = None
        self.start = None

    def check_for_items(self, items):
        ls = set([treasure.name for treasure in self.inventory])
        return items.issubset(ls)
        
    def check_for_flags(self, flags):
        flags = set(flags)
        return flags.issubset(self.flags)

    def get_inventory(self):
        return {str(index) : element for (index, element) in enumerate(self.inventory, start=1)}
        
class Event:
    #lisää myöhemmin mahdollisuus lisätä monta kuvausta... ehkä
    def __init__(self, description):
        self.description = description
        self.options = []
        self.treasure = []
        self.visited = False

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
            option_obj = option.get_option(game)
            if option_obj:
                available_options[str(i)] = option_obj
                i += 1
        return available_options

    class Option:
        def __init__(self, description, def_event, conditional_events=None, required_flags=None, required_items=None, flag=None):
            self.description = description
            self.def_event = def_event
            self.conditional_events = _ensure_set(conditional_events, "conditional_events")
            self.flag = flag
            self.required_flags = _ensure_set(required_flags, "required_flags")
            self.required_items = _ensure_set(required_items, "required_items")

            #handle option
        def get_next_event(self, game):
            #add flags if any
            if self.flag:
                game.flags.add(str(self.flag))
                
            next_event = self.def_event
            
            for event in self.conditional_events:
                if event.check_event(game):
                    next_event = event
                    break
                    
            return next_event
            
            
        def get_option(self, game):
            if game.check_for_flags(self.required_flags) and game.check_for_items(self.required_items):
                return self
        
    class Treasure:
        def __init__(self, name, description):
            self.name = name
            self.description = description

                
class ConditionalEvent(Event):
    def __init__(self, description, required_flags=None, required_items=None):
        super().__init__(description)
        self.required_flags = _ensure_set(required_flags, "required_flags")
        self.required_items = _ensure_set(required_items, "required_items")
        
        if not self.required_flags and self.required_items:
            raise ValueError("Either required_flags or required_items must be provided")
            
    def check_event(self, game):
        if self.required_flags:
            return game.check_for_flags(self.required_flags)
            
def _ensure_set(value, name):
    if value is None:
        return set()
    if isinstance(value, str):
        raise TypeError(
            f"{name} must be an iterable of strings, not a string"
        )
    return set(value)
