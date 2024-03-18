from ..utils import *


##
# Minions

class ICC_210:
	"""Shadow Ascendant"""
	events = OWN_TURN_END.on(Buff(RANDOM(FRIENDLY_MINIONS - SELF), "ICC_210e"))


ICC_210e = buff(+1, +1)


class ICC_214:
	"""Obsidian Statue"""
	deathrattle = Destroy(RANDOM_ENEMY_MINION)


class ICC_215:
	"""Archbishop Benedictus"""
	play = Shuffle(CONTROLLER, ExactCopy(ENEMY_DECK))


##
# Spells

class ICC_207:
	"""Devour Mind"""
	play = Give(CONTROLLER, Copy(RANDOM(ENEMY_DECK) * 3))


class ICC_213:
	"""Eternal Servitude"""
	requirements = {
		PlayReq.REQ_FRIENDLY_MINION_DIED_THIS_GAME: 0,
		PlayReq.REQ_NUM_MINION_SLOTS: 1,
	}
	play = Choice(CONTROLLER, Copy(RANDOM(DeDuplicate(FRIENDLY + KILLED + MINION)) * 3)).then(
		Summon(CONTROLLER, Choice.CARD)
	)


class ICC_235:
	"""Shadow Essence"""
	requirements = {
		PlayReq.REQ_NUM_MINION_SLOTS: 1,
	}
	play = Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION)).then(
		Buff(Summon.CARD, "ICC_235e")
	)


class ICC_235e:
	atk = SET(5)
	max_health = SET(5)


class ICC_802:
	"""Spirit Lash"""
	play = Hit(ALL_MINIONS, 1)


class ICC_849:
	"""Embrace Darkness"""
	requirements = {
		PlayReq.REQ_TARGET_TO_PLAY: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_ENEMY_TARGET: 0,
	}
	play = Buff(TARGET, "ICC_849e")


class ICC_849e:
	events = OWN_TURN_BEGIN.on(
		Steal(OWNER), Destroy(SELF)
	)


##
# Heros

class ICC_830:
	"""Shadowreaper Anduin"""
	play = Destroy(ALL_MINIONS + (ATK >= 5))


class ICC_830p:
	requirements = {
		PlayReq.REQ_TARGET_TO_PLAY: 0,
	}
	activate = Hit(TARGET, 2)
	events = Play(CONTROLLER).after(RefreshHeroPower(SELF))
