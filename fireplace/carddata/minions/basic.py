from ..card import *


# Bloodsail Corsair
class NEW1_025(Card):
	def activate(self):
		weapon = self.owner.opponent.hero.weapon
		if self.owner.opponent.hero.weapon:
			weapon.loseDurability(1)


# Voodoo Doctor
class EX1_011(Card):
	activate = healTarget(2)

# Novice Engineer
class EX1_015(Card):
	activate = drawCard

# Acidic Swamp Ooze
class EX1_066(Card):
	def activate(self):
		if self.owner.opponent.hero.weapon:
			self.owner.opponent.hero.weapon.destroy()

# Loot Hoarder
class EX1_096(Card):
	deathrattle = drawCard

# Murloc Tidehunter
class EX1_506(Card):
	def activate(self):
		self.owner.summon("EX1_506a")

# Harrison Jones
class EX1_558(Card):
	def activate(self):
		weapon = self.owner.opponent.hero.weapon
		if weapon:
			weapon.destroy()
			self.owner.draw(weapon.durability)

# Priestess of Elune
class EX1_583(Card):
	def activate(self):
		self.owner.hero.heal(4)

# Nightblade
class EX1_593(Card):
	def activate(self):
		self.owner.opponent.hero.damage(3)

# Guardian of Kings
class CS2_088(Card):
	def activate(self):
		self.owner.hero.heal(4)

# Earthen Ring Farseer
class CS2_117(Card):
	activate = healTarget(3)

# Raid Leader
class CS2_122(Card):
	aura = "CS2_122e"

# Gnomish Inventor
class CS2_147(Card):
	activate = drawCard

# Elven Archer
class CS2_189(Card):
	activate = damageTarget(1)


# Timber Wolf
class DS1_175(Card):
	aura = "DS1_175o"
