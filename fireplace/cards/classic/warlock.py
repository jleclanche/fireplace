from ..utils import *


##
# Hero Powers

# Life Tap
class CS2_056:
	activate = Hit(FRIENDLY_HERO, 2), Draw(CONTROLLER)


##
# Minions

# Blood Imp
class CS2_059:
	events = OWN_TURN_END.on(Buff(RANDOM_OTHER_FRIENDLY_MINION, "CS2_059o"))

CS2_059o = buff(health=1)


# Dread Infernal
class CS2_064:
	play = Hit(ALL_CHARACTERS - SELF, 1)


# Felguard
class EX1_301:
	play = GainEmptyMana(CONTROLLER, -1)


# Void Terror
class EX1_304:
	play = (
		Buff(SELF, "EX1_304e", atk=ATK(SELF_ADJACENT), max_health=CURRENT_HEALTH(SELF_ADJACENT)),
		Destroy(SELF_ADJACENT)
	)


# Succubus
class EX1_306:
	play = Discard(RANDOM(FRIENDLY_HAND))


# Doomguard
class EX1_310:
	play = Discard(RANDOM(FRIENDLY_HAND) * 2)


# Pit Lord
class EX1_313:
	play = Hit(FRIENDLY_HERO, 5)


# Summoning Portal
class EX1_315:
	update = Refresh(FRIENDLY_HAND + MINION, {
		GameTag.COST: lambda self, i: min(i, max(1, i - 2))
	})


# Flame Imp
class EX1_319:
	play = Hit(FRIENDLY_HERO, 3)


# Lord Jaraxxus
class EX1_323:
	play = (
		Summon(CONTROLLER, "EX1_323h").then(Morph(SELF, Summon.CARDS)),
		Summon(CONTROLLER, "EX1_323w")
	)

# INFERNO!
class EX1_tk33:
	activate = Summon(CONTROLLER, "EX1_tk34")


##
# Spells

# Drain Life
class CS2_061:
	play = Hit(TARGET, 2), Heal(FRIENDLY_HERO, 2)


# Hellfire
class CS2_062:
	play = Hit(ALL_CHARACTERS, 3)


# Corruption
class CS2_063:
	play = Buff(TARGET, "CS2_063e")

class CS2_063e:
	events = OWN_TURN_BEGIN.on(Destroy(OWNER))


# Shadow Bolt
class CS2_057:
	play = Hit(TARGET, 4)


# Mortal Coil
class EX1_302:
	play = Hit(TARGET, 1), Dead(TARGET) & Draw(CONTROLLER)


# Shadowflame
class EX1_303:
	play = Hit(ENEMY_MINIONS, ATK(TARGET)), Destroy(TARGET)


# Soulfire
class EX1_308:
	play = Hit(TARGET, 4), Discard(RANDOM(FRIENDLY_HAND))


# Siphon Soul
class EX1_309:
	play = Destroy(TARGET), Heal(FRIENDLY_HERO, 3)


# Twisting Nether
class EX1_312:
	play = Destroy(ALL_MINIONS)


# Power Overwhelming
class EX1_316:
	play = Buff(TARGET, "EX1_316e")

class EX1_316e:
	events = TURN_END.on(Destroy(OWNER))
	tags = {
		GameTag.ATK: +4,
		GameTag.HEALTH: +4,
	}


# Sense Demons
class EX1_317:
	play = (
		Find(FRIENDLY_DECK + DEMON) &
		ForceDraw(RANDOM(FRIENDLY_DECK + DEMON)) |
		Give(CONTROLLER, "EX1_317t"),
	) * 2


# Bane of Doom
class EX1_320:
	play = Hit(TARGET, 2), Dead(TARGET) & Summon(CONTROLLER, RandomMinion(race=Race.DEMON))


# Demonfire
class EX1_596:
	play = Find(TARGET + FRIENDLY + DEMON) & Buff(TARGET, "EX1_596e") | Hit(TARGET, 2)

EX1_596e = buff(+2, +2)


# Sacrificial Pact
class NEW1_003:
	play = Destroy(TARGET), Heal(FRIENDLY_HERO, 5)
