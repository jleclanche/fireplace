from ..utils import *


##
# Minions

# Hallazeal the Ascended
class OG_209:
	events = Damage(source=SPELL + FRIENDLY).on(Heal(FRIENDLY_HERO, Damage.AMOUNT))
