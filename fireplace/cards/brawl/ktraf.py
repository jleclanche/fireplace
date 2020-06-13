"""
An Evil Exchange
"""
from ..utils import *


class TB_KTRAF_HP_KT_3:
	"""Necromancy"""
	activate = Summon(CONTROLLER, Copy(RANDOM(FRIENDLY + KILLED + MINION)))


class TB_KTRAF_1:
	"""Anub'Rekhan"""
	events = OWN_TURN_END.on(Summon(CONTROLLER, "NAX1_03"))


class TB_KTRAF_2:
	"""Lady Blaumeux"""
	play = Summon(CONTROLLER, "TB_KTRAF_2s")


class TB_KTRAF_2s:
	"""Sir Zeliek"""
	update = Refresh(ALL_MINIONS + ID("TB_KTRAF_2"), {GameTag.CANT_BE_DAMAGED: True})


class TB_KTRAF_3:
	"""Gluth"""
	entourage = [
		"FP1_001", "AT_030", "LOE_019", "EX1_012", "EX1_059",
		"FP1_004", "EX1_616", "FP1_024", "tt_004"]
	events = OWN_TURN_END.on(Summon(CONTROLLER, RandomEntourage()))


class TB_KTRAF_4:
	"""Gothik the Harvester"""
	deathrattle = Summon(OPPONENT, "TB_KTRAF_4m")


class TB_KTRAF_4m:
	events = OWN_TURN_BEGIN.on(Hit(FRIENDLY_HERO, 4))


class TB_KTRAF_5:
	"""Grand Widow Faerlina"""
	update = Refresh(SELF, {GameTag.ATK: lambda self, i: self.health})


class TB_KTRAF_6:
	"""Grobbulus"""
	events = Death(ENEMY + MINION, source=SELF).on(Summon(CONTROLLER, "TB_KTRAF_6m"))


class TB_KTRAF_7:
	"""Heigan the Unclean"""
	events = OWN_TURN_END.on(Hit(RANDOM_ENEMY_CHARACTER, 4))


class TB_KTRAF_8:
	"""Instructor Razuvious"""
	play = Summon(CONTROLLER, "TB_KTRAF_08w")


class TB_KTRAF_08w:
	"""Massive Runeblade"""
	update = Attacking(FRIENDLY_HERO, HERO) & Refresh(SELF, {GameTag.ATK: +5})


class TB_KTRAF_10:
	"""Noth the Plaguebringer"""
	events = Death(ENEMY + MINION).on(
		Summon(CONTROLLER, "NAX4_03"), Buff(FRIENDLY_MINIONS - SELF, "TB_KTRAF_10e")
	)


TB_KTRAF_10e = buff(+1, +1)


class TB_KTRAF_11:
	"""Sapphiron"""
	events = OWN_TURN_BEGIN.on(Freeze(RANDOM_ENEMY_MINION))


class TB_KTRAF_12:
	"""Patchwerk"""
	play = Destroy(RANDOM_ENEMY_MINION)


class TB_KTRAF_101:
	"""Darkness Calls"""
	entourage = [
		"TB_KTRAF_1", "TB_KTRAF_3", "TB_KTRAF_4", "TB_KTRAF_5", "TB_KTRAF_6", "TB_KTRAF_7",
		"TB_KTRAF_8", "TB_KTRAF_2", "TB_KTRAF_10", "TB_KTRAF_12", "TB_KTRAF_11"]
	play = Summon(CONTROLLER, RandomEntourage()).then(Battlecry(Summon.CARD)) * 2


class TB_KTRAF_104:
	"""Uncover Staff Piece"""
	play = Switch(FRIENDLY_HERO_POWER, {
		"TB_KTRAF_HP_RAF3": Summon(CONTROLLER, "TB_KTRAF_HP_RAF4"),
		"TB_KTRAF_HP_RAF4": Summon(CONTROLLER, "TB_KTRAF_HP_RAF5")
	})
