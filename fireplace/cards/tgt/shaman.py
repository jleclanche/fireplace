from ..utils import *


##
# Minions

# Tuskarr Totemic
class AT_046:
	play = Summon(CONTROLLER, RandomTotem())


# Draenei Totemcarver
class AT_047:
	play = Buff(SELF, "AT_047e") * Count(FRIENDLY_MINIONS + TOTEM)


# Thunder Bluff Valiant
class AT_049:
	inspire = Buff(FRIENDLY_MINIONS + TOTEM, "AT_049e")
