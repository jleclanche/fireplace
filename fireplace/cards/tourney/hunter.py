from ..utils import *


##
# Spells

# Lock and Load
class AT_061:
	play = Buff(FRIENDLY_HERO, "AT_061e")

class PH_HUNT_001e:
	events = OWN_SPELL_PLAY.on(
		Give(CONTROLLER, RandomCollectible(card_class=CardClass.HUNTER))
	)


# Ball of Spiders
class AT_062:
	play = Summon(CONTROLLER, "FP1_011") * 3
