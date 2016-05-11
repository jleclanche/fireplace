from ..utils import *


##
# Minions

class OG_121:
	"Cho'gall"
	play = Buff(CONTROLLER, "OG_121e")

class OG_121e:
	events = OWN_SPELL_PLAY.on(Destroy(SELF))
	update = Refresh(CONTROLLER, {GameTag.SPELLS_COST_HEALTH: True})
