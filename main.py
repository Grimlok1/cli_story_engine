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
        render_scene(error_message)

        error_message = "" #reset after display

        if not game.current_event.options:
            game_over()
            return

        action, value = ask_input(commands)

        if action == "event":
            game.current_event = value.get_next_event(game)

        elif action == "command":
            value()

        elif action == "error":
            error_message = value

    
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

def new_game():
    game.current_event = game.start
    game.flags = set()
    game.inventory.clear()
    for event in game.events.values():
        event.visited = False

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def ask_input(commands):
    options = game.current_event.get_options(game)
    choice = input("> ")

    if choice in options.keys():
        return ("event", options[choice])

    elif choice in commands:
        return ("command", commands[choice])

    else:
        return ("error", "Invalid input!")

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

def quit_game():
    quit()

def render_scene(error_message=""):
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

      
def main_menu(error_message):
    clear_screen() 
    print(f"{game.name}\n")
    print("1. Start game\n2. Quit game\n")
    error(error_message)

    return input("> ")

if __name__ == "__main__":
    main()
