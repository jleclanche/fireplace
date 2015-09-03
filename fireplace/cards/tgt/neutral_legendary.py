from ..utils import *


##
# Minions

# Confessor Paletress
class AT_018:
	inspire = Summon(CONTROLLER, RandomMinion(rarity=Rarity.LEGENDARY))


# Skycap'n Kragg
class AT_070:
	cost = lambda self, i: i - len(self.controller.field.filter(race=Race.PIRATE))


# Gormok the Impaler
class AT_122:
	play = Hit(TARGET, 4)


# Chillmaw
class AT_123:
	deathrattle = HOLDING_DRAGON & Hit(ALL_MINIONS, 3)


# Nexus-Champion Saraad
class AT_127:
	inspire = Give(CONTROLLER, RandomSpell())


# The Skeleton Knight
class AT_128:
	deathrattle = JOUST & Bounce(SELF)


# Fjola Lightbane
class AT_129:
	events = Play(CONTROLLER, SPELL, SELF).on(SetTag(SELF, {GameTag.DIVINE_SHIELD: True}))


# Eydis Darkbane
class AT_131:
	events = Play(CONTROLLER, SPELL, SELF).on(Hit(RANDOM_ENEMY_CHARACTER, 3))
