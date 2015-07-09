from ..utils import *


##
# Spells

# Flameheart
class BRMA_01:
	action = [Draw(CONTROLLER) * 2, GainArmor(FRIENDLY_HERO, 4)]
