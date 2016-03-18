from ..utils import *


##
# Hero Powers

# Reinforce (Uther Lightbringer)
class CS2_101:
	activate = Summon(CONTROLLER, "CS2_101t")

# Reinforce (Lady Liadrin)
class CS2_101_H1:
	activate = CS2_101.activate


##
# Minions

# Guardian of Kings
class CS2_088:
	play = Heal(FRIENDLY_HERO, 6)


# Argent Protector
class EX1_362:
	play = GiveDivineShield(TARGET)


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

CS2_087e = buff(atk=3)


# Holy Light
class CS2_089:
	play = Heal(TARGET, 6)


# Blessing of Kings
class CS2_092:
	play = Buff(TARGET, "CS2_092e")

CS2_092e = buff(+4, +4)


# Consecration
class CS2_093:
	play = Hit(ENEMY_CHARACTERS, 2)


# Hammer of Wrath
class CS2_094:
	play = Hit(TARGET, 3), Draw(CONTROLLER)


# Divine Favor
class EX1_349:
	play = DrawUntil(CONTROLLER, Count(ENEMY_HAND))


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

# Blessing of Wisdom (Unused)
class EX1_363e2:
	events = Attack(OWNER).on(Draw(OWNER_OPPONENT))


# Holy Wrath
class EX1_365:
	play = Draw(CONTROLLER).then(Hit(TARGET, COST(Draw.CARD)))


# Hand of Protection
class EX1_371:
	play = GiveDivineShield(TARGET)


# Avenging Wrath
class EX1_384:
	def play(self):
		count = self.controller.get_spell_damage(8)
		yield Hit(RANDOM_ENEMY_CHARACTER, 1) * count


# Equality
class EX1_619:
	play = Buff(ALL_MINIONS, "EX1_619e")

class EX1_619e:
	max_health = SET(1)


##
# Secrets

# Noble Sacrifice
class EX1_130:
	secret = Attack(ENEMY_MINIONS).on(FULL_BOARD | (
		Reveal(SELF), Retarget(Attack.ATTACKER, Summon(CONTROLLER, "EX1_130a"))
	))


# Eye for an Eye
class EX1_132:
	secret = Damage(FRIENDLY_HERO).on(
		Reveal(SELF), Hit(ENEMY_HERO, Damage.AMOUNT)
	)


# Redemption
class EX1_136:
	secret = Death(FRIENDLY + MINION).on(FULL_BOARD | (
		Reveal(SELF),
		Summon(CONTROLLER, Copy(Death.ENTITY)).then(SetCurrentHealth(Summon.CARD, 1))
	))


# Repentance
class EX1_379:
	secret = Play(OPPONENT, MINION | HERO).after(
		Reveal(SELF), Buff(Play.CARD, "EX1_379e")
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
		Buff(Summon.CARD, "EX1_366e"),
		Hit(SELF, 1)
	)

EX1_366e = buff(+1, +1)
