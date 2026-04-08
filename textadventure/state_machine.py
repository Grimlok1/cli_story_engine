import os
class StateMachine:
    def __init__(self, game):
        self.game = game
        self.renderer = game.renderer
        self.inventory_manager = game.inventory_manager
        self.states = {}
        self.state = None
        
    def change_state(self, name, **kwargs):
        self.state = self.states[name]
        self.state.kwargs = kwargs
          
    def create_state(self, name, func):
        self.states[name] = State(self, func)
        
    def run(self):
        self.state.run()
        
class State:
    def __init__(self, state_machine, func):
        self.func = func
        self.state_machine = state_machine
        self.kwargs = {}
        
    def run(self):
        os.system("cls" if os.name == "nt" else "clear")
        self.func(self.state_machine, **self.kwargs)
