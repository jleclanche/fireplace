from ..utils import *

##
# Minions

# Starving Buzzard
class CS2_237:
	def OWN_MINION_SUMMONED(self, minion):
		if minion.race == Race.BEAST:
			self.controller.draw()


# Houndmaster
class DS1_070:
	action = buffTarget("DS1_070o")

class DS1_070o:
	Atk = 2
	Health = 2
	Taunt = True


# Timber Wolf
class DS1_175:
	Aura = "DS1_175o"

# Furious Howl
class DS1_175o:
	Atk = 1
	targeting = TARGET_FRIENDLY_MINIONS
	def isValidTarget(self, target):
		return target.race == Race.BEAST and target is not self.source


# Tundra Rhino
class DS1_178:
	Aura = "DS1_178e"

# Charge
class DS1_178e:
	Charge = True
	targeting = TARGET_FRIENDLY_MINIONS
	def isValidTarget(self, target):
		return target.race == Race.BEAST


# Scavenging Hyena
class EX1_531:
	def OWN_MINION_DESTROYED(self, minion):
		if minion.race == Race.BEAST:
			self.buff(self, "EX1_531e")

class EX1_531e:
	Atk = 2
	Health = 1


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
		for minion in self.controller.field:
			if minion.race == Race.BEAST:
				return self.hit(target, 5)
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


# Deadly Shot
class EX1_617:
	def action(self):
		random.choice(self.controller.opponent.field).destroy()


# Animal Companion
class NEW1_031:
	def action(self):
		self.controller.summon(random.choice(self.entourage))

# Leokk
class NEW1_033:
	Aura = "NEW1_033o"

class NEW1_033o:
	Atk = 1
	targeting = TARGET_FRIENDLY_MINIONS
	def isValidTarget(self, target):
		return target is not self.source
