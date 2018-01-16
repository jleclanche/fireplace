from ..utils import *

##
# Minions

class UNG_058:
	"Razorpetal Lasher"
	play = Give(CONTROLLER, "UNG_057t1")

##
# Spells

class UNG_057:
	"Razorpetal"
	play = Give(CONTROLLER, "UNG_057t1") * 2


class UNG_057t1:
	"Razorpetal"
	play = Hit(TARGET, 1)
