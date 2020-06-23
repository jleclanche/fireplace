from ..utils import *


##
# Minions

class AT_010:
	"""Ram Wrangler"""
	powered_up = Find(FRIENDLY_MINIONS + BEAST)
	play = powered_up & Summon(CONTROLLER, RandomBeast())


class AT_057:
	"""Stablemaster"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
		PlayReq.REQ_TARGET_WITH_RACE: 20}
	play = Buff(TARGET, "AT_057o")


AT_057o = buff(immune=True)


class AT_058:
	"""King's Elekk"""
	play = JOUST & Draw(CONTROLLER, Joust.CHALLENGER)


class AT_059:
	"""Brave Archer"""
	inspire = EMPTY_HAND & Hit(ENEMY_HERO, 2)


class AT_063:
	"""Acidmaw"""
	events = Damage(MINION - SELF).on(Destroy(Damage.TARGET))


class AT_063t:
	"""Dreadscale"""
	events = OWN_TURN_END.on(Hit(ALL_MINIONS - SELF, 1))


##
# Spells

class AT_056:
	"""Powershot"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Hit(TARGET | TARGET_ADJACENT, 2)


class AT_061:
	"""Lock and Load"""
	play = Buff(CONTROLLER, "AT_061e")


class AT_061e:
	events = OWN_SPELL_PLAY.on(
		Give(CONTROLLER, RandomCollectible(card_class=CardClass.HUNTER))
	)


class AT_062:
	"""Ball of Spiders"""
	requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
	play = Summon(CONTROLLER, "FP1_011") * 3


##
# Secrets

class AT_060:
	"""Bear Trap"""
	secret = Attack(CHARACTER, FRIENDLY_HERO).after(FULL_BOARD | (
		Reveal(SELF), Summon(CONTROLLER, "CS2_125")
	))
