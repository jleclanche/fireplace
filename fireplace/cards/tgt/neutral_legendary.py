from ..utils import *


##
# Minions

# Confessor Paletress
class AT_018:
	inspire = Summon(CONTROLLER, RandomMinion(rarity=Rarity.LEGENDARY))


# Skycap'n Kragg
class AT_070:
	cost = lambda self, i: i - len(self.controller.field.filter(race=Race.PIRATE))
