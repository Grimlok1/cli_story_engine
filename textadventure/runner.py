from ui import error, success, info, title
import os


class StateMachine:
    def __init__(self, game):
        self.game = game
        self.states = {}
        self.state = None
        
    def change_state(self, name):
        self.state = self.states[name]
          
    def create_state(self, name, func):
        self.states[name] = State(self, func)
        
    def run(self):
        self.state.run()
        
class State:
    def __init__(self, state_machine, func):
        self.func = func
        self.state_machine = state_machine
        self.arguments = {}
        
    def run(self):
        clear_screen()
        self.func(self.state_machine, **self.arguments)
        
    def set_arguments(self, **arguments):
        self.arguments = arguments
        
        
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
        
    while True:
        state_machine.run()
    

def run_game(state_machine):
    render_story_node(state_machine)
    render_treasure(state_machine) #if any
    choices = render_choices(state_machine) #if any
    advance_story(state_machine, choices)
    
    
#-----------------FUNCTIONS--------------

def advance_story(state_machine, choices):

    if choices:
        ask_input(state_machine, choices)
        return False
        
    #If no available choices and the next_story_node is set. Change to the next story_node >
    if state_machine.game.current_story_node.next_story_node:
        state_machine.game.current_story_node = state_machine.game.current_story_node.next_story_node
        input("\n(Press Enter)")
        
    #If no available choices. Game over!
    else:
        state_machine.change_state("game_over")
   
    return True

    
def quit_game():
    print("Quitting game...")
    quit()
    

def new_game(state_machine):
    state_machine.game.current_story_node = state_machine.game.start_story_node
    state_machine.game.inventory.clear()
    state_machine.game.visited_nodes.clear()
    
    #reset story_nodes
    for story_node in state_machine.game.story_nodes.values():
        for choice in story_node.choices:
            choice.exhausted = False
   
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def ask_input(state_machine, choices):
    choice = input("> ")
    
    #resolve choice
    if choice in choices.keys():
        resolve_choice(choices[choice], state_machine)
    
    elif choice in state_machine.commands:
        state_machine.commands[choice]()


        
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
    render_title(state_machine.game.name)
    print("1. Start game\n2. Help\n3. Quit game")

    i = input("> ")
    if i == "1":
        new_game(state_machine)
        state_machine.change_state("run_game")
    elif i == "2":
        state_machine.change_state("help_menu")
    elif i == "3":
        quit_game()
        
def help_menu(state_machine):
    render_title("HELP MENU") 
    info("Type 'bag', 'b', 'inventory' or 'i' if you wish to access player inventory")
    info("Type 'Quit' or 'q' if you wish to quit the game\n")
    input("(Press Enter to return to Main menu)")
    state_machine.change_state("main_menu")
        
def inventory_menu(state_machine):
    inventory = render_inventory(state_machine)
    
    choice = input("> ")
    if choice in inventory.keys():
        print(f"{inventory[choice].name}: {inventory[choice].description}")
        state_machine.change_state("item_menu")
        state_machine.state.set_arguments(item = inventory[choice]) #
        
    elif choice == f"{len(inventory) + 1}":
        state_machine.change_state("run_game")
        
def item_menu(state_machine, item):
    render_title(item.name)
    info(f"{item.description}\n")
    input("(Press enter to return)")
    state_machine.change_state("inventory_menu")
    

def game_over(state_machine):
    info(f"{state_machine.game.current_story_node.description}\n") #game over StoryNode displaying the text for one frame and then changing the state to game_over seems a bit redundant. Perhaps rework this.
    error("Game over!\n")

    print("1. Return to main menu\n2. Quit game")
    
    i = input("> ")
    
    if i == "1":
        state_machine.change_state("main_menu")
    elif i == "2":
        quit_game()

#----------------Rendering-------------------
def render_title(title):
    print("*" * (len(title) + 4))
    print(f"* {title.upper()} *")
    print("*" * (len(title) + 4))
    print()
    
    
def render_story_node(state_machine):
    state_machine.game.current_story_node = state_machine.game.current_story_node.get_story_node(state_machine.game)
    info(f"{state_machine.game.current_story_node.description}\n")
    

def render_treasure(state_machine):
    if state_machine.game.current_story_node not in state_machine.game.visited_nodes: #somehow is always true!!!
        for treasure in state_machine.game.current_story_node.treasure:
            success(f"{treasure.name} added to inventory\n")
            state_machine.game.inventory.append(treasure)
        state_machine.game.visited_nodes.add(state_machine.game.current_story_node) #add node to visited. Perhaps create a resolve funtion for story node
    
def render_choices(state_machine):
    choices = state_machine.game.current_story_node.get_choices(state_machine.game)
  
    for key, choice in choices.items():
        print(f"{key}. {choice.description}")
    return choices

def render_inventory(state_machine): #render the content of the bag
    render_title("Backpack")
    inventory = state_machine.game.get_inventory()
    for key, item in inventory.items():
        print(f"{key}. {item.name}")

    print(f"{len(state_machine.game.inventory) + 1}. Close backpack")
    return inventory
    
#----------------------------------------------------
def resolve_choice(choice, state_machine):
    if choice.exhaustible:
        choice.exhausted = True
    state_machine.game.current_story_node = choice.target


if __name__ == "__main__":
    main()
