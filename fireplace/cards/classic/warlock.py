from ..utils import *


##
# Minions

# Blood Imp
class CS2_059:
	def OWN_TURN_END(self):
		targets = self.controller.field.exclude(self)
		if targets:
			self.buff(random.choice(targets), "CS2_059o")


# Dread Infernal
class CS2_064:
	def action(self):
		for target in self.game.characters:
			if target is not self:
				self.hit(target, 1)


# Felguard
class EX1_301:
	def action(self):
		self.controller.maxMana -= 1


# Void Terror
class EX1_304:
	def action(self):
		if self.adjacentMinions:
			atk = 0
			health = 0
			for minion in self.adjacentMinions:
				atk += minion.atk
				health += minion.health
				minion.destroy()
			buff = self.buff(self, "EX1_304e", atk=atk, maxHealth=health)


# Succubus
class EX1_306:
	action = discard(1)


# Doomguard
class EX1_310:
	action = discard(2)


# Pit Lord
class EX1_313:
	action = damageHero(5)


# Summoning Portal (Virtual Aura)
class EX1_315a:
	cost = lambda self, i: min(i, max(1, i-2))


# Flame Imp
class EX1_319:
	action = damageHero(3)


# Lord Jaraxxus
class EX1_323:
	def action(self):
		self.removeFromField()
		self.controller.summon("EX1_323h")
		self.controller.summon("EX1_323w")


##
# Spells

# Drain Life
class CS2_061:
	def action(self, target):
		self.hit(target, 2)
		self.heal(self.controller.hero, 2)


# Hellfire
class CS2_062:
	def action(self):
		for target in self.game.characters:
			self.hit(target, 3)


# Corruption
class CS2_063:
	action = buffTarget("CS2_063e")

class CS2_063e:
	def TURN_BEGIN(self, player):
		# NOTE: We do not use OWN_TURN_BEGIN here because our controller
		# is not necessarily the same as the owner's controller and we
		# want it to be the original corrupting player's turn.
		if player is self.controller:
			self.owner.destroy()


# Shadow Bolt
class CS2_057:
	action = damageTarget(4)


# Mortal Coil
class EX1_302:
	def action(self, target):
		self.hit(target, 1)
		if target.dead:
			self.controller.draw()


# Shadowflame
class EX1_303:
	def action(self, target):
		for minion in self.controller.opponent.field:
			self.hit(minion, target.atk)
		target.destroy()


# Soulfire
class EX1_308:
	def action(self, target):
		self.hit(target, 4)
		if self.controller.hand:
			random.choice(self.controller.hand).discard()


# Siphon Soul
class EX1_309:
	def action(self, target):
		self.heal(self.controller.hero, 3)
		target.destroy()


# Twisting Nether
class EX1_312:
	def action(self):
		for target in self.game.board:
			target.destroy()


# Power Overwhelming
class EX1_316:
	action = buffTarget("EX1_316e")

class EX1_316e:
	def TURN_END(self, player):
		self.owner.destroy()


# Sense Demons
class EX1_317:
	def action(self):
		for i in range(2):
			demons = self.controller.deck.filter(race=Race.DEMON)
			if demons:
				self.controller.addToHand(random.choice(demons))
			else:
				self.controller.give("EX1_317t")


# Bane of Doom
class EX1_320:
	def action(self, target):
		self.hit(target, 2)
		if target.dead:
			self.controller.summon(random.choice(self.data.entourage))


# Demonfire
class EX1_596:
	def action(self, target):
		if target.race == Race.DEMON and target.controller == self.controller:
			self.buff(target, "EX1_596e")
		else:
			self.hit(target, 2)


# Sacrificial Pact
class NEW1_003:
	def action(self, target):
		target.destroy()
		self.heal(self.controller.hero, 5)
