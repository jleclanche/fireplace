from ..utils import *


##
# Minions

# Northshire Cleric
class CS2_235:
	def HEAL(self, source, target, amount):
		if target.type == CardType.MINION:
			self.controller.draw()


# Lightwarden
class EX1_001:
	def HEAL(self, source, target, amount):
		self.buff(self, "EX1_001e")


# Cabal Shadow Priest
class EX1_091:
	def action(self, target):
		self.controller.takeControl(target)


# Lightspawn
class EX1_335:
	atk = lambda self, i: self.health


# Lightwell
class EX1_341:
	def OWN_TURN_BEGIN(self):
		targets = [t for t in self.controller.characters if t.damage]
		if targets:
			self.heal(random.choice(targets), 3)


# Temple Enforcer
class EX1_623:
	action = buffTarget("EX1_623e")


##
# Spells

# Power Word: Shield
class CS2_004:
	def action(self, target):
		self.buff(target, "CS2_004e")
		self.controller.draw()


# Holy Nova
class CS1_112:
	def action(self):
		for target in self.game.characters:
			if target.controller == self.controller:
				self.heal(target, 2)
			else:
				self.hit(target, 2)


# Mind Control
class CS1_113:
	def action(self, target):
		self.controller.takeControl(target)


# Inner Fire
class CS1_129:
	action = buffTarget("CS1_129e")

class CS1_129e:
	atk = lambda self, i: self._xatk
	def apply(self, target):
		self._xatk = target.health


# Holy Smite
class CS1_130:
	action = damageTarget(2)


# Mind Vision
class CS2_003:
	def action(self):
		if self.controller.opponent.hand:
			self.controller.give(random.choice(self.controller.opponent.hand).id)


# Shadow Word: Pain
class CS2_234:
	action = destroyTarget


# Divine Spirit
class CS2_236:
	action = buffTarget("CS2_236e")

class CS2_236e:
	def apply(self, target):
		self.maxHealth = target.health


# Mind Blast
class DS1_233:
	action = damageEnemyHero(5)


# Silence
class EX1_332:
	action = silenceTarget


# Shadow Madness
class EX1_334:
	action = buffTarget("EX1_334e")

class EX1_334e:
	def apply(self, target):
		self.controller.takeControl(target)

	def destroy(self):
		self.controller.opponent.takeControl(self.owner)


# Thoughtsteal
class EX1_339:
	def action(self):
		deck = self.controller.opponent.deck
		for card in random.sample(deck, min(len(deck), 2)):
			self.controller.give(card.id)


# Mindgames
class EX1_345:
	def action(self):
		creatures = self.controller.opponent.deck.filter(type=CardType.MINION)
		if creatures:
			creature = random.choice(creatures).id
		else:
			creature = "EX1_345t"
		self.controller.summon(creature)


# Circle of Healing
class EX1_621:
	def action(self):
		for target in self.game.board:
			self.heal(target, 4)


# Shadow Word: Death
class EX1_622:
	action = destroyTarget


# Holy Fire
class EX1_624:
	def action(self, target):
		self.hit(target, 5)
		self.heal(self.controller.hero, 5)


# Shadowform
class EX1_625:
	def action(self):
		if self.controller.hero.power.id == "EX1_625t":
			self.controller.summon("EX1_625t2")
		elif self.controller.hero.power.id == "EX1_625t2":
			pass
		else:
			self.controller.summon("EX1_625t")

# Mind Spike
class EX1_625t:
	action = damageTarget(2)

# Mind Shatter
class EX1_625t2:
	action = damageTarget(3)


# Mass Dispel
class EX1_626:
	def action(self):
		for target in self.controller.opponent.field:
			target.silence()
		self.controller.draw()
