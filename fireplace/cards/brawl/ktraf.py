"""
An Evil Exchange
"""
from ..utils import *


# Necromancy
class TB_KTRAF_HP_KT_3:
	activate = Summon(CONTROLLER, Copy(RANDOM(FRIENDLY + KILLED + MINION)))


# Anub'Rekhan
class TB_KTRAF_1:
	events = OWN_TURN_END.on(Summon(CONTROLLER, "NAX1_03"))


# Lady Blaumeux
class TB_KTRAF_2:
	play = Summon(CONTROLLER, "TB_KTRAF_2s")


# Sir Zeliek
class TB_KTRAF_2s:
	update = Refresh(ALL_MINIONS + ID("TB_KTRAF_2"), {GameTag.CANT_BE_DAMAGED: True})


# Gluth
class TB_KTRAF_3:
	events = OWN_TURN_END.on(Summon(CONTROLLER, RandomEntourage()))


# Gothik the Harvester
class TB_KTRAF_4:
	deathrattle = Summon(OPPONENT, "TB_KTRAF_4m")

class TB_KTRAF_4m:
	events = OWN_TURN_BEGIN.on(Hit(FRIENDLY_HERO, 4))


# Grand Widow Faerlina
class TB_KTRAF_5:
	update = Refresh(SELF, {GameTag.ATK: lambda self, i: self.health})


# Grobbulus
class TB_KTRAF_6:
	events = Death(ENEMY + MINION, source=SELF).on(Summon(CONTROLLER, "TB_KTRAF_6m"))


# Heigan the Unclean
class TB_KTRAF_7:
	events = OWN_TURN_END.on(Hit(RANDOM_ENEMY_CHARACTER, 4))


# Instructor Razuvious
class TB_KTRAF_8:
	play = Summon(CONTROLLER, "TB_KTRAF_08w")


# Massive Runeblade
class TB_KTRAF_08w:
	update = Attacking(FRIENDLY_HERO, HERO) & Refresh(SELF, {GameTag.ATK: +5})


# Noth the Plaguebringer
class TB_KTRAF_10:
	events = Death(ENEMY + MINION).on(
		Summon(CONTROLLER, "NAX4_03"), Buff(FRIENDLY_MINIONS - SELF, "TB_KTRAF_10e")
	)

TB_KTRAF_10e = buff(+1, +1)


# Sapphiron
class TB_KTRAF_11:
	events = OWN_TURN_BEGIN.on(Freeze(RANDOM_ENEMY_MINION))


# Patchwerk
class TB_KTRAF_12:
	play = Destroy(RANDOM_ENEMY_MINION)


# Darkness Calls
class TB_KTRAF_101:
	play = Summon(CONTROLLER, RandomEntourage()).then(Battlecry(Summon.CARD)) * 2


# Uncover Staff Piece
class TB_KTRAF_104:
	play = Switch(FRIENDLY_HERO_POWER, {
		"TB_KTRAF_HP_RAF3": Summon(CONTROLLER, "TB_KTRAF_HP_RAF4"),
		"TB_KTRAF_HP_RAF4": Summon(CONTROLLER, "TB_KTRAF_HP_RAF5")
	})
