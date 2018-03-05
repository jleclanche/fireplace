from ..utils import *

##
# Minions


##
# Spells

class LOOT_008:
	"Psychic Scream"
	play = Steal(FRIENDLY_MINIONS, OPPONENT), Shuffle(OPPONENT, ALL_MINIONS)
	# The following fails for friendly minions:
	#play = Shuffle(OPPONENT, ALL_MINIONS)