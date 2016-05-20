from ..utils import *


##
# Minions

class OG_023:
	"Primal Fusion"
	play = Buff(TARGET, "OG_023t") * Count(FRIENDLY_MINIONS + TOTEM)

OG_023t = buff(+1, +1)


class OG_209:
	"Hallazeal the Ascended"
	events = Damage(source=SPELL + FRIENDLY).on(Heal(FRIENDLY_HERO, Damage.AMOUNT))
