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
game.story_node(name="darkwood", desc=text.darkwood, north="darkwood_1", south="darkwood_2", east="darkwood_3")
game.story_node(name="darkwood_1", desc="You come to a dark clearing in the forrest", south="darkwood")
game.story_node(name="darkwood_2", desc="You see a twisted tree", north="darkwood")
game.story_node(name="darkwood_3", desc="You spot a huge tree that has been split down the middle by a lightning", west="darkwood")

#a loop for when you get lost
game.story_node(name="lost_1", desc="you see a see darkwoods all around you", south="lost_2", north="lost_2", east="lost_2", west="lost_2")
game.story_node(name="lost_2", desc="you are in a dark forrest", south="lost_3", north="lost_3", 
game.story_node(name="lost_3", desc="You wander in the dark, with the tree trunks surrounding you from all sides", north="darkwood", south="darkwood", east="darkwood", west="darkwood"

game.story_node(name="lost1_tall_tree", desc="You see a large tree, perhaps you could climb it to see better", south="lost_2", north="lost_2", east="lost_2", west="lost_2") #radom event1

#game.treasure(node="waterskin", name="waterskin", desc=text.item_waterskin)
#game.treasure(node="amulet", name="ursine amulet", desc=text.item_amulet)


#----Validate----
game.validate("beginning")

#----Run-------
if __name__== "__main__":
    run_cli(game)

