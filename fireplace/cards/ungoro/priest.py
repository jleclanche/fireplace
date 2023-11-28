from ..utils import *


##
# Minions

class UNG_022:
	"""Mirage Caller"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	play = Summon(CONTROLLER, ExactCopy(TARGET)).then(
		Buff(Summon.CARD, "UNG_022e")
	)


class UNG_022e:
	atk = SET(1)
	max_health = SET(1)


class UNG_032:
	"""Crystalline Oracle"""
	deathrattle = Give(CONTROLLER, Copy(RANDOM(ENEMY_DECK)))


class UNG_034:
	"""Radiant Elemental"""
	update = Refresh(FRIENDLY_HAND + SPELL, {GameTag.COST: -1})


class UNG_035:
	"""Curious Glimmerroot"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0}
	play = GlimmerrootAction(CONTROLLER)


class UNG_037:
	"""Tortollan Shellraiser"""
	deathrattle = Buff(RANDOM(FRIENDLY_MINIONS), "UNG_037e")


UNG_037e = buff(+1, +1)


class UNG_963:
	"""Lyra the Sunshard"""
	events = Play(CONTROLLER, SPELL).after(
		Give(CONTROLLER, RandomSpell(card_class=CardClass.PRIEST)))


##
# Spells

class UNG_029:
	"""Shadow Visions"""
	# TODO: need test
	play = GenericChoice(CONTROLLER, Copy(RANDOM(DeDuplicate(FRIENDLY_DECK)) * 3))


class UNG_030:
	"""Binding Heal"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Heal(FRIENDLY_HERO, 5), Heal(TARGET, 5)


class UNG_854:
	"""Free From Amber"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_NUM_MINION_SLOTS: 1,
		PlayReq.REQ_TARGET_WITH_DEATHRATTLE: 0}
	play = Discover(CONTROLLER, RandomMinion(cost=list(range(8, 25)))).then(
		Summon(CONTROLLER, Discover.CARD)
	)


class UNG_940:
	"""Awaken the Makers"""
	# TODO: need test
	progress_total = 7
	quest = Summon(CONTROLLER, DEATHRATTLE).after(AddProgress(SELF, Summon.CARD))
	reward = Give(CONTROLLER, "UNG_940t8")


class UNG_940t8:
	requirements = {PlayReq.REQ_HERO_TARGET: 0, PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	play = Buff(FRIENDLY_HERO, "UNG_940t8e")


@custom_card
class UNG_940t8e:
	tags = {
		GameTag.CARDNAME: "Amara, Warden of Hope Buff",
		GameTag.CARDTYPE: CardType.ENCHANTMENT,
	}
	max_health = SET(40)
