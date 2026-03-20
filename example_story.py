from textadventure import Game, run_cli, Treasure
import text

#final clean up and then i'm done with this
#changes to the validation perhaps
#----Scene-----

game = Game("Trial of the heart") #Game object
game.story_node(name="beginning", desc=text.beginning, treasure=Treasure("test_item", "this is a description for the test_item"))
game.description(node="beginning", text=text.forest)
game.description(node="beginning", text=text.bolders)
game.description(node="beginning", text=text.air)
game.description(node="beginning", text=text.waterskin, treasure=Treasure("waterskin", text.item_waterskin))
game.description(node="beginning", text=text.amulet, treasure=Treasure("Ursine Amulet", text.item_amulet))
game.choice(node="beginning", text="Enter the Forest", transition=text.determination, target="darkwood")
game.story_node(name="darkwood", desc=text.darkwood)

#game.treasure(node="waterskin", name="waterskin", desc=text.item_waterskin)
#game.treasure(node="amulet", name="ursine amulet", desc=text.item_amulet)


#----Validate----
game.validate("beginning")

#----Run-------
if __name__== "__main__":
    run_cli(game)

