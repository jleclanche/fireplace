from ..utils import *


##
# Hero Powers

# Shapeshift
class CS2_017:
	activate = Buff(FRIENDLY_HERO, "CS2_017o"), GainArmor(FRIENDLY_HERO, 1)


##
# Minions

# Cat Form (Druid of the Claw)
class EX1_165a:
	play = Morph(SELF, "EX1_165t1")

# Bear Form (Druid of the Claw)
class EX1_165b:
	play = Morph(SELF, "EX1_165t2")


# Moonfire (Keeper of the Grove)
class EX1_166a:
	play = Hit(TARGET, 2)

# Dispel (Keeper of the Grove)
class EX1_166b:
	play = Silence(TARGET)


# Rooted (Ancient of War)
class EX1_178a:
	play = Buff(SELF, "EX1_178ae")

# Uproot (Ancient of War)
class EX1_178b:
	play = Buff(SELF, "EX1_178be")


# Demigod's Favor (Cenarius)
class EX1_573a:
	play = Buff(FRIENDLY_MINIONS, "EX1_573ae")

# Shan'do's Lesson (Cenarius)
class EX1_573b:
	play = Summon(CONTROLLER, "EX1_573t") * 2


# Ancient Teachings (Ancient of Lore)
class NEW1_008a:
	play = Draw(CONTROLLER) * 2

# Ancient Secrets (Ancient of Lore)
class NEW1_008b:
	play = Heal(TARGET, 5)


##
# Spells

# Claw
class CS2_005:
	play = Buff(FRIENDLY_HERO, "CS2_005o"), GainArmor(FRIENDLY_HERO, 2)


# Healing Touch
class CS2_007:
	play = Heal(TARGET, 8)


# Moonfire
class CS2_008:
	play = Hit(TARGET, 1)


# Mark of the Wild
class CS2_009:
	play = Buff(TARGET, "CS2_009e")


# Savage Roar
class CS2_011:
	play = Buff(FRIENDLY_CHARACTERS, "CS2_011o")


# Swipe
class CS2_012:
	play = Hit(TARGET, 4), Hit(ENEMY_CHARACTERS - TARGET, 1)


# Wild Growth
class CS2_013:
	def play(self):
		if self.controller.max_mana < self.controller.max_resources:
			return GainEmptyMana(CONTROLLER, 1)
		else:
			return Give(CONTROLLER, "CS2_013t")

class CS2_013t:
	play = Draw(CONTROLLER)


# Wrath (3 Damage)
class EX1_154a:
	play = Hit(TARGET, 3)

# Wrath (1 Damage)
class EX1_154b:
	play = Hit(TARGET, 1), Draw(CONTROLLER)


# Mark of Nature (Attack)
class EX1_155a:
	play = Buff(TARGET, "EX1_155ae")

# Mark of Nature (Health)
class EX1_155b:
	play = Buff(TARGET, "EX1_155be")


# Soul of the Forest
class EX1_158:
	play = Buff(FRIENDLY_MINIONS, "EX1_158e")

class EX1_158e:
	deathrattle = Summon(CONTROLLER, "EX1_158t")


# Summon a Panther (Power of the Wild)
class EX1_160a:
	play = Summon(CONTROLLER, "EX1_160t")

# Leader of the Pack (Power of the Wild)
class EX1_160b:
	play = Buff(FRIENDLY_MINIONS, "EX1_160be")


# Naturalize
class EX1_161:
	play = Destroy(TARGET), Draw(OPPONENT) * 2


# Nourish (Gain 2 Mana Crystals)
class EX1_164a:
	play = GainMana(CONTROLLER, 2)

# Nourish (Draw 3 cards)
class EX1_164b:
	play = Draw(CONTROLLER) * 3


# Innervate
class EX1_169:
	play = ManaThisTurn(CONTROLLER, 2)


# Starfire
class EX1_173:
	play = Hit(TARGET, 5), Draw(CONTROLLER)


# Bite
class EX1_570:
	play = Buff(FRIENDLY_HERO, "EX1_570e"), GainArmor(FRIENDLY_HERO, 4)


# Force of Nature
class EX1_571:
	play = Summon(CONTROLLER, "EX1_tk9") * 3

class EX1_tk9:
	events = TURN_END.on(Destroy(SELF))


# Savagery
class EX1_578:
	play = Hit(TARGET, Attr(FRIENDLY_HERO, GameTag.ATK))


# Starfall (2 Damage to All)
class NEW1_007a:
	play = Hit(ENEMY_MINIONS, 2)

# Starfall (5 Damage to One)
class NEW1_007b:
	play = Hit(TARGET, 5)
