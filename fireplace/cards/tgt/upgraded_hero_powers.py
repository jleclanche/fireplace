"""
Upgraded Hero Powers from Justicar Trueheart (AT_132)
"""
from ..utils import *


##
# Hero Powers

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


class AT_132_HUNTER:
	"""Ballista Shot"""
	requirements = {PlayReq.REQ_MINION_OR_ENEMY_HERO: 0, PlayReq.REQ_STEADY_SHOT: 0}
	activate = Hit(ENEMY_HERO, 3)


class DS1h_292_H1_AT_132(AT_132_HUNTER):
	"""Ballista Shot (Alleria Windrunner)"""
	pass


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


class AT_132_PALADIN:
	"""The Silver Hand"""
	requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
	activate = Summon(CONTROLLER, "CS2_101t") * 2


class CS2_101_H1_AT_132(AT_132_PALADIN):
	"""The Silver Hand (Lady Liadrin)"""
	pass


class CS2_101_H2_AT_132(AT_132_PALADIN):
	"""The Silver Hand (Prince Arthas)"""
	pass


class CS2_101_H3_AT_132(AT_132_PALADIN):
	"""The Silver Hand (Sir Annoy-O)"""
	pass


class AT_132_PRIEST:
	"""Heal"""
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
	activate = Heal(TARGET, 4)


class CS1h_001_H1_AT_132(AT_132_PRIEST):
	"""Heal (Tyrande Whisperwind)"""
	pass


class CS1h_001_H2_AT_132(AT_132_PRIEST):
	"""Heal (Madame Lazul)"""
	pass


class AT_132_ROGUE:
	"""Poisoned Daggers"""
	activate = Summon(CONTROLLER, "AT_132_ROGUEt")


class AT_132_ROGUE_H1:
	"""Poisoned Daggers (Maiev Shadowsong)"""
	activate = Summon(CONTROLLER, "AT_132_ROGUEt_H1")


class AT_132_WARRIOR:
	"""Tank Up!"""
	activate = GainArmor(FRIENDLY_HERO, 4)


class CS2_102_H1_AT_132(AT_132_WARRIOR):
	"""Tank Up! (Magni Bronzebeard)"""
	pass


class AT_132_WARLOCK:
	"""Soul Tap"""
	activate = Draw(CONTROLLER)


class AT_132_WARLOCKa(AT_132_WARLOCK):
	"""Soul Tap (Nemsy Necrofizzle)"""
	pass


class AT_132_WARLOCKb(AT_132_WARLOCK):
	"""Soul Tap (Mecha-Jaraxxus)"""
	pass


class AT_132_SHAMAN:
	"""Totemic Slam"""
	requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
	choose = ("AT_132_SHAMANa", "AT_132_SHAMANb", "AT_132_SHAMANc", "AT_132_SHAMANd")


class CS2_049_H1_AT_132(AT_132_SHAMAN):
	"""Totemic Slam (Morgl the Oracle)"""
	pass


class CS2_049_H2_AT_132(AT_132_SHAMAN):
	"""Totemic Slam (King Rastakhan)"""
	pass


class CS2_049_H3_AT_132(AT_132_SHAMAN):
	"""Totemic Slam (The Thunder King)"""
	pass


class AT_132_SHAMANa:
	"""Healing Totem"""
	play = Summon(CONTROLLER, "NEW1_009")


class AT_132_SHAMANb:
	"""Searing Totem"""
	play = Summon(CONTROLLER, "CS2_050")


class AT_132_SHAMANc:
	"""Stoneclaw Totem"""
	play = Summon(CONTROLLER, "CS2_051")


class AT_132_SHAMANd:
	"""Wrath of Air Totem"""
	play = Summon(CONTROLLER, "CS2_052")
