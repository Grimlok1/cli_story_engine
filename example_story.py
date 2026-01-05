from story_builder import StoryBuilder
from game import Game

game = Game("Markuksen villahousupeli") #Game object
story = StoryBuilder(game)

story.event("start", "Pue Markukselle villahousut?")
story.event("häviö", "\"Huh, tulipa hiki!\" Hävisit pelin!")
story.event("voitto", "\"Onpa mukavan viileä.\" Voitit pelin!")

story.option("start", "Pue villa housut", "häviö", required_items=["Villahousut"])
story.option("start", "Älä pue", "voitto")
story.treasure("start", "Villahousut", "Perinteiset suomalaiset villahousut. Erittäin lämpimät")

story.validate("start")

#Events