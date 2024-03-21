from ..utils import *


##
# Minions

class ULD_262:
	"""High Priest Amet"""
	# [x]Whenever you summon a minion, set its Health equal to this minion's.
	events = Summon(CONTROLLER, MINION).on(
		SetStateBuff(Summon.CARD, "ULD_262e")
	)


class ULD_262e:
	max_health = lambda self, _: self._xhealth


class ULD_266:
	"""Grandmummy"""
	# [x]<b>Reborn</b> <b>Deathrattle:</b> Give a random friendly minion +1/+1.
	deathrattle = Buff(RANDOM_OTHER_FRIENDLY_MINION, "ULD_266e")


ULD_266e = buff(+1, +1)


class ULD_268:
	"""Psychopomp"""
	# [x]<b>Battlecry:</b> Summon a random friendly minion that died this game. Give it
	# <b>Reborn</b>.
	play = Summon(CONTROLLER, Copy(RANDOM(FRIENDLY + KILLED + MINION))).then(
		GiveReborn(Summon.CARD)
	)


class ULD_269:
	"""Wretched Reclaimer"""
	# [x]<b>Battlecry:</b> Destroy a friendly minion, then return it to life with full
	# Health.
	requirements = {
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
	}
	play = Destroy(TARGET), Summon(CONTROLLER, Copy(TARGET))


class ULD_270:
	"""Sandhoof Waterbearer"""
	# At the end of your turn, restore #5 Health to a damaged friendly character.
	events = OWN_TURN_END.on(Heal(RANDOM(FRIENDLY + DAMAGED_CHARACTERS), 5))


##
# Spells

class ULD_265:
	"""Embalming Ritual"""
	# Give a minion <b>Reborn</b>.
	requirements = {
		PlayReq.REQ_TARGET_TO_PLAY: 0,
		PlayReq.REQ_MINION_TARGET: 0,
	}
	play = GiveReborn(TARGET)


class ULD_272:
	"""Holy Ripple"""
	# Deal $1 damage to all enemies. Restore #1_Health to all friendly characters.
	play = Hit(ENEMY_CHARACTERS, 1), Heal(FRIENDLY_CHARACTERS, 1)


class ULD_714:
	"""Penance"""
	# <b>Lifesteal</b> Deal $3 damage to a_minion.
	requirements = {
		PlayReq.REQ_TARGET_TO_PLAY: 0,
		PlayReq.REQ_MINION_TARGET: 0,
	}
	play = Hit(TARGET, 3)


class ULD_718:
	"""Plague of Death"""
	# <b>Silence</b> and destroy all_minions.
	play = Silence(ALL_MINIONS), Destroy(ALL_MINIONS)


class ULD_724:
	"""Activate the Obelisk"""
	# <b>Quest:</b> Restore 15_Health. <b>Reward:</b> Obelisk's Eye.
	progress_total = 15
	quest = Heal(source=FRIENDLY).after(AddProgress(SELF, Heal.TARGET, Heal.AMOUNT))
	reward = Summon(CONTROLLER, "ULD_724p")


class ULD_724p:
	"""Obelisk's Eye"""
	# <b>Hero Power</b> Restore #3 Health. If you target a minion, also give it +3/+3.
	requirements = {
		PlayReq.REQ_TARGET_TO_PLAY: 0,
	}
	play = Find(TARGET + MINION) & (
		Heal(TARGET, 3), Buff(TARGET, "ULD_724e")
	) | (
		Heal(TARGET, 3)
	)


ULD_724e = buff(+3, +3)
