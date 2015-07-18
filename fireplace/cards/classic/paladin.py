from ..utils import *


##
# Hero Powers

# Reinforce (Uther Lightbringer)
class CS2_101:
	activate = Summon(CONTROLLER, "CS2_101t")


##
# Minions

# Guardian of Kings
class CS2_088:
	play = Heal(FRIENDLY_HERO, 6)


# Argent Protector
class EX1_362:
	play = SetTag(TARGET, {GameTag.DIVINE_SHIELD: True})


# Aldor Peacekeeper
class EX1_382:
	play = Buff(TARGET, "EX1_382e")

class EX1_382e:
	atk = lambda self, i: 1


# Tirion Fordring
class EX1_383:
	deathrattle = Summon(CONTROLLER, "EX1_383t")


##
# Spells

# Blessing of Might
class CS2_087:
	play = Buff(TARGET, "CS2_087e")


# Holy Light
class CS2_089:
	play = Heal(TARGET, 6)


# Blessing of Kings
class CS2_092:
	play = Buff(TARGET, "CS2_092e")


# Consecration
class CS2_093:
	play = Hit(ENEMY_CHARACTERS, 2)


# Hammer of Wrath
class CS2_094:
	play = Hit(TARGET, 3), Draw(CONTROLLER)


# Eye for an Eye
class EX1_132:
	events = Damage(FRIENDLY_HERO).on(
		lambda self, target, amount, source: (Hit(ENEMY_HERO, amount), Reveal(SELF))
	)


# Divine Favor
class EX1_349:
	def play(self):
		diff = len(self.controller.opponent.hand) - len(self.controller.hand)
		return Draw(CONTROLLER) * max(0, diff)


# Lay on Hands
class EX1_354:
	play = Heal(TARGET, 8), Draw(CONTROLLER) * 3


# Blessed Champion
class EX1_355:
	play = Buff(TARGET, "EX1_355e")

class EX1_355e:
	atk = lambda self, i: i * 2


# Humility
class EX1_360:
	play = Buff(TARGET, "EX1_360e")

class EX1_360e:
	atk = lambda self, i: 1


# Blessing of Wisdom
class EX1_363:
	play = Buff(TARGET, "EX1_363e")

class EX1_363e:
	events = Attack(OWNER).on(Draw(CONTROLLER))


# Holy Wrath
class EX1_365:
	# TODO
	def play(self, target):
		drawn = self.controller.draw()
		self.hit(target, drawn[0].cost)


# Hand of Protection
class EX1_371:
	play = SetTag(TARGET, {GameTag.DIVINE_SHIELD: True})


# Repentance
class EX1_379:
	events = Play(OPPONENT, MINION).after(
			lambda self, source, target, *args: (
				Buff(target, "EX1_379e"),
				Reveal(self)
				))

class EX1_379e:
	max_health = lambda self, i: 1


# Avenging Wrath
class EX1_384:
	def play(self):
		count = self.controller.get_spell_damage(8)
		return Hit(RANDOM_ENEMY_CHARACTER, 1) * count


# Equality
class EX1_619:
	play = Buff(ALL_MINIONS, "EX1_619e")

class EX1_619e:
	max_health = lambda self, i: 1


##
# Weapons

# Truesilver Champion
class CS2_097:
	events = Attack(FRIENDLY_HERO).on(Heal(FRIENDLY_HERO, 2))


# Sword of Justice
class EX1_366:
	events = Summon(CONTROLLER, MINION).after(
		lambda self, source, minion: (Buff(minion, "EX1_366e"), Hit(SELF, 1))
	)
