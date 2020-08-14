from ..utils import *


##
# Minions

class BT_407:
	"""Ur'zul Horror"""
	deathrattle = Give(CONTROLLER, "BT_407t")


class BT_351:
	"""Battlefiend"""
	events = Attack(FRIENDLY_HERO).after(Buff(SELF, "BT_351e"))


BT_351e = buff(atk=1)


class BT_355:
	"""Wrathscale Naga"""
	events = Death(FRIENDLY + MINION).on(Hit(RANDOM_ENEMY_CHARACTER, 3))


class BT_814:
	"""Illidari Felblade"""
	outcast = Buff(SELF, "BT_814e")


BT_814e = buff(immune=True)


class BT_416:
	"""Raging Felscreamer"""
	play = Buff(CONTROLLER, "BT_416e")


class BT_416e:
	update = Refresh(FRIENDLY_HAND + DEMON, {GameTag.COST: -2})
	events = Play(CONTROLLER, DEMON).on(Destroy(SELF))


class BT_937:
	"""Altruis the Outcast"""
	events = Play(CONTROLLER, OUTERMOST_HAND).after(Hit(ENEMY_CHARACTERS, 1))


class BT_510:
	"""Wrathspike Brute"""
	events = Attack(ALL_CHARACTERS, SELF).after(Hit(ENEMY_CHARACTERS, 1))


class BT_487:
	"""Hulking Overfiend"""
	events = Attack(SELF, ALL_MINIONS).after(
		Dead(ALL_MINIONS + Attack.DEFENDER) & ExtraAttack(SELF)
	)


class BT_481:
	"""Nethrandamus"""
	class Hand:
		events = Death(FRIENDLY + MINION).on(Upgrade(SELF))
	play = Summon(CONTROLLER, RandomMinion(cost=min(10, UPGRADE_COUNTER(SELF)))) * 2


##
# Spells

class BT_752:
	"""Blur"""
	play = Buff(CONTROLLER, "BT_752e")


BT_752e = buff(immune=True)


class BT_175:
	"""Twin Slice"""
	play = Buff(CONTROLLER, "BT_175e"), Give(CONTROLLER, "BT_175t")


class BT_175t:
	play = Buff(CONTROLLER, "BT_175e")


BT_175e = buff(atk=2)


class BT_490:
	"""Consume Magic"""
	requirements = {
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_ENEMY_TARGET: 0,
		PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Silence(TARGET)
	outcast = Silence(TARGET), Draw(CONTROLLER)


class BT_801:
	"""Eye Beam"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Hit(TARGET, 3)
	update = Refresh(OUTERMOST_HAND + SELF, {GameTag.COST: SET(1)})


class BT_753:
	"""Mana Burn"""
	play = Buff(OPPONENT, "BT_753e")


class BT_753e:
	events = TURN_BEGIN.on(ManaThisTurn(OWNER, -2), Destroy(SELF))


class BT_354:
	"""Blade Dance"""
	requirements = {PlayReq.REQ_MINIMUM_ENEMY_MINIONS: 1}
	play = Hit(RANDOM_ENEMY_MINION * 2, ATK(FRIENDLY_HERO))


class BT_427:
	"""Feast of Souls"""
	play = Draw(CONTROLLER) * Count(FRIENDLY + MINION + KILLED_THIS_TURN)


class BT_488:
	"""Soul Split"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_TO_PLAY: 0,
		PlayReq.REQ_TARGET_WITH_RACE: Race.DEMON
	}
	play = Summon(CONTROLLER, ExactCopy(TARGET))


class BT_173:
	"""Command the Illidari"""
	play = Summon(CONTROLLER, "BT_036t") * 6


##
# Weapons

class BT_922:
	"""Umberwing"""
	play = Summon(CONTROLLER, "BT_922t") * 2


class BT_271:
	"""Flamereaper"""
	events = Attack(FRIENDLY_HERO).on(
		Hit(ADJACENT(ATTACK_TARGET), ATK(SELF), source=FRIENDLY_HERO))
