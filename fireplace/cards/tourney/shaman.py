from ..utils import *


##
# Minions

# Draenei Totemcarver
class PH_SHAM_001:
	play = Buff(SELF, "PH_SHAM_001e") * Count(FRIENDLY_MINIONS + TOTEM)


# Thunder Bluff Valiant
class PH_SHAM_002:
	inspire = Buff(FRIENDLY_TOTEMS, "PH_SHAM_002e")


# Tuskarr Totemic
class PH_SHAM_003:
	play = Summon(CONTROLLER, RandomTotem())
