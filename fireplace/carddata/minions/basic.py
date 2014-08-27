from fireplace.targeting import *


# helpers
drawCard = lambda self: self.owner.draw()

# Healing Totem
class NEW1_009:
	def endTurn(self):
		targets = self.getTargets(TARGET_FRIENDLY_MINIONS)
		for target in targets:
			if self.game.currentPlayer is self.owner:
				target.heal(1)


# Novice Engineer
class EX1_015:
	activate = drawCard

# Murloc Tidehunter
class EX1_506:
	def activate(self):
		self.owner.summon("EX1_506a")

# Dalaran Mage
class EX1_582:
	spelldamage = 1

# Kobold Geomancer
class CS2_142:
	spellpower = 1

# Gnomish Inventor
class CS2_147:
	activate = drawCard

# Archmage
class CS2_155:
	spelldamage = 1

# Elven Archer
class CS2_189:
	targeting = TARGET_ANY_CHARACTER
	def activate(self, target):
		target.damage(1)

# Ogre Magi
class CS2_197:
	spellpower = 1
