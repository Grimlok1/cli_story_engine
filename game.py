class Game:
    def __init__(self, name):
        self.flags = set()
        self.inventory = set()
        self.events = {}
        self.name = name
        self.current_event = None

    def get_inventory(self):
        return {key : value for key, value in enumerate(self.inventory, start=1)}

class Event:
    #lisää myöhemmin mahdollisuus lisätä monta kuvausta... ehkä
    def __init__(self, description, required_flags=None, required_items=None, flag=None):
        self.description = description
        self.options = []
        self.treasure = []
        self.flag = flag
        self.required_flags = set(required_flags or [])
        self.required_items = set(required_items or [])
        self.visited = False

    def resolve(self, game):
        if self.flag:
            game.flags.add(self.flag)

        #add items to inventory
        if not self.visited:
            for treasure in self.treasure:
                game.inventory.add(treasure)
            self.visited = True

    def get_options(self, game):
        available_options = {}
        i = 1
        for option in self.options:
            if not option.required_flags.issubset(game.flags):
                continue
            if option.required_items and not option.required_items in [item.name for item in game.inventory]:
                continue
            available_options[str(i)] = option
            i = i + 1
        return available_options

    class Option:
        def __init__(self, description, def_event, alt_events=None, required_flags=None, required_items=None):
            self.description = description
            self.def_event = def_event
            self.alt_events = alt_events or []

            self.required_flags = set(required_flags or [])
            self.required_items = set(required_items or [])

        def get_next_event(self, game):
            next_event = self.def_event
            for event in self.alt_events:
                if event.required_flags.issubset(game.flags):
                    next_event = event
                    break
            return next_event

    class Treasure:
        def __init__(self, name, description):
            self.name = name
            self.description = description