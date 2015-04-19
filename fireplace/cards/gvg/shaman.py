from ..utils import *


##
# Spells

# Ancestor's Call
class GVG_029:
	action = [
		ForcePlay(CONTROLLER, RANDOM(CONTROLLER_HAND + MINION)),
		ForcePlay(OPPONENT, RANDOM(OPPONENT_HAND + MINION)),
	]
