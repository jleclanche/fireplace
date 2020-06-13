from ..utils import *


##
# Minions

class CFM_060:
	"""Red Mana Wyrm"""
	events = OWN_SPELL_PLAY.on(Buff(SELF, "CFM_060e"))


CFM_060e = buff(atk=2)


class CFM_063:
	"""Kooky Chemist"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	play = Buff(TARGET, "CFM_063e")


CFM_063e = AttackHealthSwapBuff()


class CFM_067:
	"""Hozen Healer"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	play = Heal(TARGET, MAX_HEALTH(TARGET))


class CFM_120:
	"""Mistress of Mixtures"""
	deathrattle = Heal(ALL_HEROES, 4)


class CFM_619:
	"""Kabal Chemist"""
	play = Give(CONTROLLER, RandomPotion())


class CFM_646:
	"""Backstreet Leper"""
	deathrattle = Hit(ENEMY_HERO, 2)


class CFM_647:
	"""Blowgill Sniper"""
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Hit(TARGET, 1)


class CFM_648:
	"""Big-Time Racketeer"""
	play = Summon(CONTROLLER, "CFM_648t")


class CFM_651:
	"""Naga Corsair"""
	play = Buff(FRIENDLY_WEAPON, "CFM_651e")


CFM_651e = buff(atk=1)


class CFM_654:
	"""Friendly Bartender"""
	events = OWN_TURN_END.on(Heal(FRIENDLY_HERO, 1))


class CFM_655:
	"""Toxic Sewer Ooze"""
	play = Hit(ENEMY_WEAPON, 1)


class CFM_656:
	"""Streetwise Investigator"""
	play = Unstealth(ENEMY_MINIONS)


class CFM_659:
	"""Gadgetzan Socialite"""
	requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	play = Heal(TARGET, 2)


class CFM_715:
	"""Jade Spirit"""
	play = SummonJadeGolem(CONTROLLER)


class CFM_809:
	"""Tanaris Hogchopper"""
	play = Find(ENEMY_HAND) | GiveCharge(SELF)


class CFM_851:
	"""Daring Reporter"""
	events = Draw(OPPONENT).on(Buff(SELF, "CFM_851e"))


CFM_851e = buff(+1, +1)


class CFM_853:
	"""Grimestreet Smuggler"""
	play = Buff(RANDOM(FRIENDLY_HAND + MINION), "CFM_853e")


CFM_853e = buff(+1, +1)
