from ..utils import *


##
# Minions

class UNG_085:
	"""Emerald Hive Queen"""
	update = Refresh(FRIENDLY_HAND + MINION, {GameTag.COST: +2})


class UNG_087:
	"""Bittertide Hydra"""
	events = Damage(SELF).on(Hit(FRIENDLY_HERO, 3))


class UNG_088:
	"""Tortollan Primalist"""
	play = DISCOVER(RandomSpell()).then(CastSpell(Discover.CARD))


class UNG_089:
	"""Gentle Megasaur"""
	play = Adapt(FRIENDLY_MINIONS + MURLOC)


class UNG_099:
	"""Charged Devilsaur"""
	play = Buff(SELF, "UNG_099e")


@custom_card
class UNG_099e:
	tags = {
		GameTag.CARDNAME: "Can't attack heroes this turn",
		GameTag.TAG_ONE_TURN_EFFECT: True,
		GameTag.CANNOT_ATTACK_HEROES: True,
		GameTag.CARDTYPE: CardType.ENCHANTMENT,
	}


class UNG_113:
	"""Bright-Eyed Scout"""
	play = Draw(CONTROLLER).then(Buff(Draw.CARD, "UNG_113e"))


class UNG_113e:
	cost = SET(5)
	events = REMOVED_IN_PLAY


class UNG_847:
	"""Blazecaller"""
	requirements = {
		PlayReq.REQ_NONSELF_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABE_AND_ELEMENTAL_PLAYED_LAST_TURN: 0}
	play = Hit(TARGET, 5)


class UNG_848:
	"""Primordial Drake"""
	play = Hit(ALL_MINIONS, 2)


class UNG_946:
	"""Gluttonous Ooze"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_WITH_DEATHRATTLE: 0}
	play = Destroy(ENEMY_WEAPON).then(GainArmor(CONTROLLER, ATK(Destroy.TARGET)))
