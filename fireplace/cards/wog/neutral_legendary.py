from ..utils import *


##
# Minions

class OG_122:
	"Mukla, Tyrant of the Vale"
	play = Give(CONTROLLER, "EX1_014t") * 2


class OG_318:
	"Hogger, Doom of Elwynn"
	events = SELF_DAMAGE.on(Summon(CONTROLLER, "OG_318t"))


class OG_338:
	"Nat, the Darkfisher"
	events = BeginTurn(OPPONENT).on(COINFLIP & Draw(OPPONENT))
