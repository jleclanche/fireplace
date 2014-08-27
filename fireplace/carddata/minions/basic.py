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

# Goldshire Footman
class CS1_042(Minion):
	attack = 1
	health = 2
	cost = 1
	taunt = True

# Magma Rager
class CS2_118(Minion):
	attack = 5
	health = 1
	cost = 3

# Oasis Snapjaw
class CS2_119(Minion):
	attack = 2
	health = 7
	cost = 4

# River Crocolisk
class CS2_120(Beast):
	attack = 2
	health = 3
	cost = 2

# Frostwolf Grunt
class CS2_121(Minion):
	attack = 2
	health = 2
	cost = 2
	taunt = True

# Wolfrider
class CS2_124(Minion):
	attack = 3
	health = 1
	cost = 3
	charge = True

# Ironfur Grizzly
class CS2_125(Beast):
	attack = 3
	health = 3
	cost = 3
	taunt = True

# Silverback Patriarch
class CS2_127(Beast):
	attack = 1
	health = 4
	cost = 3
	taunt = True

# Stormwind Knight
class CS2_131(Minion):
	attack = 2
	health = 5
	cost = 4
	charge = True

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

# Lord of the Arena
class CS2_162(Minion):
	attack = 6
	health = 5
	cost = 6
	taunt = True

# Murloc Raider
class CS2_168(Murloc):
	attack = 2
	health = 1
	cost = 1

# Stonetusk Boar
class CS2_171(Beast):
	attack = 1
	health = 1
	cost = 1
	charge = True

# Bloodfen Raptor
class CS2_172(Beast):
	attack = 3
	health = 2
	cost = 2

# Bluegill Warrior
class CS2_173(Murloc):
	attack = 2
	health = 1
	cost = 2
	charge = True

# Sen'jin Shieldmasta
class CS2_179(Minion):
	attack = 3
	health = 5
	cost = 5
	taunt = True

# Chillwind Yeti
class CS2_182(Minion):
	attack = 4
	health = 5
	cost = 4

# War Golem
class CS2_186(Minion):
	attack = 7
	health = 7
	cost = 7

# Booty Bay Bodyguard
class CS2_187(Minion):
	attack = 5
	health = 4
	cost = 5
	taunt = True

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

# Boulderfist Ogre
class CS2_200(Minion):
	attack = 6
	health = 7
	cost = 6

# Core Hound
class CS2_201(Beast):
	attack = 9
	health = 5
	cost = 7

# Reckless Rocketeer
class CS2_213(Minion):
	attack = 5
	health = 2
	cost = 6
	charge = True
