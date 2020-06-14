from ..utils import *


##
# Minions

class FP1_001:
	"""Zombie Chow"""
	deathrattle = Heal(ENEMY_HERO, 5)


class FP1_002:
	"""Haunted Creeper"""
	deathrattle = Summon(CONTROLLER, "FP1_002t"), Summon(CONTROLLER, "FP1_002t")


class FP1_003:
	"""Echoing Ooze"""
	play = OWN_TURN_END.on(Summon(CONTROLLER, ExactCopy(SELF)))


class FP1_004:
	"""Mad Scientist"""
	deathrattle = Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + SECRET))


class FP1_005:
	"""Shade of Naxxramas"""
	events = OWN_TURN_BEGIN.on(Buff(SELF, "FP1_005e"))


FP1_005e = buff(+1, +1)


class FP1_007:
	"""Nerubian Egg"""
	deathrattle = Summon(CONTROLLER, "FP1_007t")


class FP1_009:
	"""Deathlord"""
	deathrattle = Summon(OPPONENT, RANDOM(ENEMY_DECK + MINION))


class FP1_011:
	"""Webspinner"""
	deathrattle = Give(CONTROLLER, RandomBeast())


class FP1_012:
	"""Sludge Belcher"""
	deathrattle = Summon(CONTROLLER, "FP1_012t")


class FP1_013:
	"""Kel'Thuzad"""
	events = TURN_END.on(Summon(CONTROLLER, Copy(FRIENDLY + MINION + KILLED_THIS_TURN)))


class FP1_014:
	"""Stalagg"""
	deathrattle = Find(KILLED + ID("FP1_015")) & Summon(CONTROLLER, "FP1_014t")


class FP1_015:
	"""Feugen"""
	deathrattle = Find(KILLED + ID("FP1_014")) & Summon(CONTROLLER, "FP1_014t")


class FP1_016:
	"""Wailing Soul"""
	play = Silence(FRIENDLY_MINIONS)


class FP1_017:
	"""Nerub'ar Weblord"""
	update = Refresh(IN_HAND + MINION + BATTLECRY, {GameTag.COST: +2})


class FP1_022:
	"""Voidcaller"""
	deathrattle = Summon(CONTROLLER, RANDOM(FRIENDLY_HAND + DEMON))


class FP1_023:
	"""Dark Cultist"""
	deathrattle = Buff(RANDOM_OTHER_FRIENDLY_MINION, "FP1_023e")


FP1_023e = buff(health=3)


class FP1_024:
	"""Unstable Ghoul"""
	deathrattle = Hit(ALL_MINIONS, 1)


class FP1_026:
	"""Anub'ar Ambusher"""
	deathrattle = Bounce(RANDOM_FRIENDLY_MINION)


class FP1_027:
	"""Stoneskin Gargoyle"""
	events = OWN_TURN_BEGIN.on(Heal(SELF, DAMAGE(SELF)))


class FP1_028:
	"""Undertaker"""
	events = Summon(CONTROLLER, MINION + DEATHRATTLE).on(Buff(SELF, "FP1_028e"))


FP1_028e = buff(atk=1)


class FP1_029:
	"""Dancing Swords"""
	deathrattle = Draw(OPPONENT)


class FP1_030:
	"""Loatheb"""
	play = Buff(OPPONENT, "FP1_030e")


class FP1_030e:
	update = CurrentPlayer(OWNER) & Refresh(ENEMY_HAND + SPELL, {GameTag.COST: +5})
	events = OWN_TURN_BEGIN.on(Destroy(SELF))


class FP1_031:
	"""Baron Rivendare"""
	update = Refresh(CONTROLLER, {GameTag.EXTRA_DEATHRATTLES: True})


##
# Spells

class FP1_019:
	"""Poison Seeds"""
	def play(self):
		friendly_count = len(self.controller.field)
		enemy_count = len(self.controller.opponent.field)
		yield Destroy(ALL_MINIONS)
		yield Deaths()
		yield Summon(CONTROLLER, "FP1_019t") * friendly_count
		yield Summon(OPPONENT, "FP1_019t") * enemy_count


class FP1_025:
	"""Reincarnate"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Destroy(TARGET), Deaths(), Summon(CONTROLLER, Copy(TARGET))


##
# Secrets

class FP1_018:
	"""Duplicate"""
	secret = Death(FRIENDLY + MINION).on(FULL_HAND | (
		Reveal(SELF), Give(CONTROLLER, Copy(Death.ENTITY)) * 2
	))


class FP1_020:
	"""Avenge"""
	secret = Death(FRIENDLY + MINION).on(EMPTY_BOARD | (
		Reveal(SELF), Buff(RANDOM_FRIENDLY_MINION, "FP1_020e")
	))


FP1_020e = buff(+3, +2)


##
# Weapons

class FP1_021:
	"""Death's Bite"""
	deathrattle = Hit(ALL_MINIONS, 1)
