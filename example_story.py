from game import Game
import text

#final clean up and then i'm done with this
#changes to the validation perhaps
#----Scene-----

game = Game("Conversation Demo") #Game object

game.story_node(name="start", desc="Hey, where am i?", next_node="voice1")
game.story_node(name="voice1", desc="You are where you are. Is there anything else you\'d like to know?")
game.choice(node="voice1", desc="Yes", target="voice")

game.story_node(name="voice", desc="What do you want to know?", next_node="wake_up")
game.choice(node="voice", desc="Who are you?", target="who", exhaustible=True)
game.choice(node="voice", desc="Where am i", target="where", exhaustible=True)
game.choice(node="voice", desc="What is the meaning of all this?", target="what", exhaustible=True, visited_nodes=["who", "where"])

game.story_node(name="what", desc="Nothing really", next_node="wake_up")
game.story_node(name="who", desc="No one important really", next_node="voice")
game.story_node(name="where", desc="Didn\'t you hear what i said", next_node="voice")
game.story_node(name="wake_up", desc="Well this has been a waste of time. Time to wake up!")





#----Validate----

game.validate("start")


