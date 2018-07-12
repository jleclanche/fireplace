from ..utils import *


##
# Hero Powers

class CS2_101:
	"""Reinforce (Uther Lightbringer)"""
	activate = Summon(CONTROLLER, "CS2_101t")


class CS2_101_H1:
	"""Reinforce (Lady Liadrin)"""
	activate = CS2_101.activate


##
# Minions

class CS2_088:
	"""Guardian of Kings"""
	play = Heal(FRIENDLY_HERO, 6)


class EX1_362:
	"""Argent Protector"""
	play = GiveDivineShield(TARGET)


class EX1_382:
	"""Aldor Peacekeeper"""
	play = Buff(TARGET, "EX1_382e")


class EX1_382e:
	atk = SET(1)


class EX1_383:
	"""Tirion Fordring"""
	deathrattle = Summon(CONTROLLER, "EX1_383t")


##
# Spells

class CS2_087:
	"""Blessing of Might"""
	play = Buff(TARGET, "CS2_087e")


CS2_087e = buff(atk=3)


class CS2_089:
	"""Holy Light"""
	play = Heal(TARGET, 6)


class CS2_092:
	"""Blessing of Kings"""
	play = Buff(TARGET, "CS2_092e")


CS2_092e = buff(+4, +4)


class CS2_093:
	"""Consecration"""
	play = Hit(ENEMY_CHARACTERS, 2)


class CS2_094:
	"""Hammer of Wrath"""
	play = Hit(TARGET, 3), Draw(CONTROLLER)


class EX1_349:
	"""Divine Favor"""
	play = DrawUntil(CONTROLLER, Count(ENEMY_HAND))


class EX1_354:
	"""Lay on Hands"""
	play = Heal(TARGET, 8), Draw(CONTROLLER) * 3


class EX1_355:
	"""Blessed Champion"""
	play = Buff(TARGET, "EX1_355e")


class EX1_355e:
	atk = lambda self, i: i * 2


class EX1_360:
	"""Humility"""
	play = Buff(TARGET, "EX1_360e")


class EX1_360e:
	atk = SET(1)


class EX1_363:
	"""Blessing of Wisdom"""
	play = Buff(TARGET, "EX1_363e")


class EX1_363e:
	events = Attack(OWNER).on(Draw(CONTROLLER))


class EX1_363e2:
	"""Blessing of Wisdom (Unused)"""
	events = Attack(OWNER).on(Draw(OWNER_OPPONENT))


class EX1_365:
	"""Holy Wrath"""
	play = Draw(CONTROLLER).then(Hit(TARGET, COST(Draw.CARD)))


class EX1_371:
	"""Hand of Protection"""
	play = GiveDivineShield(TARGET)


class EX1_384:
	"""Avenging Wrath"""
	def play(self):
		count = self.controller.get_spell_damage(8)
		yield Hit(RANDOM_ENEMY_CHARACTER, 1) * count


class EX1_619:
	"""Equality"""
	play = Buff(ALL_MINIONS, "EX1_619e")


class EX1_619e:
	max_health = SET(1)


##
# Secrets

class EX1_130:
	"""Noble Sacrifice"""
	secret = Attack(ENEMY_MINIONS).on(FULL_BOARD | (
		Reveal(SELF), Retarget(Attack.ATTACKER, Summon(CONTROLLER, "EX1_130a"))
	))


class EX1_132:
	"""Eye for an Eye"""
	secret = Damage(FRIENDLY_HERO).on(
		Reveal(SELF), Hit(ENEMY_HERO, Damage.AMOUNT)
	)


class EX1_136:
	"""Redemption"""
	secret = Death(FRIENDLY + MINION).on(FULL_BOARD | (
		Reveal(SELF),
		Summon(CONTROLLER, Copy(Death.ENTITY)).then(SetCurrentHealth(Summon.CARD, 1))
	))


class EX1_379:
	"""Repentance"""
	secret = Play(OPPONENT, MINION | HERO).after(
		Reveal(SELF), Buff(Play.CARD, "EX1_379e")
	)


class EX1_379e:
	max_health = SET(1)


##
# Weapons

class CS2_097:
	"""Truesilver Champion"""
	events = Attack(FRIENDLY_HERO).on(Heal(FRIENDLY_HERO, 2))


class EX1_366:
	"""Sword of Justice"""
	events = Summon(CONTROLLER, MINION).after(
		Buff(Summon.CARD, "EX1_366e"),
		Hit(SELF, 1)
	)


EX1_366e = buff(+1, +1)
