from ..utils import *


##
# Minions

# Skycap'n Kragg
class PH_NEUTRAL_LEGENDARY_001:
	cost = lambda self, i: i - self.controller.field.filter(race=Race.PIRATE)
