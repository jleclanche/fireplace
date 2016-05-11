from ..utils import *


##
# Minions

class OG_209:
	"Hallazeal the Ascended"
	events = Damage(source=SPELL + FRIENDLY).on(Heal(FRIENDLY_HERO, Damage.AMOUNT))
