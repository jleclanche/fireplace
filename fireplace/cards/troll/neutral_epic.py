from ..utils import *


##
# Minions

class TRL_405:
	"""Untamed Beastmaster"""
	# Whenever you draw a Beast, give it +2/+2.
	pass


class TRL_516:
	"""Gurubashi Offering"""
	# At the start of your turn, destroy this and gain 8_Armor.
	pass


class TRL_527:
	"""Drakkari Trickster"""
	# [x]<b>Battlecry:</b> Give each player a copy of a random card from their opponent's
	# deck.
	pass


class TRL_528:
	"""Linecracker"""
	# <b>Overkill:</b> Double this minion's Attack.
	pass


class TRL_530:
	"""Masked Contender"""
	# <b>Battlecry:</b> If you control a_<b>Secret</b>, play a <b>Secret</b> from_your
	# deck.
	pass


class TRL_532:
	"""Mosh'Ogg Announcer"""
	# [x]Enemies attacking this have a 50% chance to attack someone else.
	events = Attack(ENEMY_CHARACTERS, SELF).on(
		COINFLIP & Retarget(Attack.ATTACKER, RANDOM(FRIENDLY_CHARACTERS - SELF))
	)


class TRL_533:
	"""Ice Cream Peddler"""
	# <b>Battlecry:</b> If you control a_<b>Frozen</b> minion, gain 8_Armor.
	pass


class TRL_535:
	"""Snapjaw Shellfighter"""
	# [x]Whenever an adjacent minion takes damage, this _minion takes it instead.
	events = Predamage(SELF_ADJACENT).on(
		Predamage(Predamage.TARGET, 0), Hit(SELF, Predamage.AMOUNT)
	)


class TRL_569:
	"""Crowd Roaster"""
	# [x]<b>Battlecry:</b> If you're holding a Dragon, deal 7 damage to an enemy minion.
	pass
