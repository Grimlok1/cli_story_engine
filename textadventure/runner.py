from .text_color import error, success, info, title
from .state_machine import StateMachine
import os
     
def run_game(game):
    state_machine = StateMachine(game)
    state_machine.create_state("main_menu", main_menu)
    state_machine.create_state("game_loop", game_loop)
    state_machine.create_state("inventory_menu", inventory_menu)
    state_machine.create_state("game_over", game_over)
    state_machine.create_state("pop_up_menu", pop_up_menu)
    state_machine.create_state("help_menu", help_menu)
    state_machine.create_state("item_menu", item_menu)
    state_machine.change_state("main_menu")

    #Commands for opening the inventory and quiting the game
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
    
def game_loop(sm):
    node = sm.game.current_node
    choices = node.resolve(sm.game)
    if not choices:
        next_node = node.get_next_node()
        if next_node:
            input("Continue...")
            sm.game.change_node(next_node) #change to next_story_node
        else:
            sm.change_state("game_over") #game over
        return
        
    user_input = input(">")
    if user_input in sm.commands: #executes a command like, open inventory
        sm.commands[user_input]()
    else:
        sm.game.input_handler(user_input)
           
#-----------------FUNCTIONS--------------        
def quit_game(game):
    game.renderer.render_text("Quitting game...")
    quit()
    
#------------------------MENUS---------------
def pop_up_menu(sm):
    sm.renderer.render_text("Are you sure you want to quit?\n")
    sm.renderer.render_text("1. Continue\n2. Main menu\n3. Exit game")
    i = input("> ")
    if i == "1":
        sm.change_state("game_loop")
    elif i == "2":
        sm.change_state("main_menu")
    elif i == "3":
        quit_game()
    
def main_menu(sm):
    sm.renderer.render_title(sm.game.name)
    sm.renderer.render("1. Start game\n2. Help\n3. Quit game")

    i = input("> ")
    if i == "1":
        sm.game.new_game()
        sm.change_state("game_loop")
    elif i == "2":
        sm.change_state("help_menu")
    elif i == "3":
        quit_game()
        
def help_menu(sm):
    sm.renderer.render_title("HELP MENU") 
    sm.renderer.render_text(info("Type 'bag', 'b', 'inventory' or 'i' if you wish to access player inventory"))
    sm.renderer.render_text(info("Type 'Quit' or 'q' if you wish to quit the game\n"))
    input("(Press Enter to return to Main menu)")
    sm.change_state("main_menu")
        
def inventory_menu(sm):
    sm.game.renderer.render_title("Backpack")
    inventory = sm.inventory_manager.get_inventory(sm.game.inventory)
    if inventory:
        for key, item in inventory.items():
            sm.renderer.render_text(f"{key}. {item.name}")
        sm.renderer.render_text(f"{len(inventory) + 1}. Close backpack")
    else:
        sm.game.renderer.render_text("Backpack is empty")
        
    choice = input("> ")
    if choice in inventory.keys():
        sm.change_state("item_menu", item=inventory[choice])
        
    elif choice == f"{len(inventory) + 1}":
        sm.change_state("game_loop")
        
def item_menu(sm, item):
    sm.renderer.render_title(item.name)
    sm.renderer.render(info(f"{item.description}\n"))
    input("(Press enter to return)")
    sm.change_state("inventory_menu")
    
def game_over(sm):
    sm.renderer.render_text(sm.game) #game over StoryNode displaying the text for one frame and then changing the state to game_over seems a bit redundant. Perhaps rework this.
    sm.renderer.render_text(error("Game over!\n"))
    sm.renderer.render_text("1. Return to main menu\n2. Quit game")
    i = input("> ")
    if i == "1":
        sm.change_state("main_menu")
    elif i == "2":
        quit_game(sm.game)
