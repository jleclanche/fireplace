from ..utils import *


##
# Hero Powers

class CS2_083b:
	"""Dagger Mastery"""
	activate = Summon(CONTROLLER, "CS2_082")


class CS2_083b_H1(CS2_083b):
	"""Dagger Mastery (Maiev Shadowsong)"""
	pass


##
# Upgraded Hero Powers

class AT_132_ROGUE:
	"""Poisoned Daggers"""
	activate = Summon(CONTROLLER, "AT_132_ROGUEt")


class AT_132_ROGUE_H1:
	"""Poisoned Daggers (Maiev Shadowsong)"""
	activate = Summon(CONTROLLER, "AT_132_ROGUEt_H1")
