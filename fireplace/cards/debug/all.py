from ..utils import *


# Damage 1
class XXX_001:
	action = damageTarget(1)


# Damage 5
class XXX_002:
	action = damageTarget(5)


# Restore 1
class XXX_003:
	action = healTarget(1)


# Restore 5
class XXX_004:
	action = healTarget(5)


# Destroy
class XXX_005:
	action = destroyTarget


# Break Weapon
class XXX_006:
	def action(self):
		if self.controller.opponent.weapon:
			self.controller.opponent.weapon.destroy()


# Enable for Attack
class XXX_007:
	def action(self, target):
		target.charge = True


# Freeze
class XXX_008:
	def action(self, target):
		target.frozen = True


# Enchant
class XXX_009:
	action = buffTarget("XXX_009e")


# Silence - debug
class XXX_010:
	action = silenceTarget


# Summon a random secret
class XXX_011:
	def action(self):
		secrets = self.controller.deck.filterByTag(GameTag.SECRET)
		if secrets:
			self.controller.summon(random.choice(secrets))


# Bounce
class XXX_012:
	action = bounceTarget


# Discard
class XXX_013:
	def action(self, target):
		target.controller.discardHand()


# Mill 10
class XXX_014:
	def action(self, target):
		for i in range(10):
			target.controller.deck[-1].destroy()


# Crash
class XXX_015:
	def action(self):
		assert False


# Snake Ball
class XXX_016:
	def action(self):
		for i in range(5):
			self.controller.summon("EX1_554t")


# Draw 3 Cards
class XXX_017:
	action = drawCards(3)


# Destroy All Minions
class XXX_018:
	def action(self):
		for target in self.game.field:
			target.destroy()


# Restore All Health
class XXX_021:
	def action(self):
		self.heal(target, target.maxHealth)


# Destroy All Heroes
class XXX_023:
	def action(self):
		self.game.player1.hero.destroy()
		self.game.player2.hero.destroy()


# Do Nothing
class XXX_025:
	pass


# Server Crash
class XXX_027:
	def action(self):
		raise SystemError


# Destroy Hero Power
class XXX_041:
	def action(self, target):
		target.controller.hero.power.destroy()


# -1 Durability
class XXX_048:
	def action(self, target):
		if target.controller.hero.weapon:
			target.controller.hero.weapon.durability -= 1


# Destroy All Mana
class XXX_049:
	def action(self, target):
		target.controller.maxMana = 0


# Destroy a Mana Crystal
class XXX_050:
	def action(self, target):
		target.controller.maxMana -= 1


# Armor
class XXX_053:
	action = gainArmor(100)


# Weapon Buff
class XXX_054:
	def action(self):
		if self.hero.weapon:
			self.buff(self.hero.weapon, "XXX_054e")

class XXX_054e:
	Atk = 100
	Durability = 100


# 1000 Stats
class XXX_055:
	action = buffTarget("XXX_055e")

class XXX_055e:
	Atk = 1000
	Health = 1000


# Silence Destroy
class XXX_056:
	def action(self):
		for target in self.game.field:
			target.silence()
			target.destroy()


# Destroy Secrets
class XXX_057:
	def action(self, target):
		for secret in target.controller.secrets:
			secret.destroy()
