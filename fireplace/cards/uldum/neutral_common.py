from ..utils import *


##
# Minions

class ULD_174:
	"""Serpent Egg"""
	# <b>Deathrattle:</b> Summon a 3/4 Sea Serpent.
	pass


class ULD_179:
	"""Phalanx Commander"""
	# Your <b>Taunt</b> minions have +2 Attack.
	pass


class ULD_182:
	"""Spitting Camel"""
	# [x]At the end of your turn, __deal 1 damage to another__ random friendly minion.
	pass


class ULD_183:
	"""Anubisath Warbringer"""
	# <b>Deathrattle:</b> Give all minions in your hand +3/+3.
	pass


class ULD_184:
	"""Kobold Sandtrooper"""
	# <b>Deathrattle:</b> Deal 3 damage to the enemy_hero.
	pass


class ULD_185:
	"""Temple Berserker"""
	# <b>Reborn</b> Has +2 Attack while damaged.
	pass


class ULD_188:
	"""Golden Scarab"""
	# <b><b>Battlecry:</b> Discover</b> a 4-Cost card.
	pass


class ULD_189:
	"""Faceless Lurker"""
	# <b>Taunt</b> <b>Battlecry:</b> Double this minion's Health.
	pass


class ULD_190:
	"""Pit Crocolisk"""
	# <b>Battlecry:</b> Deal 5 damage.
	requirements = {
		PlayReq.REQ_TARGET_TO_PLAY: 0,
	}
	pass


class ULD_191:
	"""Beaming Sidekick"""
	# <b>Battlecry:</b> Give a friendly minion +2 Health.
	requirements = {
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
	}
	pass


class ULD_271:
	"""Injured Tol'vir"""
	# <b>Taunt</b> <b>Battlecry:</b> Deal 3 damage to this minion.
	pass


class ULD_282:
	"""Jar Dealer"""
	# [x]<b>Deathrattle:</b> Add a random 1-Cost minion to your hand.
	pass


class ULD_289:
	"""Fishflinger"""
	# <b>Battlecry:</b> Add a random Murloc to each player's_hand.
	pass


class ULD_712:
	"""Bug Collector"""
	# <b>Battlecry:</b> Summon a 1/1 Locust with <b>Rush</b>.
	pass


class ULD_719:
	"""Desert Hare"""
	# <b>Battlecry:</b> Summon two 1/1 Desert Hares.
	pass
