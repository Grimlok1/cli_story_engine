from game import Game
import text
#----Scene-----

game = Game("Markuksen villahousupeli") #Game object
game.scene("herätys", text.HERÄTYS)
game.scene("aamupala", text.AAMUPALA)
game.scene("murot", "syöt aamupalaksi ravitsevia muroja")
game.scene("leipä", "otat aamupalaksi hieman paahtoleipää")
game.scene("banaani", "Syöt aamupalaksi yhden banaanin")
game.scene("loppu", "peli loppui!")

#----Options-----
game.option("herätys", "loppu", "kyllä")
game.option("herätys", "loppu", "ei")
game.option("aamupala", "murot", "syö muroja")
game.option("aamupala", "leipä", "syö ruisleipää")
game.option("aamupala", "banaani", "syö banaani")
game.option
#----Validate----

game.validate("aamupala")


