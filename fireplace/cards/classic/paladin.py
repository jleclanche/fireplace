from ..utils import *


##
# Hero Powers

# Reinforce (Uther Lightbringer)
class CS2_101:
	activate = [Summon(CONTROLLER, "CS2_101t")]


##
# Minions

# Guardian of Kings
class CS2_088:
	action = [Heal(FRIENDLY_HERO, 6)]


# Argent Protector
class EX1_362:
	action = [SetTag(TARGET, {GameTag.DIVINE_SHIELD: True})]


# Aldor Peacekeeper
class EX1_382:
	action = [Buff(TARGET, "EX1_382e")]

class EX1_382e:
	atk = lambda self, i: 1


# Tirion Fordring
class EX1_383:
	deathrattle = [Summon(CONTROLLER, "EX1_383t")]


##
# Spells

# Blessing of Might
class CS2_087:
	action = [Buff(TARGET, "CS2_087e")]


# Holy Light
class CS2_089:
	action = [Heal(TARGET, 6)]


# Blessing of Kings
class CS2_092:
	action = [Buff(TARGET, "CS2_092e")]


# Consecration
class CS2_093:
	action = [Hit(ENEMY_CHARACTERS, 2)]


# Hammer of Wrath
class CS2_094:
	action = [Hit(TARGET, 3), Draw(CONTROLLER)]


# Divine Favor
class EX1_349:
	def action(self):
		diff = len(self.controller.opponent.hand) - len(self.controller.hand)
		return [Draw(CONTROLLER) * max(0, diff)]


# Lay on Hands
class EX1_354:
	action = [Heal(TARGET, 8), Draw(CONTROLLER) * 3]


# Blessed Champion
class EX1_355:
	action = [Buff(TARGET, "EX1_355e")]

class EX1_355e:
	atk = lambda self, i: i * 2


# Humility
class EX1_360:
	action = [Buff(TARGET, "EX1_360e")]

class EX1_360e:
	atk = lambda self, i: 1


# Blessing of Wisdom
class EX1_363:
	action = [Buff(TARGET, "EX1_363e")]

class EX1_363e:
	events = [
		Attack(OWNER).on(Draw(CONTROLLER))
	]


# Holy Wrath
class EX1_365:
	# TODO
	def action(self, target):
		drawn = self.controller.draw()
		self.hit(target, drawn[0].cost)


# Hand of Protection
class EX1_371:
	action = [SetTag(TARGET, {GameTag.DIVINE_SHIELD: True})]


# Avenging Wrath
class EX1_384:
	def action(self):
		count = self.controller.get_spell_damage(8)
		return [Hit(RANDOM_ENEMY_CHARACTER, 1) * count]


# Equality
class EX1_619:
	action = [Buff(ALL_MINIONS, "EX1_619e")]

class EX1_619e:
	max_health = lambda self, i: 1


##
# Weapons

# Truesilver Champion
class CS2_097:
	events = [
		Attack(FRIENDLY_HERO).on(Heal(FRIENDLY_HERO, 2))
	]


# Sword of Justice
class EX1_366:
	events = [
		Summon(CONTROLLER, MINION).after(
			lambda self, source, minion: [Buff(minion, "EX1_366e"), Hit(SELF, 1)]
		)
	]
