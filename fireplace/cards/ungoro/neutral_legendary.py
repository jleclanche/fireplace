from ..utils import *

##
# Minions

# TODO(czxcjx): does this put them in the graveyard?
class UNG_840:
	"Hemet, Jungle Hunter"
	play = Destroy(FRIENDLY_DECK + (COST <= 3))

# class UNG_843:
#	"The Voraxx"

class UNG_851:
	"Elise the Trailblazer"
	play = Shuffle(CONTROLLER, "UNG_851t1")

# class UNG_851t1:
# 	"Un'Goro Pack"

# class UNG_900:
#	"Spiritsinger Umbra"

# class UNG_907:
#	"Ozruk"
