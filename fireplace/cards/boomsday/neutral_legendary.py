from ..utils import *


##
# Minions

class BOT_424:
	"""Mecha'thun"""
	# [x]<b>Deathrattle:</b> If you have no cards in your deck, hand, and battlefield,
	# destroy the enemy hero.
	deathrattle = Find(
		FRIENDLY_DECK | FRIENDLY_HAND | FRIENDLY_MINIONS
	) | Destroy(ENEMY_HERO)


class BOT_548:
	"""Zilliax"""
	# <b>Magnetic</b> <b><b>Divine Shield</b>, <b>Taunt</b>, Lifesteal, Rush</b>
	magnetic = MAGNETIC("BOT_548e")


class BOT_548e:
	tags = {
		GameTag.TAUNT: True,
		GameTag.LIFESTEAL: True,
		GameTag.RUSH: True
	}

	def apply(self, target):
		self.game.trigger(self, (GiveDivineShield(target), ), None)


class BOT_555:
	"""Harbinger Celestia"""
	# [x]<b>Stealth</b> After your opponent plays a minion, become a copy of it.
	events = Play(OPPONENT, MINION).after(
		Morph(SELF, ExactCopy(Play.CARD))
	)


class BOT_573:
	"""Subject 9"""
	# <b>Battlecry:</b> Draw 5 different <b>Secrets</b> from your deck.
	play = ForceDraw(RANDOM(DeDuplicate(FRIENDLY_DECK + SECRET)) * 5)
