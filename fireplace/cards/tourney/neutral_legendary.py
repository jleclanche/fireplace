from ..utils import *


##
# Minions

# Skycap'n Kragg
class AT_070:
	cost = lambda self, i: i - len(self.controller.field.filter(race=Race.PIRATE))
