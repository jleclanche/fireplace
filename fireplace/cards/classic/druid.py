from ..utils import *


##
# Hero Powers

# Shapeshift
class CS2_017:
	activate = Buff(FRIENDLY_HERO, "CS2_017o"), GainArmor(FRIENDLY_HERO, 1)

CS2_017o = buff(atk=1)


##
# Minions

# Druid of the Claw
class EX1_165:
	choose = ("EX1_165a", "EX1_165b")

class EX1_165a:
	play = Morph(SELF, "EX1_165t1")

class EX1_165b:
	play = Morph(SELF, "EX1_165t2")


# Keeper of the Grove
class EX1_166:
	choose = ("EX1_166a", "EX1_166b")

class EX1_166a:
	play = Hit(TARGET, 2)

class EX1_166b:
	play = Silence(TARGET)


# Ancient of War
class EX1_178:
	choose = ("EX1_178b", "EX1_178a")

class EX1_178a:
	play = Buff(SELF, "EX1_178ae")

EX1_178ae = buff(health=5, taunt=True)

class EX1_178b:
	play = Buff(SELF, "EX1_178be")

EX1_178be = buff(atk=5)


# Cenarius
class EX1_573:
	choose = ("EX1_573a", "EX1_573b")

class EX1_573a:
	play = Buff(FRIENDLY_MINIONS, "EX1_573ae")

EX1_573ae = buff(+2, +2)

class EX1_573b:
	play = Summon(CONTROLLER, "EX1_573t") * 2


# Ancient of Lore
class NEW1_008:
	choose = ("NEW1_008a", "NEW1_008b")

class NEW1_008a:
	play = Draw(CONTROLLER)

class NEW1_008b:
	play = Heal(TARGET, 5)


##
# Spells

# Claw
class CS2_005:
	play = Buff(FRIENDLY_HERO, "CS2_005o"), GainArmor(FRIENDLY_HERO, 2)

CS2_005o = buff(atk=2)


# Healing Touch
class CS2_007:
	play = Heal(TARGET, 8)


# Moonfire
class CS2_008:
	play = Hit(TARGET, 1)


# Mark of the Wild
class CS2_009:
	play = Buff(TARGET, "CS2_009e")

CS2_009e = buff(+2, +2, taunt=True)


# Savage Roar
class CS2_011:
	play = Buff(FRIENDLY_CHARACTERS, "CS2_011o")

CS2_011o = buff(atk=2)


# Swipe
class CS2_012:
	play = Hit(TARGET, 4), Hit(ENEMY_CHARACTERS - TARGET, 1)


# Wild Growth
class CS2_013:
	play = (
		AT_MAX_MANA(CONTROLLER) &
		Give(CONTROLLER, "CS2_013t") |
		GainEmptyMana(CONTROLLER, 1)
	)

class CS2_013t:
	play = Draw(CONTROLLER)


# Wrath
class EX1_154:
	choose = ("EX1_154a", "EX1_154b")

# Wrath (3 Damage)
class EX1_154a:
	play = Hit(TARGET, 3)

# Wrath (1 Damage)
class EX1_154b:
	play = Hit(TARGET, 1), Draw(CONTROLLER)


# Mark of Nature
class EX1_155:
	choose = ("EX1_155a", "EX1_155b")

class EX1_155a:
	play = Buff(TARGET, "EX1_155ae")

EX1_155ae = buff(atk=4)

class EX1_155b:
	play = Buff(TARGET, "EX1_155be")

EX1_155be = buff(health=4, taunt=True)


# Soul of the Forest
class EX1_158:
	play = Buff(FRIENDLY_MINIONS, "EX1_158e")

class EX1_158e:
	deathrattle = Summon(CONTROLLER, "EX1_158t")
	tags = {GameTag.DEATHRATTLE: True}


# Power of the Wild
class EX1_160:
	choose = ("EX1_160a", "EX1_160b")

class EX1_160a:
	play = Summon(CONTROLLER, "EX1_160t")

class EX1_160b:
	play = Buff(FRIENDLY_MINIONS, "EX1_160be")

EX1_160be = buff(+1, +1)


# Naturalize
class EX1_161:
	play = Destroy(TARGET), Draw(OPPONENT) * 2


# Nourish
class EX1_164:
	choose = ("EX1_164a", "EX1_164b")

class EX1_164a:
	play = GainMana(CONTROLLER, 2)

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

EX1_570e = buff(atk=4)


# Force of Nature
class EX1_571:
	play = Summon(CONTROLLER, "EX1_tk9") * 3


# Savagery
class EX1_578:
	play = Hit(TARGET, ATK(FRIENDLY_HERO))


# Starfall
class NEW1_007:
	choose = ("NEW1_007a", "NEW1_007b")

class NEW1_007a:
	play = Hit(ENEMY_MINIONS, 2)

class NEW1_007b:
	play = Hit(TARGET, 5)
