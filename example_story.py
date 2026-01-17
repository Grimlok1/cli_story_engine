from story_builder import StoryBuilder
from game import Game
import text

game = Game("Markuksen villahousupeli") #Game object
story = StoryBuilder(game)
story.event("aamupala", "Syötkö aamupalan")
story.event("start", text.START)
story.event("häviö", text.VILLAHOUSUT)
story.event("voitto", "\"Onpa mukavan viileä.\" Voitit pelin!")
story.event("kalsarit", text.KALSARIT) 
story.event("riisu_kalsarit", text.RIISU_KALSARIT)
story.event("hyppää_lumeen", text.HYPPÄÄ_LUMEEN)
story.event("juokse", text.JUOKSE)
story.conditional_event("nälkä", "voi ei unohdit syödä aamupalan ja nyt sinulla on nälkä, hävisit pelin!", required_flags=["nälkä"])

story.option("aamupala", "Kyllä", "start")
story.option("aamupala", "Ei", "start", flag="nälkä")
story.option("start", "Pue villa housut", "häviö")
story.option("start", "Pue kalsarit", "kalsarit", conditional_events=["nälkä"])
story.option("start", "Älä pue", "voitto")

story.option("kalsarit", "riisu kalsarit", "riisu_kalsarit")
story.option("kalsarit", "hyppää äkkiä lumihankeen!", "hyppää_lumeen")
story.option("kalsarit", "juokse äkkiä joosepin luo", "juokse")

story.treasure("start", "Villahousut", "Perinteiset suomalaiset villahousut. Erittäin lämpimät")
story.treasure("start", "Kalsarit", "Perinteiset suomalaiset pitkät kalsarit melko lämpimät")

story.validate("aamupala")

#Events