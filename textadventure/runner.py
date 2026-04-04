from textadventure.ui import error, success, info, title
import os


class StateMachine:
    def __init__(self, game):
        self.game = game
        self.rederer = game.renderer
        self.current_node = game.current_story_node
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
        clear_screen()
        self.func(self.state_machine, **self.kwargs)
        
        
def run_cli(game):
    state_machine = StateMachine(game)
    state_machine.create_state("main_menu", main_menu)
    state_machine.create_state("run_game", run_game)
    state_machine.create_state("inventory_menu", inventory_menu)
    state_machine.create_state("game_over", game_over)
    state_machine.create_state("pop_up_menu", pop_up_menu)
    state_machine.create_state("help_menu", help_menu)
    state_machine.create_state("item_menu", item_menu)
    state_machine.change_state("main_menu") 
    state_machine.commands = dict(
        bag = lambda: state_machine.change_state("inventory_menu"),
        b = lambda: state_machine.change_state("inventory_menu"),
        i = lambda: state_machine.change_state("inventory_menu"),
        inventory = lambda: state_machine.change_state("inventory_menu"),
        quit = lambda: state_machine.change_state("pop_up_menu"),
        q = lambda: state_machine.change_state("pop_up_menu"),
        )
        
    while True: #game loop
        state_machine.run()
    
#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------

def run_game(state_machine):
    game = state_machine.game
    game.renderer.render_node(game, game.current_story_node, game.flags)
    
    if not game.current_story_node.choices:
        next_node = game.get_next_story_node()
        if next_node:
            input("Continue...")
            game.change_story_node(next_node) #change to next_story_node
        else:
            state_machine.change_state("game_over") #game over
        return
        
    user_input = input(">")
    handle_user_input(state_machine, user_input)
           
#-----------------FUNCTIONS--------------
def handle_user_input(state_machine, user_input): #user_input should be something like: 1, 2, 3, 4
    game = state_machine.game
    if user_input in state_machine.commands: #execute a command
        state_machine.commands[user_input]()
        return
        
    choices = game.get_choices()
    if user_input in choices.keys():
        choice = choices[user_input]
        resolve_choice(game, choice) 
       
            
def resolve_choice(game, choice):
    if choice.transition:
        game.renderer.render_text(choice.transition)
        input("Continue...")
    choice.resolve()
    game.change_story_node(game.get_target(choice))
        
def quit_game():
    print("Quitting game...")
    quit()
    
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")
     
#------------------------MENUS---------------
def pop_up_menu(state_machine):
    print("Are you sure you want to quit?\n")
    print("1. Continue\n2. Main menu\n3. Exit game")
    i = input("> ")
    if i == "1":
        state_machine.change_state("run_game")
    elif i == "2":
        state_machine.change_state("main_menu")
    elif i == "3":
        quit_game()
    
def main_menu(state_machine):
    state_machine.renderer.render_title(state_machine.game.name)
    print("1. Start game\n2. Help\n3. Quit game")

    i = input("> ")
    if i == "1":
        state_machine.game.new_game()
        state_machine.change_state("run_game")
    elif i == "2":
        state_machine.change_state("help_menu")
    elif i == "3":
        quit_game()
        
def help_menu(state_machine):
    state_machine.renderer.render_title("HELP MENU") 
    info("Type 'bag', 'b', 'inventory' or 'i' if you wish to access player inventory")
    info("Type 'Quit' or 'q' if you wish to quit the game\n")
    input("(Press Enter to return to Main menu)")
    state_machine.change_state("main_menu")
        
def inventory_menu(state_machine):
    renderer = state_machine.game.renderer
    inventory = renderer.render_inventory(state_machine)
    
    choice = input("> ")
    if choice in inventory.keys():
        state_machine.change_state("item_menu", item=inventory[choice])
        
    elif choice == f"{len(inventory) + 1}":
        state_machine.change_state("run_game")
        
def item_menu(state_machine, item):
    state_machine.renderer.render_title(item.name)
    info(f"{item.description}\n")
    input("(Press enter to return)")
    state_machine.change_state("inventory_menu")
    
def game_over(state_machine):
    state_machine.renderer.render_description(state_machine.game) #game over StoryNode displaying the text for one frame and then changing the state to game_over seems a bit redundant. Perhaps rework this.
    error("Game over!\n")

    print("1. Return to main menu\n2. Quit game")
    
    i = input("> ")
    
    if i == "1":
        state_machine.change_state("main_menu")
    elif i == "2":
        quit_game()
