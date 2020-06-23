from ..utils import *


##
# Minions

class CFM_061:
	"""Jinyu Waterspeaker"""
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Heal(TARGET, 6)


class CFM_312:
	"""Jade Chieftain"""
	play = SummonJadeGolem(CONTROLLER).then(Taunt(SummonJadeGolem.CARD))


class CFM_324:
	"""White Eyes"""
	deathrattle = Shuffle(CONTROLLER, "CFM_324t")


class CFM_697:
	"""Lotus Illusionist"""
	events = Attack(SELF, ENEMY_HERO).after(Morph(SELF, RandomMinion(cost=6)))


##
# Spells

class CFM_310:
	"""Call in the Finishers"""
	requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
	play = Summon(CONTROLLER, "CFM_310t") * 4


class CFM_313:
	"""Finders Keepers"""
	play = DISCOVER(RandomCollectible(card_class=CardClass.SHAMAN, overload=True))


class CFM_696:
	"""Devolve"""
	requirements = {PlayReq.REQ_HERO_TARGET: 0}
	play = Evolve(ENEMY_MINIONS, -1)


class CFM_707:
	"""Jade Lightning"""
	requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	play = Hit(TARGET, 4), SummonJadeGolem(CONTROLLER)


##
# Weapons

class CFM_717:
	"""Jade Claws"""
	play = SummonJadeGolem(CONTROLLER)
