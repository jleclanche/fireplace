from ..utils import *


##
# Minions

class TRL_071:
	"""Bloodsail Howler"""
	# [x]<b>Rush</b> <b>Battlecry:</b> Gain +1/+1 for each other Pirate you control.
	play = Buff(SELF, "TRL_071e") * Count(FRIENDLY_MINIONS + PIRATE)


TRL_071e = buff(+1, +1)


class TRL_077:
	"""Gurubashi Hypemon"""
	# <b>Battlecry:</b> <b>Discover</b> a 1/1 copy of a <b>Battlecry</b> minion. It costs
	# (1).
	play = Discover(CONTROLLER, RandomMinion(battlecry=True)).then(
		Give(CONTROLLER, Buff(Discover.CARD, "TRL_077e"))
	)


class TRL_077e:
	cost = SET(1)
	atk = SET(1)
	max_health = SET(1)


class TRL_092:
	"""Spirit of the Shark"""
	# [x]<b>Stealth</b> for 1 turn. Your minions' <b>Battlecries</b> __and <b>Combos</b>
	# trigger twice._
	events = (
		OWN_TURN_BEGIN.on(Unstealth(SELF)),
		Refresh(CONTROLLER, {enums.EXTRA_BATTLECRIES: True}),
		Refresh(CONTROLLER, {enums.EXTRA_COMBOS: True}),
	)


class TRL_126:
	"""Captain Hooktusk"""
	# <b>Battlecry:</b> Summon 3 Pirates from your deck. Give them <b>Rush</b>.
	play = Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + PIRATE) * 3).then(
		Buff(Summon.CARD, "TRL_126e")
	)


TRL_126e = buff(rush=True)


class TRL_409:
	"""Gral, the Shark"""
	# [x]<b>Battlecry:</b> Eat a minion in your deck and gain its stats.
	# <b>Deathrattle:</b> Add it to your hand.
	play = (
		Retarget(SELF, RANDOM(FRIENDLY_DECK + MINION)),
		Reveal(TARGET),
		Destroy(TARGET),
		Buff(SELF, "TRL_409e", atk=ATK(TARGET), max_health=CURRENT_HEALTH(TARGET))
	)
	deathrattle = Give(CONTROLLER, Copy(TARGET))


##
# Spells

class TRL_124:
	"""Raiding Party"""
	# Draw 2 Pirates from_your deck. <b>Combo:</b> And a weapon.
	play = ForceDraw(RANDOM(FRIENDLY_DECK + PIRATE) * 2)
	combo = (
		ForceDraw(RANDOM(FRIENDLY_DECK + PIRATE) * 2),
		ForceDraw(RANDOM(FRIENDLY_DECK + WEAPON))
	)


class TRL_127:
	"""Cannon Barrage"""
	# [x]Deal $3 damage to a random enemy. Repeat for each of your Pirates.
	play = Hit(RANDOM_ENEMY_CHARACTER, 3) * (Count(FRIENDLY_MINIONS + PIRATE) + Number(1))


class TRL_156:
	"""Stolen Steel"""
	# <b>Discover</b> a weapon <i>(from another class)</i>.
	# TODO need test
	play = GenericChoice(
		CONTROLLER,
		RandomWeapon(card_class=ANOTHER_CLASS) * 3
	)


class TRL_157:
	"""Walk the Plank"""
	# Destroy an undamaged minion.
	play = Destroy(TARGET)


##
# Weapons

class TRL_074:
	"""Serrated Tooth"""
	# <b>Deathrattle:</b> Give your minions <b>Rush</b>.
	deathrattle = Buff(FRIENDLY_MINIONS, "TRL_074e")


TRL_074e = buff(rush=True)
