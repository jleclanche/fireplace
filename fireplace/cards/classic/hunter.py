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
	play = Buff(TARGET, "DS1_070o")


# Timber Wolf
class DS1_175:
	update = Refresh(FRIENDLY_MINIONS + BEAST - SELF, buff="DS1_175o")


# Tundra Rhino
class DS1_178:
	update = Refresh(FRIENDLY_MINIONS + BEAST, buff="DS1_178e")


# Scavenging Hyena
class EX1_531:
	events = Death(FRIENDLY + BEAST).on(Buff(SELF, "EX1_531e"))


# Savannah Highmane
class EX1_534:
	deathrattle = Summon(CONTROLLER, "EX1_534t") * 2


# Leokk
class NEW1_033:
	update = Refresh(FRIENDLY_MINIONS - SELF, buff="NEW1_033o")


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
	play = Find(FRIENDLY_MINIONS + BEAST) & Hit(TARGET, 5) | Hit(TARGET, 3)


# Flare
class EX1_544:
	play = (
		SetTag(ALL_MINIONS, {GameTag.STEALTH: False}),
		Destroy(ENEMY_SECRETS),
		Draw(CONTROLLER),
	)


# Bestial Wrath
class EX1_549:
	play = Buff(TARGET, "EX1_549o")


# Deadly Shot
class EX1_617:
	play = Destroy(RANDOM_ENEMY_MINION)


# Animal Companion
class NEW1_031:
	play = Summon(CONTROLLER, RandomEntourage())


##
# Secrets

# Snake Trap
class EX1_554:
	events = Attack(ALL_MINIONS, FRIENDLY_MINIONS).on(
		Summon(CONTROLLER, "EX1_554t") * 3, Reveal(SELF)
	)


# Snipe
class EX1_609:
	events = Play(OPPONENT, MINION).after(
		Hit(Play.Args.CARD, 4), Reveal(SELF)
	)


# Explosive Trap
class EX1_610:
	events = Attack(ENEMY_CHARACTERS, FRIENDLY_HERO).on(
		Hit(ENEMY_CHARACTERS, 2), Reveal(SELF)
	)


# Freezing Trap
class EX1_611:
	events = Attack(ENEMY_MINIONS).on(
		Bounce(Attack.Args.ATTACKER),
		Buff(Attack.Args.ATTACKER, "EX1_611e"),
		Reveal(SELF)
	)

class EX1_611e:
	# Remove the buff when the card is played
	events = Play(PLAYER, OWNER).after(Destroy(SELF))


##
# Weapons

# Eaglehorn Bow
class EX1_536:
	events = Reveal(FRIENDLY_SECRETS).on(Buff(SELF, "EX1_536e"))
