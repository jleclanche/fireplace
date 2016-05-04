from ..utils import *


##
# Minions


##
# Spells

# Thistle Tea
class OG_073:
	play = Draw(CONTROLLER).then(Give(CONTROLLER, Copy(Draw.CARD)) * 2)
