from example_story import game
from ui import error, success, info
import os



def main():
    error_message = ""
    while True:
        choice = main_menu(error_message)
        if choice == "1":
            run_game()
            error_message = ""

        elif choice == "2":
            quit_game()

        else:
            error_message = "Invalid input!"

def run_game():
    commands = dict(bag = inventory_menu, b = inventory_menu, quit = quit_game)
    new_game()
    error_message = "" #reset after display

    while True:
        render_scene(error_message) #render scene and set current_event

        error_message = "" #reset after display

        if not game.current_event.options:
            game_over()
            return

        action, value = ask_input(commands)
        
        #resolve option
        if action == "option":
            game.current_scene = value.target #set current_scene

        elif action == "command":
            value()

        elif action == "error":
            error_message = value

#-----------------FUNCTIONS--------------    
def quit_game():
    quit()

def new_game():
    game.current_scene = game.start_scene
    game.flags = set()
    game.inventory.clear()
    
    ###FIX
    #for event in game.events.values(): Korjaa MYÖHEMMIN!
        #event.visited = False

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def ask_input(commands):
    options = game.current_event.get_options(game)
    choice = input("> ")

    if choice in options.keys():
        return ("option", options[choice])

    elif choice in commands:
        return ("command", commands[choice])

    else:
        return ("error", "Invalid input!")
        
#------------------------MENUS---------------
def inventory_menu():
    message = ""
    msg_type = "default"
    while True:
        clear_screen()
        inventory = render_inventory()

        if msg_type == "error":
            error(message)
        else:
            info(message)

        choice = input("> ")

        if choice in inventory.keys():
            message = f"{inventory[choice].name}: {inventory[choice].description}"
            msg_type = "default"

        elif choice == f"{len(inventory) + 1}":
            return

        else:
            message = "Invalid input!"
            msg_type = "error"
            
def main_menu(error_message):
    clear_screen() 
    print(f"{game.name}\n")
    print("1. Start game\n2. Quit game\n")
    error(error_message)

    return input("> ")
    
def game_over():
    while True:
        clear_screen()
        print(f"{game.current_event.description}\n")
        error("Game over!\n")

        print("1. Return to main menu\n2. Quit game\n")
        i = input("> ")
        if i == "1":
            return
        elif i == "2":
            quit()

#----------------Rendering-------------------

def render_scene(error_message=""):
    game.current_scene.set_current_event(game) #set current event
    clear_screen()
    render_event()
    render_options()
    error(f"{error_message}")
    
def render_inventory():
    print("Backpack items:\n")
    inventory = game.get_inventory()
    for key, item in inventory.items():
        print(f"{key}. {item.name}")

    print(f"{len(game.inventory) + 1}. close bag")
    return inventory

def render_event():
    event = game.current_event
    print(f"{event.description}\n")
    for treasure in event.treasure:
        success(f"{treasure.name} added to inventory\n")
    event.resolve(game)
    
def render_options():
    if game.current_event.options:
        for key, option in game.current_event.get_options(game).items():
            print(f"{key}. {option.description}")

      

if __name__ == "__main__":
    main()
