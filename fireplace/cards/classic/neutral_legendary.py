from ..utils import *


# The Black Knight
class EX1_002:
	action = destroyTarget


# Bloodmage Thalnos
class EX1_012:
	deathrattle = drawCard


# King Mukla
class EX1_014:
	def action(self):
		self.controller.opponent.give("EX1_014t")
		self.controller.opponent.give("EX1_014t")

# Bananas
class EX1_014t:
	action = buffTarget("EX1_014te")


# Sylvanas Windrunner
class EX1_016:
	def deathrattle(self):
		if self.controller.opponent.field:
			self.controller.takeControl(random.choice(self.controller.opponent.field))


# Lorewalker Cho
class EX1_100:
	def CARD_PLAYED(self, player, card):
		if card.type == CardType.SPELL:
			player.opponent.give(card.id)


# Cairne Bloodhoof
class EX1_110:
	deathrattle = summonMinion("EX1_110t")


# Leeroy Jenkins
class EX1_116:
	def action(self):
		self.controller.opponent.summon("EX1_116t")
		self.controller.opponent.summon("EX1_116t")


# Baron Geddon
class EX1_249:
	def action(self):
		for target in self.controller.getTargets(TARGET_ALL_MINIONS):
			if target is not self:
				self.hit(target, 2)


# Ragnaros the Firelord
class EX1_298:
	def OWN_TURN_END(self):
		self.hit(random.choice(self.controller.getTargets(TARGET_ENEMY_CHARACTERS)), 8)


# Nat Pagle
class EX1_557:
	def OWN_TURN_BEGIN(self):
		if random.choice((0, 1)):
			self.controller.draw()


# Harrison Jones
class EX1_558:
	def action(self):
		weapon = self.controller.opponent.hero.weapon
		if weapon:
			self.controller.draw(weapon.durability)
			weapon.destroy()


# Ysera
class EX1_572:
	def OWN_TURN_END(self):
		self.controller.give(random.choice(self.data.entourage))

# Ysera Awakens
class DREAM_02:
	def action(self):
		for target in self.controller.getTargets(TARGET_ALL_CHARACTERS):
			if target.id != "EX1_572":
				self.hit(target, 5)

# Dream
class DREAM_04:
	action = bounceTarget

# Nightmare
class DREAM_05:
	action = buffTarget("DREAM_05e")

class DREAM_05e:
	def OWN_TURN_BEGIN(self):
		self.owner.destroy()


# The Beast
class EX1_577:
	def deathrattle(self):
		self.controller.opponent.summon("EX1_finkle")


# Illidan Stormrage
class EX1_614:
	def OWN_CARD_PLAYED(self, card):
		self.controller.summon("EX1_614t")


# Captain Greenskin
class NEW1_024:
	def action(self):
		if self.controller.hero.weapon:
			self.buff(self.controller.hero.weapon, "NEW1_024o")


# Millhouse Manastorm
class NEW1_029:
	def action(self):
		self.buff(self.controller.opponent.hero, "NEW1_029t")

class NEW1_029t:
	AURA = True
	class Aura:
		CARDNAME = "Kill Millhouse! (Aura)"
		COST = lambda i: 0
		targeting = TARGET_ENEMY_HAND
		def isValidTarget(self, target):
			return target.type == CardType.SPELL

	def TURN_END(self, player):
		# Remove the buff at the end of the other player's turn
		if player is not self.owner.controller:
			self.destroy()


# Deathwing
class NEW1_030:
	def action(self):
		for target in self.controller.getTargets(TARGET_ALL_MINIONS):
			# Let's not kill ourselves in the process
			if target is not self:
				target.destroy()
		self.controller.discardHand()


# Gruul
class NEW1_038:
	def TURN_END(self, player):
		self.buff(self, "NEW1_038o")


# Hogger
class NEW1_040:
	OWN_TURN_END = summonMinion("NEW1_040t")


# Elite Tauren Chieftain
class PRO_001:
	def action(self):
		self.controller.give(random.choice(self.data.entourage))
		self.controller.opponent.give(random.choice(self.data.entourage))

# I Am Murloc
class PRO_001a:
	def action(self):
		for i in range(random.choice((3, 4, 5))):
			self.controller.summon("PRO_001at")

# Rogues Do It...
class PRO_001b:
	def action(self, target):
		target.damage(4)
		self.controller.draw()


# Power of the Horde
class PRO_001c:
	def action(self):
		self.controller.summon(random.choice(self.data.entourage))
