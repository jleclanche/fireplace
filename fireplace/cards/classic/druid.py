from ..utils import *


##
# Hero Powers

class CS2_017:
	"Shapeshift"
	activate = Buff(FRIENDLY_HERO, "CS2_017o"), GainArmor(FRIENDLY_HERO, 1)

CS2_017o = buff(atk=1)


##
# Minions

class EX1_165:
	"Druid of the Claw"
	choose = ("EX1_165a", "EX1_165b")
	play = ChooseBoth(CONTROLLER) & Morph(SELF, "OG_044a")

class EX1_165a:
	play = Morph(SELF, "EX1_165t1")

class EX1_165b:
	play = Morph(SELF, "EX1_165t2")


class EX1_166:
	"Keeper of the Grove"
	choose = ("EX1_166a", "EX1_166b")
	play = ChooseBoth(CONTROLLER) & (Hit(TARGET, 2), Silence(TARGET))

class EX1_166a:
	play = Hit(TARGET, 2)

class EX1_166b:
	play = Silence(TARGET)


class EX1_178:
	"Ancient of War"
	choose = ("EX1_178b", "EX1_178a")
	play = ChooseBoth(CONTROLLER) & (Buff(SELF, "EX1_178ae"), Buff(SELF, "EX1_178be"))

class EX1_178a:
	play = Buff(SELF, "EX1_178ae")

EX1_178ae = buff(health=5, taunt=True)

class EX1_178b:
	play = Buff(SELF, "EX1_178be")

EX1_178be = buff(atk=5)


class EX1_573:
	"Cenarius"
	choose = ("EX1_573a", "EX1_573b")
	play = ChooseBoth(CONTROLLER) & (Buff(FRIENDLY_MINIONS, "EX1_573ae"), Summon(CONTROLLER, "EX1_573t") * 2)

class EX1_573a:
	play = Buff(FRIENDLY_MINIONS, "EX1_573ae")

EX1_573ae = buff(+2, +2)

class EX1_573b:
	play = Summon(CONTROLLER, "EX1_573t") * 2


class NEW1_008:
	"Ancient of Lore"
	choose = ("NEW1_008a", "NEW1_008b")
	play = ChooseBoth(CONTROLLER) & (Draw(CONTROLLER), Heal(TARGET, 5))

class NEW1_008a:
	play = Draw(CONTROLLER)

class NEW1_008b:
	play = Heal(TARGET, 5)


##
# Spells

class CS2_005:
	"Claw"
	play = Buff(FRIENDLY_HERO, "CS2_005o"), GainArmor(FRIENDLY_HERO, 2)

CS2_005o = buff(atk=2)


class CS2_007:
	"Healing Touch"
	play = Heal(TARGET, 8)


class CS2_008:
	"Moonfire"
	play = Hit(TARGET, 1)


class CS2_009:
	"Mark of the Wild"
	play = Buff(TARGET, "CS2_009e")

CS2_009e = buff(+2, +2, taunt=True)


class CS2_011:
	"Savage Roar"
	play = Buff(FRIENDLY_CHARACTERS, "CS2_011o")

CS2_011o = buff(atk=2)


class CS2_012:
	"Swipe"
	play = Hit(TARGET, 4), Hit(ENEMY_CHARACTERS - TARGET, 1)


class CS2_013:
	"Wild Growth"
	play = (
		AT_MAX_MANA(CONTROLLER) &
		Give(CONTROLLER, "CS2_013t") |
		GainEmptyMana(CONTROLLER, 1)
	)

class CS2_013t:
	play = Draw(CONTROLLER)


class EX1_154:
	"Wrath"
	choose = ("EX1_154a", "EX1_154b")
	play = ChooseBoth(CONTROLLER) & (Hit(TARGET, 3), Hit(TARGET, 1), Draw(CONTROLLER))

class EX1_154a:
	"Wrath (3 Damage)"
	play = Hit(TARGET, 3)

class EX1_154b:
	"Wrath (1 Damage)"
	play = Hit(TARGET, 1), Draw(CONTROLLER)


class EX1_155:
	"Mark of Nature"
	choose = ("EX1_155a", "EX1_155b")
	play = ChooseBoth(CONTROLLER) & (Buff(TARGET, "EX1_155ae"), Buff(TARGET, "EX1_155be"))

class EX1_155a:
	play = Buff(TARGET, "EX1_155ae")

EX1_155ae = buff(atk=4)

class EX1_155b:
	play = Buff(TARGET, "EX1_155be")

EX1_155be = buff(health=4, taunt=True)


class EX1_158:
	"Soul of the Forest"
	play = Buff(FRIENDLY_MINIONS, "EX1_158e")

class EX1_158e:
	deathrattle = Summon(CONTROLLER, "EX1_158t")
	tags = {GameTag.DEATHRATTLE: True}


class EX1_160:
	"Power of the Wild"
	choose = ("EX1_160a", "EX1_160b")
	play = ChooseBoth(CONTROLLER) & (Summon(CONTROLLER, "EX1_160t"), Buff(FRIENDLY_MINIONS, "EX1_160be"))

class EX1_160a:
	play = Summon(CONTROLLER, "EX1_160t")

class EX1_160b:
	play = Buff(FRIENDLY_MINIONS, "EX1_160be")

EX1_160be = buff(+1, +1)


class EX1_161:
	"Naturalize"
	play = Destroy(TARGET), Draw(OPPONENT) * 2


class EX1_164:
	"Nourish"
	choose = ("EX1_164a", "EX1_164b")
	play = ChooseBoth(CONTROLLER) & (GainMana(CONTROLLER, 2), Draw(CONTROLLER) * 3)

class EX1_164a:
	play = GainMana(CONTROLLER, 2)

class EX1_164b:
	play = Draw(CONTROLLER) * 3


class EX1_169:
	"Innervate"
	play = ManaThisTurn(CONTROLLER, 2)


class EX1_173:
	"Starfire"
	play = Hit(TARGET, 5), Draw(CONTROLLER)


class EX1_570:
	"Bite"
	play = Buff(FRIENDLY_HERO, "EX1_570e"), GainArmor(FRIENDLY_HERO, 4)

EX1_570e = buff(atk=4)


class EX1_571:
	"Force of Nature"
	play = Summon(CONTROLLER, "EX1_tk9") * 3


class EX1_578:
	"Savagery"
	play = Hit(TARGET, ATK(FRIENDLY_HERO))


class NEW1_007:
	"Starfall"
	choose = ("NEW1_007a", "NEW1_007b")
	play = ChooseBoth(CONTROLLER) & (Hit(ENEMY_MINIONS, 2), Hit(TARGET, 5))


class NEW1_007a:
	play = Hit(ENEMY_MINIONS, 2)

class NEW1_007b:
	play = Hit(TARGET, 5)
