from ..utils import *

##
# Minions

class LOOT_041:
	"Kobold Barbarian"
	events = OWN_TURN_BEGIN.on(Attack(SELF, RANDOM_ENEMY_CHARACTER))

##
# Spells

##
# Weapons


