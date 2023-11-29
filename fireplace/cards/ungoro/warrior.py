from ..utils import *


##
# Minions

class UNG_838:
	"""Tar Lord"""
	update = CurrentPlayer(OPPONENT) & Refresh(SELF, {GameTag.ATK: +4})


class UNG_925:
	"""Ornery Direhorn"""
	play = Adapt(SELF)


class UNG_926:
	"""Cornered Sentry"""
	play = Summon(OPPONENT, "UNG_076t1") * 3


class UNG_933:
	"""King Mosh"""
	play = Destroy(ALL_MINIONS + DAMAGED)


class UNG_957:
	"""Direhorn Hatchling"""
	deathrattle = Shuffle(CONTROLLER, "UNG_957t1")


##
# Spells

class UNG_922:
	"""Explore Un'Goro"""
	play = Morph(FRIENDLY_DECK, "UNG_922t1")


class UNG_922t1:
	play = DISCOVER(RandomCollectible())


class UNG_923:
	"""Iron Hide"""
	play = GainArmor(FRIENDLY_HERO, 5)


class UNG_927:
	"""Sudden Genesis"""
	play = Summon(CONTROLLER, ExactCopy(FRIENDLY_MINIONS + DAMAGED))


class UNG_934:
	"""Fire Plume's Heart"""
	progress_total = 7
	quest = Play(CONTROLLER, TAUNT).after(AddProgress(SELF, Play.CARD))
	reward = Give(CONTROLLER, "UNG_934t1")


class UNG_934t1:
	play = Summon(CONTROLLER, "UNG_934t2")


class UNG_934t2:
	activate = Hit(RANDOM_ENEMY_CHARACTER, 8)


##
# Weapons

class UNG_929:
	"""Molten Blade"""
	class Hand:
		events = OWN_TURN_BEGIN.on(
			Morph(SELF, RandomWeapon()).then(Buff(Morph.CARD, "UNG_929e"))
		)


class UNG_929e:
	class Hand:
		events = OWN_TURN_BEGIN.on(
			Morph(OWNER, RandomWeapon()).then(Buff(Morph.CARD, "UNG_929e"))
		)
	events = REMOVED_IN_PLAY
