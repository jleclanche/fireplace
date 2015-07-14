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
	deathrattle = [Summon(CONTROLLER, RandomMinion(rarity=Rarity.LEGENDARY))]


# Toshley
class GVG_115:
	action = deathrattle = [Give(CONTROLLER, RandomSparePart())]


# Mekgineer Thermaplugg
class GVG_116:
	events = [
		Death(ENEMY + MINION).on(Summon(CONTROLLER, "EX1_029"))
	]


# Gazlowe
class GVG_117:
	events = [
		Play(CONTROLLER, SPELL).on(
			lambda self, player, card, *args: card.cost == 1 and [
				Give(player, RandomMinion(race=Race.MECHANICAL))
			] or []
		)
	]


# Troggzor the Earthinator
class GVG_118:
	events = [
		Play(OPPONENT, SPELL).on(Summon(CONTROLLER, "GVG_068"))
	]


# Blingtron 3000
class GVG_119:
	action = [Summon(ALL_PLAYERS, RandomWeapon())]


# Hemet Nesingwary
class GVG_120:
	action = [Destroy(TARGET)]
