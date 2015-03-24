from ..utils import *


##
# Minions

# Starving Buzzard
class CS2_237:
	def OWN_MINION_SUMMON(self, minion):
		if minion.race == Race.BEAST:
			self.controller.draw()


# Houndmaster
class DS1_070:
	action = buffTarget("DS1_070o")


# Furious Howl (Timber Wolf)
class DS1_175o:
	targeting = TARGET_FRIENDLY_MINIONS
	def isValidTarget(self, target):
		return target.race == Race.BEAST and target is not self.source


# Charge (Tundra Rhino)
class DS1_178e:
	targeting = TARGET_FRIENDLY_MINIONS
	def isValidTarget(self, target):
		return target.race == Race.BEAST


# Scavenging Hyena
class EX1_531:
	def OWN_MINION_DESTROY(self, minion):
		if minion.race == Race.BEAST:
			self.buff(self, "EX1_531e")


# Savannah Highmane
class EX1_534:
	def deathrattle(self):
		self.controller.summon("EX1_534t")
		self.controller.summon("EX1_534t")


##
# Spells

# Hunter's Mark
class CS2_084:
	action = buffTarget("CS2_084e")

class CS2_084e:
	def apply(self, target):
		self.setHealth(1)

# Multi-Shot
class DS1_183:
	def action(self):
		targets = random.sample(self.controller.opponent.field, 2)
		for target in targets:
			self.hit(target, 3)


# Arcane Shot
class DS1_185:
	def action(self, target):
		self.hit(target, 3)


# Explosive Shot
class EX1_537:
	def action(self, target):
		for minion in target.adjacentMinions:
			self.hit(minion, 2)
		self.hit(target, 5)


# Unleash the Hounds
class EX1_538:
	def action(self):
		for i in range(len(self.controller.opponent.field)):
			self.controller.summon("EX1_538t")


# Kill Command
class EX1_539:
	def action(self, target):
		if self.poweredUp:
			self.hit(target, 5)
		else:
			self.hit(target, 3)


# Flare
class EX1_544:
	def action(self):
		for minion in self.controller.getTargets(TARGET_ALL_MINIONS):
			if minion.stealthed:
				minion.stealthed = False
		for secret in self.controller.opponent.secrets:
			secret.destroy()
		self.controller.draw()


# Bestial Wrath
class EX1_549:
	action = buffTarget("EX1_549o")


# Freezing Trap
class EX1_611:
	def ATTACK(self, source, target):
		if source.controller is self.controller.opponent and source.type == CardType.MINION:
			source.bounce()
			self.buff(source, "EX1_611e")
			self.reveal()

class EX1_611e:
	# Remove the buff when the card is played
	def AFTER_SELF_CARD_PLAYED(self):
		self.destroy()


# Deadly Shot
class EX1_617:
	def action(self):
		random.choice(self.controller.opponent.field).destroy()


# Animal Companion
class NEW1_031:
	def action(self):
		self.controller.summon(random.choice(self.entourage))


# Eye in the Sky (Leokk)
class NEW1_033o:
	targeting = TARGET_FRIENDLY_MINIONS
	def isValidTarget(self, target):
		return target is not self.source


##
# Weapons

# Eaglehorn Bow
class EX1_536:
	def OWN_SECRET_REVEAL(self, secret):
		self.buff(self, "EX1_536e")
