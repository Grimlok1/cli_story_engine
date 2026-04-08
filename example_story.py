from textadventure import Game
from textadventure import StoryFactory
import text

game = Game("Trial of the heart") #Game object
f = StoryFactory()
f = game.story_factory
f.node(name="beginning", text=text.beginning, treasures=Treasure("test_item", "this is a description for the test_item"), default_next_node="forest")
f.node(name="forest", text=text.forest, default_next_node="boulders")
f.node(name="boulders", text=text.boulders, default_next_node="air")
f.node(name="air", text=text.air, default_next_node="waterskin")
f.node(name="waterskin", text=text.waterskin, treasures=Treasure("Waterskin", text.item_waterskin), default_next_node="amulet")
f.node(name="amulet", text=text.amulet, treasures=Treasure("Ursine Amulet", text.item_amulet), default_next_node="what_now")
f.node(name="what_now", text="What now?")
f.choice(node_name="what_now", text="Enter the forest", transition_text=text.determination, target="darkwood")

f.node(name="darkwood", text=text.darkwood)
f.choice(node="darkwood", text="traverse the woods", transition_text=text.travel, target=["darkwood_1", "darkwood_2" ,"darkwood_3", "darkwood_4", "darkwood_5"])

f.node(name="darkwood_1", text="You come a cross a small clearing in the woods")
f.choice(node_name="darkwood_1", text="traverse the woods", transition_text=text.travel, target=["darkwood_2" ,"darkwood_3", "darkwood_4", "darkwood_5"])

f.node(name="darkwood_2", text="You come a cross a small forest pond")
f.choice(node_name="darkwood_2", text="traverse the woods", transition_text=text.travel, target=["darkwood_1", "darkwood_3", "darkwood_4", "darkwood_5"])

f.node(name="darkwood_3", text="You come a cross a hughely tall tree")
f.choice(node_name="darkwood_3", text="traverse the woods", transition_text=text.travel, target=["darkwood_1", "darkwood_2", "darkwood_4", "darkwood_5"])

f.node(name="darkwood_4", text="You come a cross an abandoned hunting cabbin")
f.choice(node_name="darkwood_4", text="traverse the woods", transition_text=text.travel, target=["darkwood_1", "darkwood_2" ,"darkwood_3", "darkwood_5"])

f.node(name="darkwood_5", text="You come a cross a hughely tall tree")
f.choice(node_name="darkwood_5", text="traverse the woods", transition_text=text.travel, target=["darkwood_1", "darkwood_2" ,"darkwood_3", "darkwood_4"])


#----Validate----
story_data = f.build(start_node_name="beginning")
game = Game(name="Trial of the heart", data=story_data)
#----Run-------
if __name__== "__main__":
    run_cli(game)