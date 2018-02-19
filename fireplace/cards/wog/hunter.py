from ..utils import *


##
# Minions

class OG_179:
	"Fiery Bat"
	deathrattle = Hit(RANDOM_ENEMY_CHARACTER, 1)


class OG_292:
	"Forlorn Stalker"
	play = Buff(FRIENDLY_HAND + MINION + DEATHRATTLE, "OG_292e")

OG_292e = buff(+1, +1)


class OG_216:
	"Infested Wolf"
	deathrattle = Summon(CONTROLLER, "OG_216a") * 2


class OG_308:
	"Giant Sand Worm"
	events = Attack(SELF, ALL_MINIONS).after(
		Dead(ALL_MINIONS + Attack.DEFENDER) & ExtraAttack(SELF)
	)

class OG_309:
	"Princess Huhuran"
	play = Deathrattle(TARGET)


##
# Spells

class OG_045:
	"Infest"
	play = Buff(FRIENDLY_MINIONS, "OG_045a")

class OG_045a:
	"Nerubian Spores"
	deathrattle = Give(CONTROLLER, RandomBeast())
	tags = {GameTag.DEATHRATTLE: True}


class OG_061:
	"On the Hunt"
	play = Hit(TARGET, 1), Summon(CONTROLLER, "OG_061t")


class OG_211:
	"Call of the Wild"
	play = (
		Summon(CONTROLLER, "NEW1_034"),
		Summon(CONTROLLER, "NEW1_033"),
		Summon(CONTROLLER, "NEW1_032")
	)
