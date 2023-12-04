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
		# Druid
		"CS2_017": "AT_132_DRUID",  # Malfurion Stormrage
		# Hunter
		"DS1h_292": "AT_132_HUNTER",  # Rexxar
		"DS1h_292_H1": "DS1h_292_H1_AT_132",  # Alleria Windrunner
		# Mage
		"CS2_034": "AT_132_MAGE",  # Jaina Proudmoore
		"CS2_034_H1": "CS2_034_H1_AT_132",  # Medivh
		"CS2_034_H2": "CS2_034_H2_AT_132",  # Khadgar
		# Paladin
		"CS2_101": "AT_132_PALADIN",  # Uther Lightbringer
		"CS2_101_H1": "CS2_101_H1_AT_132",  # Lady Liadrin
		"CS2_101_H2": "CS2_101_H2_AT_132",  # Prince Arthas
		# Priest
		"CS1h_001": "AT_132_PRIEST",  # Anduin Wrynn
		"CS1h_001_H1": "CS1h_001_H1_AT_132",  # Tyrande Whisperwind
		# Rogue
		"CS2_083b": "AT_132_ROGUE",  # Valeera Sanguinar
		# Shaman
		"CS2_049": "AT_132_SHAMAN",  # Thrall
		"CS2_049_H1": "CS2_049_H1_AT_132",  # Morgl the Oracle
		# Warlock
		"CS2_056": "AT_132_WARLOCK",  # Gul'dan
		# Warrior
		"CS2_102": "AT_132_WARRIOR",  # Garrosh Hellscream
		"CS2_102_H1": "CS2_102_H1_AT_132",  # Magni Bronzebeard
	}

	play = Switch(FRIENDLY_HERO_POWER, {
		k: Summon(CONTROLLER, v) for k, v in HERO_POWER_MAP.items()
	})
