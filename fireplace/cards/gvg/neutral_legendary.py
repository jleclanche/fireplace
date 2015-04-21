from ..utils import *


##
# Minions

# Dr. Boom
class GVG_110:
	action = [Summon(CONTROLLER, "GVG_110t") * 2]

# Boom Bot
class GVG_110t:
	def deathrattle(self):
		return [Hit(RANDOM_ENEMY_CHARACTER, random.randint(1, 4))]


# Sneed's Old Shredder
class GVG_114:
	def deathrattle(self):
		legendary = randomCollectible(type=CardType.MINION, rarity=Rarity.LEGENDARY)
		return [Summon(CONTROLLER, legendary)]
