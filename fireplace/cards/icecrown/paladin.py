from ..utils import *


##
# Minions

class ICC_034:
	"""Arrogant Crusader"""
	deathrattle = CurrentPlayer(OPPONENT) & Summon(CONTROLLER, "ICC_900t")


class ICC_245:
	"""Blackguard"""
	events = Heal(FRIENDLY_HERO).on(Hit(RANDOM_ENEMY_MINION, Heal.AMOUNT))


class ICC_801:
	"""Howling Commander"""
	play = ForceDraw(RANDOM(FRIENDLY_DECK + DIVINE_SHIELD))


class ICC_858:
	"""Bolvar, Fireblood"""
	events = LosesDivineShield(FRIENDLY_MINIONS).after(Buff(SELF, "ICC_858e"))


ICC_858e = buff(atk=2)


##
# Spells

class ICC_039:
	"""Dark Conviction"""
	play = Buff(TARGET, "ICC_039e")


class ICC_039e:
	atk = SET(3)
	max_health = SET(3)


class ICC_244:
	"""Desperate Stand"""
	play = Buff(TARGET, "ICC_244e")


class ICC_244e:
	tags = {GameTag.DEATHRATTLE: True}
	deathrattle = Summon(CONTROLLER, Copy(SELF)).then(SetCurrentHealth(Summon.CARD, 1))


##
# Weapons

class ICC_071:
	"""Light's Sorrow"""
	events = LosesDivineShield(FRIENDLY_MINIONS).after(Buff(SELF, "ICC_071e"))


ICC_071e = buff(atk=1)


##
# Heros

class ICC_829:
	"""Uther of the Ebon Blade"""
	play = Summon(CONTROLLER, "ICC_829t")


class ICC_829p:
	entourage = ["ICC_829t2", "ICC_829t3", "ICC_829t4", "ICC_829t5"]

	def activate(self):
		totems = [t for t in self.entourage if not self.controller.field.contains(t)]
		yield Summon(CONTROLLER, random.choice(totems))

	update = FindAll(
		FRIENDLY_MINIONS + ID("ICC_829t2"),
		FRIENDLY_MINIONS + ID("ICC_829t3"),
		FRIENDLY_MINIONS + ID("ICC_829t4"),
		FRIENDLY_MINIONS + ID("ICC_829t5")
	) & Destroy(ENEMY_HERO)
