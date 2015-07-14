from ..utils import *


##
# Hero Powers

# Steady Shot (Rexxar)
class DS1h_292:
	activate = [Hit(ENEMY_HERO, 2)]

# Steady Shot (Alleria Windrunner)
class DS1h_292_H1:
	activate = DS1h_292.activate


##
# Minions

# Starving Buzzard
class CS2_237:
	events = [
		Summon(CONTROLLER, BEAST).on(Draw(CONTROLLER))
	]


# Houndmaster
class DS1_070:
	action = [Buff(TARGET, "DS1_070o")]


# Scavenging Hyena
class EX1_531:
	events = [
		Death(FRIENDLY + BEAST).on(Buff(SELF, "EX1_531e"))
	]


# Savannah Highmane
class EX1_534:
	deathrattle = [Summon(CONTROLLER, "EX1_534t") * 2]


##
# Spells

# Hunter's Mark
class CS2_084:
	action = [Buff(TARGET, "CS2_084e")]

class CS2_084e:
	max_health = lambda self, i: 1

# Multi-Shot
class DS1_183:
	action = [Hit(RANDOM_ENEMY_MINION * 2, 3)]


# Arcane Shot
class DS1_185:
	action = [Hit(TARGET, 2)]


# Explosive Shot
class EX1_537:
	action = [Hit(TARGET, 5), Hit(TARGET_ADJACENT, 2)]


# Unleash the Hounds
class EX1_538:
	def action(self):
		count = len(self.controller.opponent.field)
		return [Summon(CONTROLLER, "EX1_538t") * count]


# Kill Command
class EX1_539:
	action = [Find(FRIENDLY_MINIONS + BEAST) & Hit(TARGET, 5) | Hit(TARGET, 3)]


# Flare
class EX1_544:
	action = [
		SetTag(ALL_MINIONS, {GameTag.STEALTH: False}),
		Destroy(ENEMY_SECRETS),
		Draw(CONTROLLER),
	]


# Bestial Wrath
class EX1_549:
	action = [Buff(TARGET, "EX1_549o")]


# Freezing Trap
class EX1_611:
	events = [
		Attack(ENEMY_MINIONS).on(
			lambda self, source, target: [Bounce(source), Buff(source, "EX1_611e"), Reveal(SELF)],
		zone=Zone.SECRET)
	]

class EX1_611e:
	# Remove the buff when the card is played
	events = [
		Play(PLAYER, OWNER).after(Destroy(SELF))
	]


# Deadly Shot
class EX1_617:
	action = [Destroy(RANDOM_ENEMY_MINION)]


# Animal Companion
class NEW1_031:
	def action(self):
		huffer = random.choice(self.data.entourage)
		return [Summon(CONTROLLER, huffer)]


##
# Secrets


# Snake Trap
class EX1_554:
	events = [
		Attack(ALL_MINIONS, FRIENDLY_MINIONS).on(lambda self, source, target, *args: [
			Summon(CONTROLLER, "EX1_554t") * 3, Reveal(SELF)
		], zone=Zone.SECRET)
	]


# Snipe
class EX1_609:
	events = [
		Play(OPPONENT, MINION).after(
			lambda self, source, target, *args: [Hit(target, 4), Reveal(SELF)],
		zone=Zone.SECRET)
	]


# Explosive Trap
class EX1_610:
	events = [
		Attack(ENEMY_MINIONS, FRIENDLY_HERO).on(
			Hit(ENEMY_CHARACTERS, 2), Reveal(SELF),
		zone=Zone.SECRET)
	]


##
# Weapons

# Eaglehorn Bow
class EX1_536:
	events = [
		Reveal(FRIENDLY_SECRETS).on(Buff(SELF, "EX1_536e"))
	]
