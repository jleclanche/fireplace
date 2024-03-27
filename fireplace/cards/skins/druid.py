from ..utils import *


##
# Hero Powers

class CS2_017:
	"""Shapeshift"""
	activate = Buff(FRIENDLY_HERO, "CS2_017o"), GainArmor(FRIENDLY_HERO, 1)


CS2_017o = buff(atk=1)


class CS2_017_HS1(CS2_017):
	"""Shapeshift (Lunara)"""
	pass


class CS2_017_HS2(CS2_017):
	"""Shapeshift (Elise Starseeker)"""
	pass


class CS2_017_HS4(CS2_017):
	"""Shapeshift (Dame Hazelbark)"""
	pass


##
# Upgraded Hero Powers

class AT_132_DRUID:
	"""Dire Shapeshift"""
	activate = Buff(FRIENDLY_HERO, "AT_132_DRUIDe"), GainArmor(FRIENDLY_HERO, 2)


AT_132_DRUIDe = buff(atk=2)


class AT_132_DRUIDa(AT_132_DRUID):
	"""Dire Shapeshift (Lunara)"""
	pass


class AT_132_DRUIDb(AT_132_DRUID):
	"""Dire Shapeshift (Elise Starseeker)"""
	pass


class AT_132_DRUIDc(AT_132_DRUID):
	"""Dire Shapeshift (Dame Hazelbark)"""
	pass
