from ..utils import *


##
# Minions

class TRL_405:
	"""Untamed Beastmaster"""
	# Whenever you draw a Beast, give it +2/+2.
	events = Draw(CONTROLLER, BEAST).on(
		Buff(Draw.TARGET, "TRL_405e")
	)


TRL_405e = buff(+2, +2)


class TRL_516:
	"""Gurubashi Offering"""
	# At the start of your turn, destroy this and gain 8_Armor.
	events = OWN_TURN_BEGIN.on(Destroy(SELF), GainArmor(FRIENDLY_HERO, 8))


class TRL_527:
	"""Drakkari Trickster"""
	# [x]<b>Battlecry:</b> Give each player a copy of a random card from their opponent's
	# deck.
	play = (
		Give(CONTROLLER, ExactCopy(RANDOM(FRIENDLY_DECK))),
		Give(OPPONENT, ExactCopy(RANDOM(ENEMY_DECK))),
	)

class TRL_528:
	"""Linecracker"""
	# <b>Overkill:</b> Double this minion's Attack.
	overkill = Buff(SELF, "TRL_528e")


class TRL_528e:
	atk = lambda self, i: i * 2


class TRL_530:
	"""Masked Contender"""
	# <b>Battlecry:</b> If you control a_<b>Secret</b>, play a <b>Secret</b> from_your
	# deck.
	play = Find(FRIENDLY_SECRETS) & Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + SECRET))


class TRL_532:
	"""Mosh'Ogg Announcer"""
	# [x]Enemies attacking this have a 50% chance to attack someone else.
	# TODO need test
	events = Attack(ENEMY_CHARACTERS, SELF).on(
		COINFLIP & Retarget(Attack.ATTACKER, RANDOM(FRIENDLY_CHARACTERS - SELF))
	)


class TRL_533:
	"""Ice Cream Peddler"""
	# <b>Battlecry:</b> If you control a_<b>Frozen</b> minion, gain 8_Armor.
	play = Find(FRIENDLY_MINIONS + FROZEN) & GainArmor(FRIENDLY_HERO, 8)


class TRL_535:
	"""Snapjaw Shellfighter"""
	# [x]Whenever an adjacent minion takes damage, this _minion takes it instead.
	events = Predamage(SELF_ADJACENT).on(
		Predamage(Predamage.TARGET, 0), Hit(SELF, Predamage.AMOUNT)
	)


class TRL_569:
	"""Crowd Roaster"""
	# [x]<b>Battlecry:</b> If you're holding a Dragon, deal 7 damage to an enemy minion.
	powered_up = HOLDING_DRAGON
	play = powered_up & Hit(TARGET, 7)
