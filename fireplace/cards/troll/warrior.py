from ..utils import *


##
# Minions

class TRL_323:
	"""Emberscale Drake"""
	# <b>Battlecry:</b> If you're holding a Dragon, gain 5 Armor.
	powered_up = HOLDING_DRAGON
	play = powered_up & GainArmor(FRIENDLY_HERO, 5)


class TRL_326:
	"""Smolderthorn Lancer"""
	# <b>Battlecry:</b> If you're holding a Dragon, destroy a damaged enemy minion.
	powered_up = HOLDING_DRAGON
	play = powered_up & Destroy(TARGET)


class TRL_327:
	"""Spirit of the Rhino"""
	# <b>Stealth</b> for 1 turn. Your <b>Rush</b> minions are <b>Immune</b> the turn
	# they're summoned.
	events = OWN_TURN_BEGIN.on(Unstealth(SELF)),
	update = Refresh(
		FRIENDLY_MINIONS + RUSH + THE_TURN_SUMMONED,
		{GameTag.CANT_BE_DAMAGED: True}
	)


class TRL_328:
	"""War Master Voone"""
	# <b>Battlecry:</b> Copy all Dragons in your hand.
	play = Give(CONTROLLER, Copy(FRIENDLY_HAND + DRAGON))


class TRL_329:
	"""Akali, the Rhino"""
	# <b>Rush</b> <b>Overkill:</b> Draw a <b>Rush</b> minion from your deck. Give it +5/+5.
	overkill = ForceDraw(RANDOM(FRIENDLY_DECK + RUSH + MINION)).then(
		Buff(ForceDraw.TARGET, "TRL_329e")
	)


TRL_329e = buff(+5, +5)


##
# Spells

class TRL_321:
	"""Devastate"""
	# Deal $4 damage to a damaged minion.
	play = Hit(TARGET, 4)


class TRL_324:
	"""Heavy Metal!"""
	# [x]Summon a random minion with Cost equal to your Armor <i>(up to 10).</i>
	play = Summon(CONTROLLER, RandomMinion(cost=Max(ARMOR(FRIENDLY_HERO, 10))))


class TRL_362:
	"""Dragon Roar"""
	# Add 2 random Dragons to your hand.
	play = Give(CONTROLLER, RandomDragon()) * 2


##
# Weapons

class TRL_325:
	"""Sul'thraze"""
	# <b>Overkill</b>: You may attack again.
	overkill = ExtraAttack(FRIENDLY_HERO)


class TRL_360:
	"""Overlord's Whip"""
	# After you play a minion, deal 1 damage to it.
	events = Play(CONTROLLER, MINION).after(
		Hit(Play.CARD, 1)
	)
