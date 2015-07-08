from ..utils import *


##
# Hero Powers

# Lesser Heal (Anduin Wrynn)
class CS1h_001:
	activate = [Heal(TARGET, 2)]


##
# Minions

# Northshire Cleric
class CS2_235:
	events = [
		Heal(ALL_MINIONS).on(Draw(CONTROLLER))
	]


# Lightwarden
class EX1_001:
	events = [
		Heal().on(Buff(SELF, "EX1_001e"))
	]


# Cabal Shadow Priest
class EX1_091:
	action = [TakeControl(TARGET)]


# Lightspawn
class EX1_335:
	atk = lambda self, i: self.health


# Lightwell
class EX1_341:
	events = [
		OWN_TURN_BEGIN.on(Heal(RANDOM(FRIENDLY + DAMAGED_CHARACTERS), 3))
	]


# Temple Enforcer
class EX1_623:
	action = [Buff(TARGET, "EX1_623e")]


##
# Spells

# Power Word: Shield
class CS2_004:
	action = [Buff(TARGET, "CS2_004e"), Draw(CONTROLLER)]


# Holy Nova
class CS1_112:
	action = [Hit(ENEMY_CHARACTERS, 2), Heal(FRIENDLY_CHARACTERS, 2)]


# Mind Control
class CS1_113:
	action = [TakeControl(TARGET)]


# Inner Fire
class CS1_129:
	action = [Buff(TARGET, "CS1_129e")]

class CS1_129e:
	atk = lambda self, i: self._xatk

	def apply(self, target):
		self._xatk = target.health


# Holy Smite
class CS1_130:
	action = [Hit(TARGET, 2)]


# Mind Vision
class CS2_003:
	action = [Give(CONTROLLER, Copy(RANDOM(OPPONENT_HAND)))]


# Shadow Word: Pain
class CS2_234:
	action = [Destroy(TARGET)]


# Divine Spirit
class CS2_236:
	action = [Buff(TARGET, "CS2_236e")]

class CS2_236e:
	def apply(self, target):
		self.max_health = target.health


# Mind Blast
class DS1_233:
	action = [Hit(ENEMY_HERO, 5)]


# Silence
class EX1_332:
	action = [Silence(TARGET)]


# Shadow Madness
class EX1_334:
	action = [Buff(TARGET, "EX1_334e")]

class EX1_334e:
	def apply(self, target):
		self.controller.take_control(target)

	def destroy(self):
		self.controller.opponent.take_control(self.owner)


# Thoughtsteal
class EX1_339:
	action = [Give(CONTROLLER, Copy(RANDOM(OPPONENT_DECK + MINION) * 2))]


# Mindgames
class EX1_345:
	action = [Summon(CONTROLLER, Copy(RANDOM(OPPONENT_DECK + MINION) | "EX1_345t"))]


# Circle of Healing
class EX1_621:
	action = [Heal(ALL_MINIONS, 4)]


# Shadow Word: Death
class EX1_622:
	action = [Destroy(TARGET)]


# Holy Fire
class EX1_624:
	action = [Hit(TARGET, 5), Heal(FRIENDLY_HERO, 5)]


# Shadowform
class EX1_625:
	def action(self):
		if self.controller.hero.power.id == "EX1_625t":
			return [Summon(CONTROLLER, "EX1_625t2")]
		elif self.controller.hero.power.id == "EX1_625t2":
			pass
		else:
			return [Summon(CONTROLLER, "EX1_625t")]

# Mind Spike
class EX1_625t:
	activate = [Hit(TARGET, 2)]

# Mind Shatter
class EX1_625t2:
	activate = [Hit(TARGET, 3)]


# Mass Dispel
class EX1_626:
	action = [Silence(ENEMY_MINIONS), Draw(CONTROLLER)]
