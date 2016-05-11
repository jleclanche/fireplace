from ..utils import *


##
# Hero Powers

class CS2_056:
	"Life Tap"
	activate = Hit(FRIENDLY_HERO, 2), Draw(CONTROLLER)


##
# Minions

class CS2_059:
	"Blood Imp"
	events = OWN_TURN_END.on(Buff(RANDOM_OTHER_FRIENDLY_MINION, "CS2_059o"))

CS2_059o = buff(health=1)


class CS2_064:
	"Dread Infernal"
	play = Hit(ALL_CHARACTERS - SELF, 1)


class EX1_301:
	"Felguard"
	play = GainEmptyMana(CONTROLLER, -1)


class EX1_304:
	"Void Terror"
	play = (
		Buff(SELF, "EX1_304e", atk=ATK(SELF_ADJACENT), max_health=CURRENT_HEALTH(SELF_ADJACENT)),
		Destroy(SELF_ADJACENT)
	)


class EX1_306:
	"Succubus"
	play = Discard(RANDOM(FRIENDLY_HAND))


class EX1_310:
	"Doomguard"
	play = Discard(RANDOM(FRIENDLY_HAND) * 2)


class EX1_313:
	"Pit Lord"
	play = Hit(FRIENDLY_HERO, 5)


class EX1_315:
	"Summoning Portal"
	update = Refresh(FRIENDLY_HAND + MINION, {
		GameTag.COST: lambda self, i: min(i, max(1, i - 2))
	})


class EX1_319:
	"Flame Imp"
	play = Hit(FRIENDLY_HERO, 3)


class EX1_323:
	"Lord Jaraxxus"
	play = (
		Summon(CONTROLLER, "EX1_323h").then(Morph(SELF, Summon.CARD)),
		Summon(CONTROLLER, "EX1_323w")
	)

class EX1_tk33:
	"INFERNO!"
	activate = Summon(CONTROLLER, "EX1_tk34")


##
# Spells

class CS2_061:
	"Drain Life"
	play = Hit(TARGET, 2), Heal(FRIENDLY_HERO, 2)


class CS2_062:
	"Hellfire"
	play = Hit(ALL_CHARACTERS, 3)


class CS2_063:
	"Corruption"
	play = Buff(TARGET, "CS2_063e")

class CS2_063e:
	events = OWN_TURN_BEGIN.on(Destroy(OWNER))


class CS2_057:
	"Shadow Bolt"
	play = Hit(TARGET, 4)


class EX1_302:
	"Mortal Coil"
	play = Hit(TARGET, 1), Dead(TARGET) & Draw(CONTROLLER)


class EX1_303:
	"Shadowflame"
	play = Hit(ENEMY_MINIONS, ATK(TARGET)), Destroy(TARGET)


class EX1_308:
	"Soulfire"
	play = Hit(TARGET, 4), Discard(RANDOM(FRIENDLY_HAND))


class EX1_309:
	"Siphon Soul"
	play = Destroy(TARGET), Heal(FRIENDLY_HERO, 3)


class EX1_312:
	"Twisting Nether"
	play = Destroy(ALL_MINIONS)


class EX1_316:
	"Power Overwhelming"
	play = Buff(TARGET, "EX1_316e")

class EX1_316e:
	events = TURN_END.on(Destroy(OWNER))
	tags = {
		GameTag.ATK: +4,
		GameTag.HEALTH: +4,
	}


class EX1_317:
	"Sense Demons"
	play = (
		Find(FRIENDLY_DECK + DEMON) &
		ForceDraw(RANDOM(FRIENDLY_DECK + DEMON)) |
		Give(CONTROLLER, "EX1_317t"),
	) * 2


class EX1_320:
	"Bane of Doom"
	play = Hit(TARGET, 2), Dead(TARGET) & Summon(CONTROLLER, RandomMinion(race=Race.DEMON))


class EX1_596:
	"Demonfire"
	play = Find(TARGET + FRIENDLY + DEMON) & Buff(TARGET, "EX1_596e") | Hit(TARGET, 2)

EX1_596e = buff(+2, +2)


class NEW1_003:
	"Sacrificial Pact"
	play = Destroy(TARGET), Heal(FRIENDLY_HERO, 5)
