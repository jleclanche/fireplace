from ..utils import *


##
# Minions

class ULD_145:
	"""Brazen Zealot"""
	# Whenever you summon a minion, gain +1 Attack.
	events = Summon(CONTROLLER, MINION).on(Buff(SELF, "ULD_145e"))


ULD_145e = buff(atk=1)


class ULD_217:
	"""Micro Mummy"""
	# [x]<b>Reborn</b> At the end of your turn, give another random friendly minion +1
	# Attack.
	events = OWN_TURN_END.on(
		Buff(RANDOM_OTHER_FRIENDLY_MINION, "ULD_217e")
	)


ULD_217e = buff(atk=1)


class ULD_438:
	"""Salhet's Pride"""
	# <b>Deathrattle:</b> Draw two 1-Health minions from your_deck.
	deathrattle = ForceDraw(RANDOM(FRIENDLY_DECK + MINION + (CURRENT_HEALTH == 1)) * 2)


class ULD_439:
	"""Sandwasp Queen"""
	# <b>Battlecry:</b> Add two 2/1 Sandwasps to your hand.
	play = Give(CONTROLLER, "ULD_439t") * 2


class ULD_500:
	"""Sir Finley of the Sands"""
	# [x]<b>Battlecry:</b> If your deck has no duplicates, <b>Discover</b> an upgraded Hero
	# Power.
	powered_up = -FindDuplicates(FRIENDLY_DECK)
	play = powered_up & GenericChoice(CONTROLLER, RandomUpgradedHeroPower() * 3)


##
# Spells

class ULD_143:
	"""Pharaoh's Blessing"""
	# Give a minion +4/+4, <b>Divine Shield</b>, and <b>Taunt</b>.
	requirements = {
		PlayReq.REQ_TARGET_TO_PLAY: 0,
		PlayReq.REQ_MINION_TARGET: 0,
	}
	play = Buff(TARGET, "ULD_143e"), GiveDivineShield(TARGET)


ULD_143e = buff(+4, +4, taunt=True)


class ULD_431:
	"""Making Mummies"""
	# [x]<b>Quest:</b> Play 5 <b>Reborn</b> minions. <b>Reward:</b> Emperor Wraps.
	progress_total = 5
	quest = Play(CONTROLLER, REBORN + MINION).after(AddProgress(SELF, Play.CARD))
	reward = Summon(CONTROLLER, "ULD_431p")


class ULD_431p:
	"""Emperor Wraps"""
	# [x]<b>Hero Power</b> Summon a 2/2 copy of a friendly minion.
	requirements = {
		PlayReq.REQ_TARGET_TO_PLAY: 0,
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_NUM_MINION_SLOTS: 1,
	}
	activate = Summon(CONTROLLER, Buff(ExactCopy(TARGET), "ULD_431e"))


class ULD_431e:
	atk = SET(2)
	max_health = SET(2)


class ULD_716:
	"""Tip the Scales"""
	# Summon 7 Murlocs from your deck.
	requirements = {
		PlayReq.REQ_MINION_TARGET: 0,
	}
	play = Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MURLOC) * 7)


class ULD_728:
	"""Subdue"""
	# Set a minion's Attack and Health to 1.
	requirements = {
		PlayReq.REQ_TARGET_TO_PLAY: 0,
		PlayReq.REQ_MINION_TARGET: 0,
	}
	play = Buff(TARGET, "ULD_728e")


class ULD_728e:
	atk = SET(1)
	max_health = SET(1)
