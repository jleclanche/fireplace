from ..utils import *


##
# Minions

class ICC_021:
	"""Exploding Bloatbat"""
	deathrattle = Hit(ENEMY_MINIONS, 2)


class ICC_204:
	"""Professor Putricide"""
	events = Play(CONTROLLER, SECRET).after(
		Summon(CONTROLLER, RandomSpell(
			secret=True,
			card_class=CardClass.HUNTER,
			exclude=FRIENDLY_SECRETS)))


class ICC_243:
	"""Corpse Widow"""
	update = Refresh(FRIENDLY_HAND + DEATHRATTLE, {GameTag.COST: -2})


class ICC_415:
	"""Stitched Tracker"""
	play = GenericChoice(CONTROLLER, Copy(RANDOM(DeDuplicate(FRIENDLY_DECK + MINION)) * 3))


class ICC_825:
	"""Abominable Bowman"""
	deathrattle = Summon(CONTROLLER, Copy(FRIENDLY + KILLED + BEAST))


##
# Spells

class ICC_049:
	"""Toxic Arrow"""
	requirements = {
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_TO_PLAY: 0,
	}
	play = Hit(TARGET, 2), Dead(TARGET) | GivePoisonous(TARGET)


class ICC_052:
	"""Play Dead"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_WITH_DEATHRATTLE: 0,
		PlayReq.REQ_TARGET_TO_PLAY: 0,
	}
	play = Deathrattle(TARGET)


class ICC_200:
	"""Venomstrike Trap"""
	secret = Attack(None, FRIENDLY_MINIONS).on(FULL_BOARD | (
		Reveal(SELF), Summon(CONTROLLER, "EX1_170")
	))


##
# Heros

class ICC_828:
	"""Deathstalker Rexxar"""
	play = Hit(ENEMY_MINIONS, 2)


class ICC_828p:
	requirements = {
		PlayReq.REQ_HAND_NOT_FULL: 0,
	}
	activate = CreateZombeast(CONTROLLER)
