from ..utils import *


##
# Minions

class OG_042:
	"Y'Shaarj, Rage Unbound"
	events = OWN_TURN_END.on(Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION)))


class OG_122:
	"Mukla, Tyrant of the Vale"
	play = Give(CONTROLLER, "EX1_014t") * 2


class OG_317:
	"Deathwing, Dragonlord"
	deathrattle = Summon(CONTROLLER, FRIENDLY_HAND + DRAGON)


class OG_318:
	"Hogger, Doom of Elwynn"
	events = SELF_DAMAGE.on(Summon(CONTROLLER, "OG_318t"))


class OG_338:
	"Nat, the Darkfisher"
	events = BeginTurn(OPPONENT).on(COINFLIP & Draw(OPPONENT))
