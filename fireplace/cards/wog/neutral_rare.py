from ..utils import *


##
# Minions

class OG_034:
	"Silithid Swarmer"
	update = (NUM_ATTACKS_THIS_TURN(FRIENDLY_HERO) == 0) & (
		Refresh(SELF, {GameTag.CANT_ATTACK: True})
	)
