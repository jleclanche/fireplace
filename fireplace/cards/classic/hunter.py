from ..utils import *


##
# Minions

# Starving Buzzard
class CS2_237:
	def OWN_MINION_SUMMON(self, minion):
		if minion.race == Race.BEAST:
			return [Draw(CONTROLLER, 1)]


# Houndmaster
class DS1_070:
	action = [Buff(TARGET, "DS1_070o")]


# Scavenging Hyena
class EX1_531:
	def OWN_MINION_DESTROY(self, minion):
		if minion.race == Race.BEAST:
			return [Buff(SELF, "EX1_531e")]


# Savannah Highmane
class EX1_534:
	deathrattle = [Summon(CONTROLLER, "EX1_534t") * 2]


##
# Spells

# Hunter's Mark
class CS2_084:
	action = [Buff(TARGET, "CS2_084e")]

class CS2_084e:
	maxHealth = lambda self, i: 1

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
	def action(self, target):
		return [Hit(TARGET, 5 if self.poweredUp else 3)]


# Flare
class EX1_544:
	action = [
		SetTag(ALL_MINIONS, {GameTag.STEALTH: False}),
		Destroy(ENEMY_SECRETS),
		Draw(CONTROLLER, 1),
	]


# Bestial Wrath
class EX1_549:
	action = [Buff(TARGET, "EX1_549o")]


# Freezing Trap
class EX1_611:
	def ATTACK(self, source, target):
		if source.controller is self.controller.opponent and source.type == CardType.MINION:
			return [Bounce(source), Buff(source, "EX1_611e"), Reveal(SELF)]

class EX1_611e:
	# Remove the buff when the card is played
	AFTER_SELF_CARD_PLAYED = [Destroy(SELF)]


# Deadly Shot
class EX1_617:
	action = [Destroy(RANDOM_ENEMY_MINION)]


# Animal Companion
class NEW1_031:
	def action(self):
		huffer = random.choice(self.data.entourage)
		return [Summon(CONTROLLER, huffer)]


##
# Weapons

# Eaglehorn Bow
class EX1_536:
	OWN_SECRET_REVEAL = [Buff(SELF, "EX1_536e")]
