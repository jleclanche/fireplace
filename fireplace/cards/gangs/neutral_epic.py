from ..utils import *


##
# Minions

class CFM_025:
	"""Wind-up Burglebot"""
	events = Attack(SELF, ALL_MINIONS).after(
		Dead(SELF) | Draw(CONTROLLER)
	)


class CFM_064:
	"""Blubber Baron"""
	class Hand:
		events = Play(CONTROLLER, BATTLECRY + MINION).on(
			Buff(SELF, "CFM_064e")
		)


CFM_064e = buff(+1, +1)


class CFM_095:
	"""Weasel Tunneler"""
	deathrattle = Shuffle(OPPONENT, SELF)


class CFM_328:
	"""Fight Promoter"""
	play = Find(FRIENDLY_MINIONS + (CURRENT_HEALTH >= 6)) & Draw(CONTROLLER, 2)


class CFM_609:
	"""Fel Orc Soulfiend"""
	events = OWN_TURN_BEGIN.on(Hit(SELF, 2))


class CFM_669:
	"""Burgly Bully"""
	events = Play(OPPONENT, SPELL).on(Give(CONTROLLER, "GAME_005"))


class CFM_790:
	"""Dirty Rat"""
	play = Summon(OPPONENT, RANDOM(ENEMY_HAND + MINION))


class CFM_810:
	"""Leatherclad Hogleader"""
	play = (Count(ENEMY_HAND) >= 6) & GiveCharge(SELF)


class CFM_855:
	"""Defias Cleaner"""
	requirements = {
		PlayReq.REQ_NONSELF_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
		PlayReq.REQ_TARGET_WITH_DEATHRATTLE: 0}
	play = Silence(TARGET)
