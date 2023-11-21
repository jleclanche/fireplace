from ..utils import *


##
# Minions

class CFM_321:
	"""Grimestreet Informant"""
	play = GenericChoice(CONTROLLER, [
		RandomCollectible(card_class=CardClass.HUNTER),
		RandomCollectible(card_class=CardClass.PALADIN),
		RandomCollectible(card_class=CardClass.WARRIOR)
	])


class CFM_325:
	"""Small-Time Buccaneer"""
	update = Find(FRIENDLY_WEAPON) & Refresh(SELF, buff="CFM_325e")


CFM_325e = buff(atk=2)


class CFM_649:
	"""Kabal Courier"""
	play = GenericChoice(CONTROLLER, [
		RandomCollectible(card_class=CardClass.MAGE),
		RandomCollectible(card_class=CardClass.PRIEST),
		RandomCollectible(card_class=CardClass.WARLOCK)
	])


class CFM_652:
	"""Second-Rate Bruiser"""
	class Hand:
		update = (Count(ENEMY_MINIONS) >= 3) & Refresh(SELF, {GameTag.COST: -2})


class CFM_658:
	"""Backroom Bouncer"""
	events = Death(FRIENDLY + MINION).on(Buff(SELF, "CFM_658e"))


CFM_658e = buff(atk=1)


class CFM_667:
	"""Bomb Squad"""
	requirements = {
		PlayReq.REQ_ENEMY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	play = Hit(TARGET, 5)
	deathrattle = Hit(FRIENDLY_HERO, 5)


class CFM_668:
	"""Doppelgangster"""
	play = (
		(Summon(CONTROLLER, ExactCopy(SELF)) * 2).then(
			Find(SELF, ID("CFM_668")) & (
				Find(LEFT_OF(SELF) + ID("CFM_668")) &
				Morph(LEFT_OF(SELF), ExactCopy(LEFT_OF(SELF), "CFM_668t")),
				Find(RIGHT_OF(SELF) + ID("CFM_668")) &
				Morph(RIGHT_OF(SELF), ExactCopy(RIGHT_OF(SELF), "CFM_668t2"))
			)  # WTF
		)
	)


class CFM_688:
	"""Spiked Hogrider"""
	powered_up = Find(ENEMY_MINIONS + TAUNT)
	play = powered_up & GiveCharge(SELF)


class CFM_852:
	"""Lotus Agents"""
	play = GenericChoice(CONTROLLER, [
		RandomCollectible(card_class=CardClass.DRUID),
		RandomCollectible(card_class=CardClass.ROGUE),
		RandomCollectible(card_class=CardClass.SHAMAN)
	])
