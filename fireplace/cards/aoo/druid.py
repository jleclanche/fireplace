from ..utils import *


##
# Minions

class BT_136:
	"""Archspore Msshi'fn"""
	deathrattle = Shuffle(CONTROLLER, "BT_136t")


class BT_136t:
	"""Msshi'fn Prime"""
	choose = ("BT_136ta", "BT_136tb")
	play = ChooseBoth(CONTROLLER) & (Summon(CONTROLLER, "BT_136tt3"))


class BT_136ta:
	play = Summon(CONTROLLER, "BT_136tt")


class BT_136tb:
	play = Summon(CONTROLLER, "BT_136tt2")


class BT_127:
	"""Imprisoned Satyr"""
	dormant = 2
	awaken = Buff(RANDOM(FRIENDLY_HAND + MINION), "BT_127e")


BT_127e = buff(cost=-5)


class BT_133:
	"""Marsh Hydra"""
	events = Attack(SELF).after(Give(CONTROLLER, RandomMinion(cost=8)))


class BT_131:
	"""Ysiel Windsinger"""
	update = Refresh(FRIENDLY_HAND + SPELL, {GameTag.COST: 1})


##
# Spells

class BT_132:
	"""Ironbark"""
	requirements = {
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Buff(TARGET, "BT_132e")
	update = (MANA(CONTROLLER) >= 7) & Refresh(SELF, {GameTag.COST: SET(0)})


BT_132e = buff(atk=1, health=1, taunt=True)


class BT_134:
	"""Bogbeam"""
	requirements = {
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Hit(TARGET, 3)
	update = (MANA(CONTROLLER) >= 7) & Refresh(SELF, {GameTag.COST: SET(0)})


class BT_128:
	"""Fungal Fortunes"""
	play = Draw(CONTROLLER).then(Discard(Draw.CARD + MINION)) * 3


class BT_129:
	"""Germination"""
	requirements = {
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Summon(CONTROLLER, ExactCopy(TARGET)).then(Buff(Summon.CARD, "BT_129e"))


BT_129e = buff(taunt=True)


class BT_130:
	"""Overgrowth"""
	play = GainEmptyMana(CONTROLLER, 2)


class BT_135:
	"""Glowfly Swarm"""
	play = Summon(CONTROLLER, "BT_135t") * Count(FRIENDLY_HAND + SPELL)
