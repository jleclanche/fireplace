from ..utils import *


##
# Spells

# Lock and Load
class PH_HUNT_001:
	play = Buff(FRIENDLY_HERO, "PH_HUNT_001e")

class PH_HUNT_001e:
	events = OWN_SPELL_PLAY.on(
		Give(CONTROLLER, RandomCollectible(card_class=CardClass.HUNTER))
	)


# Ball of Spiders
class PH_HUNT_002:
	play = Summon(CONTROLLER, "FP1_011") * 3
