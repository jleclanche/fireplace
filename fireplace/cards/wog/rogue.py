from ..utils import *


##
# Minions


##
# Spells

class OG_073:
	"Thistle Tea"
	play = Draw(CONTROLLER).then(Give(CONTROLLER, Copy(Draw.CARD)) * 2)
