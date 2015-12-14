from ..utils import *


##
# Hero Powers

# Steady Shot (Rexxar)
class DS1h_292:
	activate = Hit(ENEMY_HERO, 2)

# Steady Shot (Alleria Windrunner)
class DS1h_292_H1:
	activate = DS1h_292.activate


##
# Minions

# Starving Buzzard
class CS2_237:
	events = Summon(CONTROLLER, BEAST).on(Draw(CONTROLLER))


# Houndmaster
class DS1_070:
	powered_up = Find(FRIENDLY_MINIONS + BEAST)
	play = Buff(TARGET, "DS1_070o")

DS1_070o = buff(+2, +2, taunt=True)


# Timber Wolf
class DS1_175:
	update = Refresh(FRIENDLY_MINIONS + BEAST - SELF, buff="DS1_175o")

DS1_175o = buff(atk=1)


# Tundra Rhino
class DS1_178:
	update = Refresh(FRIENDLY_MINIONS + BEAST, buff="DS1_178e")

DS1_178e = buff(charge=True)


# Scavenging Hyena
class EX1_531:
	events = Death(FRIENDLY + BEAST).on(Buff(SELF, "EX1_531e"))

EX1_531e = buff(+2, +1)


# Savannah Highmane
class EX1_534:
	deathrattle = Summon(CONTROLLER, "EX1_534t") * 2


# Leokk
class NEW1_033:
	update = Refresh(FRIENDLY_MINIONS - SELF, buff="NEW1_033o")

NEW1_033o = buff(atk=1)


##
# Spells

# Hunter's Mark
class CS2_084:
	play = Buff(TARGET, "CS2_084e")

class CS2_084e:
	max_health = SET(1)


# Multi-Shot
class DS1_183:
	play = Hit(RANDOM_ENEMY_MINION * 2, 3)


# Tracking
class DS1_184:
	play = GenericChoice(CONTROLLER, FRIENDLY_DECK[:3])


# Arcane Shot
class DS1_185:
	play = Hit(TARGET, 2)


# Explosive Shot
class EX1_537:
	play = Hit(TARGET, 5), Hit(TARGET_ADJACENT, 2)


# Unleash the Hounds
class EX1_538:
	play = Summon(CONTROLLER, "EX1_538t") * Count(ENEMY_MINIONS)


# Kill Command
class EX1_539:
	powered_up = Find(FRIENDLY_MINIONS + BEAST)
	play = powered_up & Hit(TARGET, 5) | Hit(TARGET, 3)


# Flare
class EX1_544:
	play = (
		Unstealth(ALL_MINIONS),
		Destroy(ENEMY_SECRETS),
		Draw(CONTROLLER),
	)


# Bestial Wrath
class EX1_549:
	play = Buff(TARGET, "EX1_549o")

EX1_549o = buff(atk=2, immune=True)


# Deadly Shot
class EX1_617:
	play = Destroy(RANDOM_ENEMY_MINION)


# Animal Companion
class NEW1_031:
	play = Summon(CONTROLLER, RandomEntourage())


##
# Secrets

# Misdirection
class EX1_533:
	secret = Attack(ALL_CHARACTERS, FRIENDLY_HERO).on(
		Retarget(Attack.ATTACKER, RANDOM(ALL_CHARACTERS - FRIENDLY_HERO))
	)


# Snake Trap
class EX1_554:
	secret = Attack(ALL_MINIONS, FRIENDLY_MINIONS).on(FULL_BOARD | (
		Reveal(SELF), Summon(CONTROLLER, "EX1_554t") * 3
	))


# Snipe
class EX1_609:
	secret = Play(OPPONENT, MINION | HERO).after(
		Reveal(SELF), Hit(Play.CARD, 4)
	)


# Explosive Trap
class EX1_610:
	secret = Attack(ENEMY_CHARACTERS, FRIENDLY_HERO).on(
		Reveal(SELF), Hit(ENEMY_CHARACTERS, 2)
	)


# Freezing Trap
class EX1_611:
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

# Gladiator's Longbow
class DS1_188:
	update = Refresh(FRIENDLY_HERO, {GameTag.IMMUNE_WHILE_ATTACKING: True})


# Eaglehorn Bow
class EX1_536:
	events = Reveal(FRIENDLY_SECRETS).on(Buff(SELF, "EX1_536e"))

EX1_536e = buff(health=1)
