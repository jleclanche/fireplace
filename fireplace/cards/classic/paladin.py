from ..utils import *


##
# Hero Powers

# Reinforce (Uther Lightbringer)
class CS2_101:
	activate = Summon(CONTROLLER, "CS2_101t")

# Reinforce (Uther Skin 1)
class CS2_101_H1:
	activate = CS2_101.activate


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
	atk = SET(1)


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
	atk = SET(1)


# Blessing of Wisdom
class EX1_363:
	play = Buff(TARGET, "EX1_363e")

class EX1_363e:
	events = Attack(OWNER).on(Draw(CONTROLLER))


# Holy Wrath
class EX1_365:
	play = Hit(TARGET, Attr(Draw(CONTROLLER), GameTag.COST))

# Hand of Protection
class EX1_371:
	play = SetTag(TARGET, {GameTag.DIVINE_SHIELD: True})


# Avenging Wrath
class EX1_384:
	def play(self):
		count = self.controller.get_spell_damage(8)
		return Hit(RANDOM_ENEMY_CHARACTER, 1) * count


# Equality
class EX1_619:
	play = Buff(ALL_MINIONS, "EX1_619e")

class EX1_619e:
	max_health = SET(1)


##
# Secrets

# Noble Sacrifice
class EX1_130:
	events = Attack(ENEMY_MINIONS).on(
		Retarget(Attack.Args.ATTACKER, Summon(CONTROLLER, "EX1_130a")), Reveal(SELF)
	)


# Eye for an Eye
class EX1_132:
	events = Damage(FRIENDLY_HERO).on(
		Hit(ENEMY_HERO, Damage.Args.AMOUNT), Reveal(SELF)
	)


# Redemption
class EX1_136:
	events = Death(FRIENDLY + MINION).on(
		SetCurrentHealth(Summon(CONTROLLER, Copy(Death.Args.ENTITY)), 1), Reveal(SELF)
	)


# Repentance
class EX1_379:
	events = Play(OPPONENT, MINION).after(
		Buff(Play.Args.CARD, "EX1_379e"), Reveal(SELF)
	)

class EX1_379e:
	max_health = SET(1)


##
# Weapons

# Truesilver Champion
class CS2_097:
	events = Attack(FRIENDLY_HERO).on(Heal(FRIENDLY_HERO, 2))


# Sword of Justice
class EX1_366:
	events = Summon(CONTROLLER, MINION).after(
		Buff(Summon.Args.CARDS, "EX1_366e"),
		Hit(SELF, 1)
	)
