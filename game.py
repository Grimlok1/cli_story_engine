class Game:
    def __init__(self, name):
        self.flags = set()
        self.inventory = []
        self.events = {}
        self.name = name
        self.current_event = None
        self.start = None

    def check_for_item(self, items):
        ls = set([treasure.name for treasure in self.inventory])
        return items.issubset(ls)

    def get_inventory(self):
        return {str(index) : element for (index, element) in enumerate(self.inventory, start=1)}

class Event:
    #lisää myöhemmin mahdollisuus lisätä monta kuvausta... ehkä
    def __init__(self, description, flag=None):
        self.description = description
        self.options = []
        self.treasure = []
        self.flag = flag
        self.visited = False

    def resolve(self, game):
        if self.flag:
            game.flags.add(self.flag)

        #add items to inventory
        if not self.visited:
            for treasure in self.treasure:
                game.inventory.append(treasure)
            self.visited = True

    def get_options(self, game):
        available_options = {}
        i = 1
        for option in self.options:
            if option.required_flags.issubset(game.flags) and game.check_for_item(option.required_items):
                available_options[str(i)] = option
                i = i + 1

        return available_options

    class Option:
        def __init__(self, description, def_event, required_flags=None, required_items=None):
            self.description = description
            self.def_event = def_event

            self.required_flags = set(required_flags or [])
            self.required_items = set(required_items or [])

        def get_next_event(self, game):
            next_event = self.def_event
            return next_event

    class Treasure:
        def __init__(self, name, description):
            self.name = name
            self.description = description