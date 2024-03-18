from ..utils import *


##
# Minions

class GIL_125:
	"""Mad Hatter"""
	# [x]<b>Battlecry:</b> Randomly toss 3 hats to other minions. Each hat gives +1/+1.
	requirements = {
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_WITH_RACE: 11,
	}
	play = Buff(RANDOM_OTHER_MINION, "GIL_125e") * 3


GIL_125e = buff(+1, +1)


class GIL_202:
	"""Gilnean Royal Guard"""
	# [x]<b>Divine Shield</b>, <b>Rush</b> Each turn this is in your hand, swap its Attack
	# and Health.
	class Hand:
		events = OWN_TURN_BEGIN.on(Morph(SELF, Buff("GIL_202t", "GIL_200e")))


class GIL_202t:
	"""Gilnean Royal Guard"""
	# [x]<b>Stealth</b> Each turn this is in your hand, swap its Attack and Health.
	class Hand:
		events = OWN_TURN_BEGIN.on(Morph(SELF, Buff("GIL_202", "GIL_200e")))


class GIL_584:
	"""Witchwood Piper"""
	# [x]<b>Battlecry:</b> Draw the lowest Cost minion from your deck.
	play = ForceDraw(RANDOM(LOWEST_COST(FRIENDLY_DECK + MINION)))


class GIL_601:
	"""Scaleworm"""
	# <b>Battlecry:</b> If you're holding a Dragon, gain +1 Attack and <b>Rush</b>.
	powered_up = HOLDING_DRAGON
	play = powered_up & Buff(SELF, "GIL_601e")


GIL_601e = buff(atk=1, rush=True)


class GIL_622:
	"""Lifedrinker"""
	# [x]<b>Battlecry:</b> Deal 3 damage to the enemy hero. Restore 3 Health to your hero.
	play = Hit(ENEMY_HERO, 3), Heal(FRIENDLY_HERO, 3)


class GIL_623:
	"""Witchwood Grizzly"""
	# [x]<b>Taunt</b> <b>Battlecry:</b> Lose 1 Health for each card in your opponent's
	# hand.
	play = Buff(SELF, "GIL_623e") * Count(ENEMY_HERO)


GIL_623e = buff(health=-1)


class GIL_624:
	"""Night Prowler"""
	# <b>Battlecry:</b> If this is the only minion on the battlefield, gain +3/+3.
	play = Find(ALL_MINIONS - SELF) | Buff(SELF, "GIL_624e")


GIL_624e = buff(+3, +3)


class GIL_648:
	"""Chief Inspector"""
	# <b>Battlecry:</b> Destroy all enemy <b>Secrets</b>.
	play = Destroy(ENEMY_SECRETS)
