from fireplace.cards import Card, Minion


# helpers
drawCard = lambda self: self.owner.draw()

# Minion types
class Murloc(Minion):
	type = "Murloc"

class Beast(Minion):
	type = "Beast"


# Novice Engineer
class EX1_015(Minion):
	attack = 1
	health = 1
	cost = 2
	activate = drawCard

# Murloc Tidehunter
class EX1_506(Murloc):
	attack = 2
	health = 1
	cost = 2
	def activate(self):
		self.owner.summon(Card.byId("EX1_506a"))

# Dalaran Mage
class EX1_582(Minion):
	attack = 1
	health = 4
	cost = 3
	spelldamage = 1

# Kobold Geomancer
class CS2_142(Minion):
	attack = 2
	health = 2
	cost = 2
	spellpower = 1

# Gnomish Inventor
class CS2_147(Minion):
	attack = 2
	health = 4
	cost = 4
	activate = drawCard

# Archmage
class CS2_155(Minion):
	attack = 4
	health = 7
	cost = 6
	spelldamage = 1

# Elven Archer
class CS2_189(Minion):
	attack = 1
	health = 1
	cost = 1
	def activate(self, target):
		target.damage(1)

# Ogre Magi
class CS2_197(Minion):
	attack = 4
	health = 4
	cost = 4
	spellpower = 1
