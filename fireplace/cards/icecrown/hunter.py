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
	play = Hit(TARGET, 2), Dead(TARGET) | GivePoisonous(TARGET)


class ICC_052:
	"""Play Dead"""
	play = Deathrattle(TARGET)


class ICC_200:
	"""Venomstrike Trap"""
	secret = Attack(ALL_MINIONS, FRIENDLY_MINIONS).on(FULL_BOARD | (
		Reveal(SELF), Summon(CONTROLLER, "EX1_170")
	))


##
# Heros

class ICC_828:
	"""Deathstalker Rexxar"""
	play = Hit(ENEMY_MINIONS, 2)


class ICC_828p:
	activate = CreateZombeast(CONTROLLER)
