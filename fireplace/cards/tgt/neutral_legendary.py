from ..utils import *


##
# Minions

class AT_070:
	"""Skycap'n Kragg"""
	cost_mod = -Count(FRIENDLY_MINIONS + PIRATE)


class AT_122:
	"""Gormok the Impaler"""
	requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE_AND_MINIMUM_FRIENDLY_MINIONS: 4}
	play = (Count(FRIENDLY_MINIONS) >= 4) & Hit(TARGET, 4)


class AT_123:
	"""Chillmaw"""
	deathrattle = HOLDING_DRAGON & Hit(ALL_MINIONS, 3)


class AT_124:
	"""Bolf Ramshield"""
	events = Predamage(FRIENDLY_HERO).on(
		Predamage(FRIENDLY_HERO, 0), Hit(SELF, Predamage.AMOUNT)
	)


class AT_125:
	"""Icehowl"""
	tags = {GameTag.CANNOT_ATTACK_HEROES: True}


class AT_127:
	"""Nexus-Champion Saraad"""
	inspire = Give(CONTROLLER, RandomSpell())


class AT_128:
	"""The Skeleton Knight"""
	deathrattle = JOUST & Bounce(SELF)


class AT_129:
	"""Fjola Lightbane"""
	events = Play(CONTROLLER, SPELL, SELF).on(GiveDivineShield(SELF))


class AT_131:
	"""Eydis Darkbane"""
	events = Play(CONTROLLER, SPELL, SELF).on(Hit(RANDOM_ENEMY_CHARACTER, 3))


class AT_132:
	"""Justicar Trueheart"""
	HERO_POWER_MAP = {
		# 德鲁伊
		"CS2_017": "AT_132_DRUID",  # 玛法里奥·怒风
		# 猎人
		"DS1h_292": "AT_132_HUNTER",  # 雷克萨
		"DS1h_292_H1": "DS1h_292_H1_AT_132",  # 奥蕾莉亚·风行者
		# 法师
		"CS2_034": "AT_132_MAGE",  # 吉安娜·普罗德摩尔
		"CS2_034_H1": "CS2_034_H1_AT_132",  # 麦迪文
		"CS2_034_H2": "CS2_034_H2_AT_132",  # 卡德加
		# 圣骑士
		"CS2_101": "AT_132_PALADIN",  # 乌瑟尔·光明使者
		"CS2_101_H": "CS2_101_H1_AT_132",  # 女伯爵莉亚德琳
		# 牧师
		"CS1h_001": "AT_132_PRIEST",  # 安度因·乌瑞恩
		"CS1h_001_H1": "CS1h_001_H1_AT_132",  # 泰兰德·语风
		# 盗贼
		"CS2_083b": "AT_132_ROGUE",  # 瓦莉拉·萨古纳尔
		# 萨满
		"CS2_049": "AT_132_SHAMAN",  # 萨尔
		"CS2_049_H1": "CS2_049_H1_AT_132",  # 神谕者摩戈尔
		# 术士
		"CS2_056": "AT_132_WARLOCK",  # 古尔丹
		# 战士
		"CS2_102": "AT_132_WARRIOR",  # 加尔鲁什·地狱咆哮
		"CS2_102_H1": "CS2_102_H1_AT_132",  # 麦格尼·铜须
	}

	play = Switch(FRIENDLY_HERO_POWER, {
		k: Summon(CONTROLLER, v) for k, v in HERO_POWER_MAP.items()
	})
