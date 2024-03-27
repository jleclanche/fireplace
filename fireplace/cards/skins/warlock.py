from ..utils import *


##
# Hero Powers

class CS2_056:
	"""Life Tap"""
	activate = Hit(FRIENDLY_HERO, 2), Draw(CONTROLLER)


class CS2_056_H1(CS2_056):
	"""Life Tap (Nemsy Necrofizzle)"""
	pass


class CS2_056_H2(CS2_056):
	"""Life Tap (Mecha-Jaraxxus)"""
	pass


##
# Upgraded Hero Powers

class AT_132_WARLOCK:
	"""Soul Tap"""
	activate = Draw(CONTROLLER)


class AT_132_WARLOCKa(AT_132_WARLOCK):
	"""Soul Tap (Nemsy Necrofizzle)"""
	pass


class AT_132_WARLOCKb(AT_132_WARLOCK):
	"""Soul Tap (Mecha-Jaraxxus)"""
	pass
