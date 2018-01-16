from ..utils import *


##
# Minions
class ICC_025:
	"Rattling Rascal"
	play = Summon(CONTROLLER, "ICC_025t")
	deathrattle = Summon(OPPONENT, "ICC_025t")


class ICC_911:
	"Keening Banshee"
	events = Play(CONTROLLER).on(Mill(CONTROLLER, 3))


##
# Spells


##
# Secrets

class ICC_082:
	"Frozen Clone"
	secret = Play(OPPONENT, MINION).after(
		Reveal(SELF), Give(CONTROLLER, Copy(Play.CARD)) * 2
	)
