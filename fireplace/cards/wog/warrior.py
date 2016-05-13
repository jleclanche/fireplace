from ..utils import *


##
# Minions


##
# Spells

class OG_276:
	"Blood Warriors"
	play = Give(CONTROLLER, Copy(FRIENDLY_MINIONS + DAMAGED))


class OG_314:
	"Blood To Ichor"
	play = Hit(TARGET,1), Dead(TARGET) | Summon(CONTROLLER, "OG_314b")
