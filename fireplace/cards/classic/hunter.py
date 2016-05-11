from ..utils import *


##
# Hero Powers

class DS1h_292:
	"Steady Shot (Rexxar)"
	activate = Hit(ENEMY_HERO, 2)

class DS1h_292_H1:
	"Steady Shot (Alleria Windrunner)"
	activate = DS1h_292.activate


##
# Minions

class CS2_237:
	"Starving Buzzard"
	events = Summon(CONTROLLER, BEAST).on(Draw(CONTROLLER))


class DS1_070:
	"Houndmaster"
	powered_up = Find(FRIENDLY_MINIONS + BEAST)
	play = Buff(TARGET, "DS1_070o")

DS1_070o = buff(+2, +2, taunt=True)


class DS1_175:
	"Timber Wolf"
	update = Refresh(FRIENDLY_MINIONS + BEAST - SELF, buff="DS1_175o")

DS1_175o = buff(atk=1)


class DS1_178:
	"Tundra Rhino"
	update = Refresh(FRIENDLY_MINIONS + BEAST, buff="DS1_178e")

DS1_178e = buff(charge=True)


class EX1_531:
	"Scavenging Hyena"
	events = Death(FRIENDLY + BEAST).on(Buff(SELF, "EX1_531e"))

EX1_531e = buff(+2, +1)


class EX1_534:
	"Savannah Highmane"
	deathrattle = Summon(CONTROLLER, "EX1_534t") * 2


class NEW1_033:
	"Leokk"
	update = Refresh(FRIENDLY_MINIONS - SELF, buff="NEW1_033o")

NEW1_033o = buff(atk=1)


##
# Spells

class CS2_084:
	"Hunter's Mark"
	play = Buff(TARGET, "CS2_084e")

class CS2_084e:
	max_health = SET(1)


class DS1_183:
	"Multi-Shot"
	play = Hit(RANDOM_ENEMY_MINION * 2, 3)


class DS1_184:
	"Tracking"
	play = GenericChoice(CONTROLLER, FRIENDLY_DECK[:3])


class DS1_185:
	"Arcane Shot"
	play = Hit(TARGET, 2)


class EX1_537:
	"Explosive Shot"
	play = Hit(TARGET, 5), Hit(TARGET_ADJACENT, 2)


class EX1_538:
	"Unleash the Hounds"
	play = Summon(CONTROLLER, "EX1_538t") * Count(ENEMY_MINIONS)


class EX1_539:
	"Kill Command"
	powered_up = Find(FRIENDLY_MINIONS + BEAST)
	play = powered_up & Hit(TARGET, 5) | Hit(TARGET, 3)


class EX1_544:
	"Flare"
	play = (
		Unstealth(ALL_MINIONS),
		Destroy(ENEMY_SECRETS),
		Draw(CONTROLLER),
	)


class EX1_549:
	"Bestial Wrath"
	play = Buff(TARGET, "EX1_549o")

EX1_549o = buff(atk=2, immune=True)


class EX1_617:
	"Deadly Shot"
	play = Destroy(RANDOM_ENEMY_MINION)


class NEW1_031:
	"Animal Companion"
	play = Summon(CONTROLLER, RandomEntourage())


##
# Secrets

class EX1_533:
	"Misdirection"
	secret = Attack(ALL_CHARACTERS, FRIENDLY_HERO).on(
		Reveal(SELF),
		Retarget(Attack.ATTACKER, RANDOM(ALL_CHARACTERS - FRIENDLY_HERO - Attack.ATTACKER))
	)


class EX1_554:
	"Snake Trap"
	secret = Attack(ALL_MINIONS, FRIENDLY_MINIONS).on(FULL_BOARD | (
		Reveal(SELF), Summon(CONTROLLER, "EX1_554t") * 3
	))


class EX1_609:
	"Snipe"
	secret = Play(OPPONENT, MINION | HERO).after(
		Reveal(SELF), Hit(Play.CARD, 4)
	)


class EX1_610:
	"Explosive Trap"
	secret = Attack(ENEMY_CHARACTERS, FRIENDLY_HERO).on(
		Reveal(SELF), Hit(ENEMY_CHARACTERS, 2)
	)


class EX1_611:
	"Freezing Trap"
	secret = Attack(ENEMY_MINIONS).on(
		Reveal(SELF),
		Bounce(Attack.ATTACKER),
		Buff(Attack.ATTACKER, "EX1_611e")
	)

class EX1_611e:
	events = REMOVED_IN_PLAY
	tags = {GameTag.COST: +2}


##
# Weapons

class DS1_188:
	"Gladiator's Longbow"
	update = Refresh(FRIENDLY_HERO, {GameTag.IMMUNE_WHILE_ATTACKING: True})


class EX1_536:
	"Eaglehorn Bow"
	events = Reveal(FRIENDLY_SECRETS).on(Buff(SELF, "EX1_536e"))

EX1_536e = buff(health=1)
