from ..utils import *


##
# Hero Powers

class CS1h_001:
	"Lesser Heal (Anduin Wrynn)"
	activate = Heal(TARGET, 2)


##
# Minions

class CS2_235:
	"Northshire Cleric"
	events = Heal(ALL_MINIONS).on(Draw(CONTROLLER))


class EX1_091:
	"Cabal Shadow Priest"
	play = Steal(TARGET)


class EX1_335:
	"Lightspawn"
	update = Refresh(SELF, {GameTag.ATK: lambda self, i: self.health}, priority=100)


class EX1_341:
	"Lightwell"
	events = OWN_TURN_BEGIN.on(Heal(RANDOM(FRIENDLY + DAMAGED_CHARACTERS), 3))


class EX1_350:
	"Prophet Velen"
	update = Refresh(CONTROLLER, {
		GameTag.HEALING_DOUBLE: 1,
		GameTag.SPELLPOWER_DOUBLE: 1,
		GameTag.HERO_POWER_DOUBLE: 1,
	})


class EX1_591:
	"Auchenai Soulpriest"
	update = Refresh(CONTROLLER, {
		GameTag.EMBRACE_THE_SHADOW: True,
	})


class EX1_623:
	"Temple Enforcer"
	play = Buff(TARGET, "EX1_623e")

EX1_623e = buff(health=3)


##
# Spells

class CS2_004:
	"Power Word: Shield"
	play = Buff(TARGET, "CS2_004e"), Draw(CONTROLLER)

CS2_004e = buff(health=2)


class CS1_112:
	"Holy Nova"
	play = Hit(ENEMY_CHARACTERS, 2), Heal(FRIENDLY_CHARACTERS, 2)


class CS1_113:
	"Mind Control"
	play = Steal(TARGET)


class CS1_129:
	"Inner Fire"
	play = Buff(TARGET, "CS1_129e")

class CS1_129e:
	atk = lambda self, i: self._xatk

	def apply(self, target):
		self._xatk = target.health


class CS1_130:
	"Holy Smite"
	play = Hit(TARGET, 2)


class CS2_003:
	"Mind Vision"
	play = Give(CONTROLLER, Copy(RANDOM(ENEMY_HAND)))


class CS2_234:
	"Shadow Word: Pain"
	play = Destroy(TARGET)


class CS2_236:
	"Divine Spirit"
	play = Buff(TARGET, "CS2_236e", max_health=CURRENT_HEALTH(TARGET))


class DS1_233:
	"Mind Blast"
	play = Hit(ENEMY_HERO, 5)


class EX1_332:
	"Silence"
	play = Silence(TARGET)


class EX1_334:
	"Shadow Madness"
	play = Steal(TARGET), Buff(TARGET, "EX1_334e")

class EX1_334e:
	events = [
		TURN_END.on(Destroy(SELF), Steal(OWNER, OPPONENT)),
		Silence(OWNER).on(Steal(OWNER, OPPONENT))
	]
	tags = {GameTag.CHARGE: True}


class EX1_339:
	"Thoughtsteal"
	play = Give(CONTROLLER, Copy(RANDOM(ENEMY_DECK) * 2))


class EX1_345:
	"Mindgames"
	play = (
		Find(ENEMY_DECK + MINION) &
		Summon(CONTROLLER, Copy(RANDOM(ENEMY_DECK + MINION))) |
		Summon(CONTROLLER, "EX1_345t")
	)


class EX1_621:
	"Circle of Healing"
	play = Heal(ALL_MINIONS, 4)


class EX1_622:
	"Shadow Word: Death"
	play = Destroy(TARGET)


class EX1_624:
	"Holy Fire"
	play = Hit(TARGET, 5), Heal(FRIENDLY_HERO, 5)


class EX1_625:
	"Shadowform"
	play = Switch(FRIENDLY_HERO_POWER, {
		"EX1_625t": Summon(CONTROLLER, "EX1_625t2"),
		"EX1_625t2": (),
		None: Summon(CONTROLLER, "EX1_625t"),
	})

class EX1_625t:
	"Mind Spike"
	activate = Hit(TARGET, 2)
	update = Refresh(CONTROLLER, {GameTag.SHADOWFORM: True})

class EX1_625t2:
	"Mind Shatter"
	activate = Hit(TARGET, 3)
	update = Refresh(CONTROLLER, {GameTag.SHADOWFORM: True})


class EX1_626:
	"Mass Dispel"
	play = Silence(ENEMY_MINIONS), Draw(CONTROLLER)
