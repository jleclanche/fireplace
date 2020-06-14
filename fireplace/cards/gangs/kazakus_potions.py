from ..utils import *


##
# Potions

class CFM_621t2:
	"""Heart of Fire"""
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
	# 1 Cost: Deal 3
	play = Hit(TARGET, 3)


class CFM_621t3:
	"""Stonescale Oil"""
	# 1 Cost: Gain 4 Armor
	play = GainArmor(FRIENDLY_HERO, 4)


class CFM_621t4:
	"""Felbloom"""
	# 1 Cost: 2 AOE
	play = Hit(ALL_MINIONS, 2)


class CFM_621t5:
	"""Icecap"""
	# 1 Cost: Freeze 1
	play = Freeze(RANDOM_ENEMY_MINION)


class CFM_621t6:
	"""Goldthorn"""
	# 1 Cost: +2 Health
	play = Buff(FRIENDLY_MINIONS, "CFM_621e")


CFM_621e = buff(health=2)


class CFM_621t8:
	"""Kingsblood"""
	# 1 Cost: Draw 1
	play = Draw(CONTROLLER)


class CFM_621t9:
	"""Shadow Oil"""
	# 1 Cost: Add 1 Demon
	play = Give(CONTROLLER, RandomDemon())


class CFM_621t10:
	"""Netherbloom"""
	# 1 Cost: Summon 2/2
	play = Summon(CONTROLLER, "CFM_621_m4")


class CFM_621t16:
	"""Heart of Fire"""
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
	# 5 Cost: Deal 5 Dmg
	play = Hit(TARGET, 5)


class CFM_621t17:
	"""Stonescale Oil"""
	# 5 Cost: Gain 7 Armor
	play = GainArmor(FRIENDLY_HERO, 7)


class CFM_621t18:
	"""Felbloom"""
	# 5 Cost: AOE 4
	play = Hit(ALL_MINIONS, 4)


class CFM_621t19:
	"""Icecap"""
	# 5 Cost: Freeze 2
	play = Freeze(RANDOM_ENEMY_MINION * 2)


class CFM_621t20:
	"""Netherbloom"""
	# 5 Cost: Summon 5/5
	play = Summon(CONTROLLER, "CFM_621_m2")


class CFM_621t21:
	"""Mystic Wool"""
	requirements = {PlayReq.REQ_MINIMUM_TOTAL_MINIONS: 1}
	# 5 Cost: Polymorph 1
	play = Morph(RANDOM_ENEMY_MINION, "CFM_621_m5")


class CFM_621t22:
	"""Kingsblood"""
	# 5 Cost: Draw 2
	play = Draw(CONTROLLER) * 2


class CFM_621t23:
	"""Shadow Oil"""
	# 5 Cost: Add 2 Demons
	play = Give(CONTROLLER, RandomDemon()) * 2


class CFM_621t24:
	"""Goldthorn"""
	# 5 Cost: +4 Health
	play = Buff(FRIENDLY_MINIONS, "CFM_621e2")


CFM_621e2 = buff(health=4)


class CFM_621t25:
	"""Heart of Fire"""
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
	# 10 Cost: Deal 10
	play = Hit(TARGET, 10)


class CFM_621t26:
	"""Stonescale Oil"""
	# 10 Cost: Gain 10 Armor
	play = GainArmor(FRIENDLY_HERO, 10)


class CFM_621t27:
	"""Icecap"""
	# 10 Cost: Freeze 3
	play = Freeze(RANDOM_ENEMY_MINION * 3)


class CFM_621t28:
	"""Netherbloom"""
	# 10 Cost: Summon 8/8
	play = Summon(CONTROLLER, "CFM_621_m3")


class CFM_621t29:
	"""Mystic Wool"""
	# 10 Cost: Polymorph all
	play = Morph(ALL_MINIONS, "CFM_621_m5")


class CFM_621t30:
	"""Kingsblood"""
	# 10 Cost: Draw 3
	play = Draw(CONTROLLER) * 3


class CFM_621t31:
	"""Shadow Oil"""
	# 10 Cost: Add 3 Demons
	play = Give(CONTROLLER, RandomDemon()) * 3


class CFM_621t32:
	"""Goldthorn"""
	# 10 Cost: +6 Health
	play = Buff(FRIENDLY_MINIONS, "CFM_621e3")


CFM_621e3 = buff(health=6)


class CFM_621t33:
	"""Felbloom"""
	# 10 Cost: 6 AOE
	play = Hit(ALL_MINIONS, 6)


class CFM_621t37:
	"""Ichor of Undeath"""
	# 1 Cost: Revive 1
	play = Summon(CONTROLLER, Copy(RANDOM(FRIENDLY + KILLED + MINION)))


class CFM_621t38:
	"""Ichor of Undeath"""
	# 5 Cost: Revive 2
	play = Summon(CONTROLLER, Copy(RANDOM(FRIENDLY + KILLED + MINION) * 2))


class CFM_621t39:
	"""Ichor of Undeath"""
	# 10 Cost: Revive 3
	play = Summon(CONTROLLER, Copy(RANDOM(FRIENDLY + KILLED + MINION) * 3))
