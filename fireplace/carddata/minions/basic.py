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
	activate = drawCard

# Murloc Tidehunter
class EX1_506(Murloc):
	def activate(self):
		self.owner.summon(Card.byId("EX1_506a"))

# Dalaran Mage
class EX1_582(Minion):
	spelldamage = 1

# Kobold Geomancer
class CS2_142(Minion):
	spellpower = 1

# Gnomish Inventor
class CS2_147(Minion):
	activate = drawCard

# Archmage
class CS2_155(Minion):
	spelldamage = 1

# Elven Archer
class CS2_189(Minion):
	def activate(self, target):
		target.damage(1)

# Ogre Magi
class CS2_197(Minion):
	spellpower = 1
