from ..utils import *


##
# Minions

# Cho'gall
class OG_121:
	play = Buff(CONTROLLER, "OG_121e")

class OG_121e:
	events = OWN_SPELL_PLAY.on(Destroy(SELF))
	update = Refresh(CONTROLLER, {GameTag.SPELLS_COST_HEALTH: True})
