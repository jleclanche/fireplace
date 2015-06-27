from ..utils import *


##
# Hero Powers

# Shapeshift
class CS2_017:
	activate = [Buff(FRIENDLY_HERO, "CS2_017o"), GainArmor(FRIENDLY_HERO, 1)]


##
# Minions

# Cat Form (Druid of the Claw)
class EX1_165a:
	action = [Morph(SELF, "EX1_165t1")]

# Bear Form (Druid of the Claw)
class EX1_165b:
	action = [Morph(SELF, "EX1_165t2")]


# Moonfire (Keeper of the Grove)
class EX1_166a:
	action = [Hit(TARGET, 2)]

# Dispel (Keeper of the Grove)
class EX1_166b:
	action = [Silence(TARGET)]


# Rooted (Ancient of War)
class EX1_178a:
	action = [Buff(SELF, "EX1_178ae")]

# Uproot (Ancient of War)
class EX1_178b:
	action = [Buff(SELF, "EX1_178be")]


# Demigod's Favor (Cenarius)
class EX1_573a:
	action = [Buff(FRIENDLY_MINIONS, "EX1_573ae")]

# Shan'do's Lesson (Cenarius)
class EX1_573b:
	action = [Summon(CONTROLLER, "EX1_573t") * 2]


# Ancient Teachings (Ancient of Lore)
class NEW1_008a:
	action = [Draw(CONTROLLER) * 2]

# Ancient Secrets (Ancient of Lore)
class NEW1_008b:
	action = [Heal(TARGET, 5)]


##
# Spells

# Claw
class CS2_005:
	action = [Buff(FRIENDLY_HERO, "CS2_005o"), GainArmor(FRIENDLY_HERO, 2)]


# Healing Touch
class CS2_007:
	action = [Heal(TARGET, 8)]


# Moonfire
class CS2_008:
	action = [Hit(TARGET, 1)]


# Mark of the Wild
class CS2_009:
	action = [Buff(TARGET, "CS2_009e")]


# Savage Roar
class CS2_011:
	action = [Buff(FRIENDLY_CHARACTERS, "CS2_011o")]


# Swipe
class CS2_012:
	action = [Hit(TARGET, 4), Hit(ENEMY_CHARACTERS - TARGET, 1)]


# Wild Growth
class CS2_013:
	def action(self):
		if self.controller.max_mana < self.controller.max_resources:
			return [GainMana(CONTROLLER, 1)]
		else:
			return [Give(CONTROLLER, "CS2_013t")]

class CS2_013t:
	action = [Draw(CONTROLLER)]


# Wrath (3 Damage)
class EX1_154a:
	action = [Hit(TARGET, 3)]

# Wrath (1 Damage)
class EX1_154b:
	action = [Hit(TARGET, 1), Draw(CONTROLLER)]


# Mark of Nature (Attack)
class EX1_155a:
	action = [Buff(TARGET, "EX1_155ae")]

# Mark of Nature (Health)
class EX1_155b:
	action = [Buff(TARGET, "EX1_155be")]


# Soul of the Forest
class EX1_158:
	action = [Buff(FRIENDLY_MINIONS, "EX1_158e")]

class EX1_158e:
	deathrattle = [Summon(CONTROLLER, "EX1_158t")]


# Summon a Panther (Power of the Wild)
class EX1_160a:
	action = [Summon(CONTROLLER, "EX1_160t")]

# Leader of the Pack (Power of the Wild)
class EX1_160b:
	action = [Buff(FRIENDLY_MINIONS, "EX1_160be")]


# Naturalize
class EX1_161:
	action = [Destroy(TARGET), Draw(OPPONENT) * 2]


# Nourish (Gain 2 Mana Crystals)
class EX1_164a:
	action = [GainMana(CONTROLLER, 2)]

# Nourish (Draw 3 cards)
class EX1_164b:
	action = [Draw(CONTROLLER) * 3]


# Innervate
class EX1_169:
	action = [ManaThisTurn(CONTROLLER, 2)]


# Starfire
class EX1_173:
	action = [Hit(TARGET, 5), Draw(CONTROLLER)]


# Bite
class EX1_570:
	action = [Buff(FRIENDLY_HERO, "EX1_570e"), GainArmor(FRIENDLY_HERO, 4)]


# Force of Nature
class EX1_571:
	action = [Summon(CONTROLLER, "EX1_tk9") * 3]

class EX1_tk9:
	events = [
		TURN_END.on(Destroy(SELF))
	]


# Savagery
class EX1_578:
	def action(self, target):
		return [Hit(TARGET, self.controller.hero.atk)]


# Starfall (2 Damage to All)
class NEW1_007a:
	action = [Hit(ENEMY_MINIONS, 2)]

# Starfall (5 Damage to One)
class NEW1_007b:
	action = [Hit(TARGET, 2)]
