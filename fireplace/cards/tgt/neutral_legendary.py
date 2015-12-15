from ..utils import *


##
# Minions

# Confessor Paletress
class AT_018:
	inspire = Summon(CONTROLLER, RandomMinion(rarity=Rarity.LEGENDARY))


# Skycap'n Kragg
class AT_070:
	cost_mod = -Count(FRIENDLY_MINIONS + PIRATE)


# Gormok the Impaler
class AT_122:
	play = (Count(FRIENDLY_MINIONS) >= 4) & Hit(TARGET, 4)


# Chillmaw
class AT_123:
	deathrattle = HOLDING_DRAGON & Hit(ALL_MINIONS, 3)


# Bolf Ramshield
class AT_124:
	events = Predamage(FRIENDLY_HERO).on(
		Predamage(FRIENDLY_HERO, 0), Hit(SELF, Predamage.AMOUNT)
	)


# Nexus-Champion Saraad
class AT_127:
	inspire = Give(CONTROLLER, RandomSpell())


# The Skeleton Knight
class AT_128:
	deathrattle = JOUST & Bounce(SELF)


# Fjola Lightbane
class AT_129:
	events = Play(CONTROLLER, SPELL, SELF).on(GiveDivineShield(SELF))


# Eydis Darkbane
class AT_131:
	events = Play(CONTROLLER, SPELL, SELF).on(Hit(RANDOM_ENEMY_CHARACTER, 3))


# Justicar Trueheart
class AT_132:
	HERO_POWER_MAP = {
		"CS2_017": "AT_132_DRUID",
		"DS1h_292": "AT_132_HUNTER",
		"DS1h_292_H1": "DS1h_292_H1_AT_132",
		"CS2_034": "AT_132_MAGE",
		"CS2_101": "AT_132_PALADIN",
		"CS1h_001": "AT_132_PRIEST",
		"CS2_083b": "AT_132_ROGUE",
		"CS2_049": "AT_132_SHAMAN",
		"CS2_056": "AT_132_WARLOCK",
		"CS2_102": "AT_132_WARRIOR",
		"CS2_102_H1": "CS2_102_H1_AT_132",
	}

	def play(self):
		upgrade = AT_132.HERO_POWER_MAP.get(self.controller.hero.power.id)
		if upgrade:
			yield Summon(CONTROLLER, upgrade)
