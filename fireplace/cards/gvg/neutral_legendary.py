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


# Toshley
class GVG_115:
	action = [GiveSparePart(CONTROLLER)]
	deathrattle = [GiveSparePart(CONTROLLER)]


# Mekgineer Thermaplugg
class GVG_116:
	def MINION_DESTROY(self, minion):
		if minion.controller is not self.controller:
			return [Summon(CONTROLLER, "EX1_029")]


# Gazlowe
class GVG_117:
	def OWN_CARD_PLAYED(self, card):
		if card.type == CardType.SPELL and card.cost == 1:
			return [Give(CONTROLLER, randomCollectible(race=Race.MECHANICAL))]
