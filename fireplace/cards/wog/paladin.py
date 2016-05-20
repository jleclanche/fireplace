from ..utils import *


##
# Minions


class OG_006:
	"Vilefin Inquisitor"
	play = Summon(CONTROLLER, "OG_006b")

class OG_006b:
	"The Tidal Hand"
	activate = Summon(CONTROLLER, "OG_006a")
