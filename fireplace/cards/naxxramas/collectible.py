from ..utils import *


##
# Minions

# Zombie Chow
class FP1_001:
	def deathrattle(self):
		self.heal(self.controller.opponent.hero, 5)


# Haunted Creeper
class FP1_002:
	def deathrattle(self):
		self.controller.summon("FP1_002t")
		self.controller.summon("FP1_002t")


# Mad Scientist
class FP1_004:
	def deathrattle(self):
		secrets = self.controller.deck.filterByTag(GameTag.SECRET)
		if secrets:
			self.controller.summon(random.choice(secrets))


# Shade of Naxxramas
class FP1_005:
	def OWN_TURN_BEGIN(self):
		self.buff(self, "FP1_005e")


# Nerubian Egg
class FP1_007:
	deathrattle = summonMinion("FP1_007t")


# Deathlord
class FP1_009:
	def deathrattle(self):
		minions = self.controller.opponent.deck.filterByType(CardType.MINION)
		if minions:
			self.controller.opponent.summon(random.choice(minions))


# Webspinner
class FP1_011:
	def deathrattle(self):
		self.controller.give(randomCollectible(type=CardType.MINION, race=Race.BEAST))


# Sludge Belcher
class FP1_012:
	deathrattle = summonMinion("FP1_012t")


# Wailing Soul
class FP1_016:
	def action(self):
		for target in self.controller.field:
			target.silence()


# Voidcaller
class FP1_022:
	def deathrattle(self):
		demons = self.controller.hand.filterByRace(Race.DEMON)
		if demons:
			self.controller.summon(random.choice(demons))


# Dark Cultist
class FP1_023:
	def deathrattle(self):
		if self.controller.field:
			target = random.choice(self.controller.field)
			self.buff(target, "FP1_023e")


# Unstable Ghoul
class FP1_024:
	def deathrattle(self):
		for target in self.controller.getTargets(TARGET_ALL_MINIONS):
			self.hit(target, 1)


# Anub'ar Ambusher
class FP1_026:
	def deathrattle(self):
		if self.controller.field:
			random.choice(self.controller.field).bounce()


# Stoneskin Gargoyle
class FP1_027:
	def OWN_TURN_BEGIN(self):
		self.heal(self, self.damage)


# Undertaker
class FP1_028:
	def OWN_MINION_SUMMON(self, minion):
		if minion.hasDeathrattle:
			self.buff(self, "FP1_028e")


# Dancing Swords
class FP1_029:
	def deathrattle(self):
		self.controller.opponent.draw()


# Loatheb
class FP1_030:
	def action(self):
		self.game.register("TURN_END",
			lambda *args: self.buff(self.controller.opponent.hero, "FP1_030e"),
		once=True)

class FP1_030e:
	def TURN_END(self, player):
		# Remove the buff at the end of the other player's turn
		if player is not self.owner.controller:
			self.destroy()

class FP1_030ea:
	cost = lambda self, i: i+5


##
# Spells

# Reincarnate
class FP1_025:
	def action(self, target):
		target.destroy()
		self.controller.summon(target.id)


##
# Weapons

# Death's Bite
class FP1_021:
	def deathrattle(self):
		for target in self.controller.game.board:
			self.hit(target, 1)
