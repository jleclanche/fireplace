from ..utils import *

##
# Minions

class LOOT_026:
	"Fal'dorei Strider"
	play = Shuffle(CONTROLLER, "LOOT_026e") * 3

class LOOT_026e:
	draw = Destroy(SELF), Summon(CONTROLLER, "LOOT_026t"), Draw(CONTROLLER)

class LOOT_033:
	"Cavern Shinyfinder"
	play = ForceDraw(RANDOM(FRIENDLY_DECK + WEAPON))

##
# Spells