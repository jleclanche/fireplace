from ..utils import *


##
# Spells

# Flameheart
class BRMA_01:
	play = Draw(CONTROLLER) * 2, GainArmor(FRIENDLY_HERO, 4)
