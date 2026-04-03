from textadventure import Game, run_cli, Treasure
import text

#final clean up and then i'm done with this
#changes to the validation perhaps
#----Scene-----

game = Game("Trial of the heart") #Game object
game.create_story_node(name="beginning", text=text.beginning, treasures=Treasure("test_item", "this is a description for the test_item"), default_next_node="forest")
game.create_story_node(name="forest", text=text.forest, default_next_node="boulders")
game.create_story_node(name="boulders", text=text.boulders, default_next_node="air")
game.create_story_node(name="air", text=text.air, default_next_node="waterskin")
game.create_story_node(name="waterskin", text=text.waterskin, treasures=Treasure("Waterskin", text.item_waterskin), default_next_node="amulet")
game.create_story_node(name="amulet", text=text.amulet, treasures=Treasure("Ursine Amulet", text.item_amulet), default_next_node="what_now")
game.create_story_node(name="what_now", text="What now?")
game.create_choice(node="what_now", text="Enter the forest", transition=text.determination, target="darkwood")

game.create_story_node(name="darkwood", text=text.darkwood)
game.create_choice(node="darkwood", text="traverse the woods", transition=text.travel, target=["darkwood_1", "darkwood_2" ,"darkwood_3", "darkwood_4", "darkwood_5"])

game.create_story_node(name="darkwood_1", text="You come a cross a small clearing in the woods")
game.create_choice(node="darkwood_1", text="traverse the woods", transition=text.travel, target=["darkwood_2" ,"darkwood_3", "darkwood_4", "darkwood_5"])

game.create_story_node(name="darkwood_2", text="You come a cross a small forest pond")
game.create_choice(node="darkwood_2", text="traverse the woods", transition=text.travel, target=["darkwood_1", "darkwood_3", "darkwood_4", "darkwood_5"])

game.create_story_node(name="darkwood_3", text="You come a cross a hughely tall tree")
game.create_choice(node="darkwood_3", text="traverse the woods", transition=text.travel, target=["darkwood_1", "darkwood_2", "darkwood_4", "darkwood_5"])

game.create_story_node(name="darkwood_4", text="You come a cross an abandoned hunting cabbin")
game.create_choice(node="darkwood_4", text="traverse the woods", transition=text.travel, target=["darkwood_1", "darkwood_2" ,"darkwood_3", "darkwood_5"])

game.create_story_node(name="darkwood_5", text="You come a cross a hughely tall tree")
game.create_choice(node="darkwood_5", text="traverse the woods", transition=text.travel, target=["darkwood_1", "darkwood_2" ,"darkwood_3", "darkwood_4"])




'''
game.story_node(name="darkwood", desc=text.darkwood, north="darkwood_1", south="darkwood_2", east="darkwood_3")
game.story_node(name="darkwood_1", desc="You come to a dark clearing in the forrest", south="darkwood")
game.story_node(name="darkwood_2", desc="You see a twisted tree", north="darkwood")
game.story_node(name="darkwood_3", desc="You spot a huge tree that has been split down the middle by a lightning", west="darkwood")

#a loop for when you get lost
game.story_node(name="lost1_tall_tree", desc="you see a see darkwoods all around you", south="lost_2", north="lost_2", east="lost_2", west="lost_2")
game.choice(node="lost_1", text="Climb a the tree", target="climb_a_tree")
game.story_Node(name="climb_a_tree", desc="You begin to accend the tree. Just as you are about to reach the top you fall", target="lost1_tall_tree", exhaustible=True) 

game.story_node(name="lost2_pond", desc="You come a cross a small pond", south="lost_3", 
game.story_node(name="lost_2", desc="you are in a dark forrest", south="lost_3", north="lost_3", 
game.story_node(name="lost_3", desc="You wander in the dark, with the tree trunks surrounding you from all sides", north="darkwood", south="darkwood", east="darkwood", west="darkwood"

game.story_node(name="lost1_tall_tree", desc="You see a large tree, perhaps you could climb it to see better", south="lost_2", north="lost_2", east="lost_2", west="lost_2") #radom event1

#game.treasure(node="waterskin", name="waterskin", desc=text.item_waterskin)
#game.treasure(node="amulet", name="ursine amulet", desc=text.item_amulet)
'''

#----Validate----
game.validate("beginning")

#----Run-------
if __name__== "__main__":
    run_cli(game)