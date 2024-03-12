from ..utils import *


##
# Minions

class DAL_060:
	"""Clockwork Goblin"""
	# [x]<b>Battlecry:</b> Shuffle a Bomb into your opponent's deck. When drawn, it
	# explodes for 5 damage.
	play = Shuffle(OPPONENT, "BOT_511t")


class DAL_064:
	"""Blastmaster Boom"""
	# [x]<b>Battlecry:</b> Summon two 1/1 Boom Bots for each Bomb in your opponent's deck.
	pass


class DAL_070:
	"""The Boom Reaver"""
	# <b>Battlecry:</b> Summon a copy of a minion in your deck. Give it <b>Rush</b>.
	pass


class DAL_759:
	"""Vicious Scraphound"""
	# Whenever this minion deals damage, gain that much Armor.
	pass


class DAL_770:
	"""Omega Devastator"""
	# [x]<b>Battlecry:</b> If you have 10 Mana Crystals, deal 10 damage to a minion.
	pass


##
# Spells

class DAL_008:
	"""Dr. Boom's Scheme"""
	# Gain @ Armor. <i>(Upgrades each turn!)</i>
	pass


class DAL_059:
	"""Dimensional Ripper"""
	# Summon 2 copies of a minion in your deck.
	pass


class DAL_062:
	"""Sweeping Strikes"""
	# Give a minion "Also damages minions next to whomever this attacks."
	pass


class DAL_769:
	"""Improve Morale"""
	# [x]Deal $1 damage to a minion. If it survives, add a <b>Lackey</b> to your hand.
	play = Hit(TARGET, 1), Dead(TARGET) | Give(CONTROLLER, RandomLackey())


##
# Weapons

class DAL_063:
	"""Wrenchcalibur"""
	# After your hero attacks, shuffle a Bomb into your [x]opponent's deck.
	events = Attack(FRIENDLY_HERO).after(Shuffle(OPPONENT, "BOT_511t"))
