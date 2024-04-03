from ..utils import *


##
# Hero Powers

class CS2_034:
	"""Fireblast (Jaina Proudmoore)"""
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
	activate = Hit(TARGET, 1)


class CS2_034_H1:
	"""Fireblast (Medivh)"""
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
	activate = CS2_034.activate


class CS2_034_H2:
	"""Fireblast (Khadgar)"""
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
	activate = CS2_034.activate


##
# Upgraded Hero Powers

class AT_132_MAGE:
	"""Fireblast Rank 2"""
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
	activate = Hit(TARGET, 2)


class CS2_034_H1_AT_132(AT_132_MAGE):
	"""Fireblast Rank 2 (Medivh)"""
	pass


class CS2_034_H2_AT_132(AT_132_MAGE):
	"""Fireblast Rank 2 (Khadgar)"""
	pass
