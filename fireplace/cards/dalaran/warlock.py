from ..utils import *


##
# Minions

class DAL_185:
	"""Aranasi Broodmother"""
	# [x]<b>Taunt</b> When you draw this, restore #4 Health to your hero.
	draw = Heal(FRIENDLY_HERO, 4)


class DAL_422:
	"""Arch-Villain Rafaam"""
	# <b><b>Taunt</b> Battlecry:</b> Replace your hand and deck with <b>Legendary</b>
	# minions.
	play = Morph(FRIENDLY_HAND + FRIENDLY_DECK, RandomLegendaryMinion())


class DAL_561:
	"""Jumbo Imp"""
	# Costs (1) less whenever a friendly Demon dies while this is in your hand.
	class Hand:
		events = Death(FRIENDLY + DEMON).on(Buff(SELF, "DAL_561e"))


class GVG_063e:
	tags = {GameTag.COST: -1}
	events = REMOVED_IN_PLAY


class DAL_563:
	"""Eager Underling"""
	# <b>Deathrattle:</b> Give two random friendly minions +2/+2.
	deathrattle = Buff(RANDOM_OTHER_FRIENDLY_MINION * 2, "DAL_563e")


DAL_563e = buff(+2, +2)


class DAL_606:
	"""EVIL Genius"""
	# <b>Battlecry:</b> Destroy a friendly minion to add 2 random
	# <b>Lackeys</b>_to_your_hand.
	play = Destroy(TARGET), Give(CONTROLLER, RandomLackey() * 2)


class DAL_607:
	"""Fel Lord Betrug"""
	# [x]Whenever you draw a minion, summon a copy with <b>Rush</b> that dies at end of
	# turn.
	events = Draw(CONTROLLER).on(
		Summon(CONTROLLER, Copy(Draw.CARD)).then(Buff(Summon.CARD, "DAL_607e"))
	)


class DAL_607e:
	tags = {GameTag.RUSH: True}
	events = OWN_TURN_END.on(Destroy(OWNER))


##
# Spells

class DAL_007:
	"""Rafaam's Scheme"""
	# Summon @ 1/1 |4(Imp, Imps). <i>(Upgrades each turn!)</i>
	class Hand:
		events = OWN_TURN_BEGIN.on(AddProgress(SELF, SELF))

	play = Summon(CONTROLLER, "DAL_751t") * (Attr(SELF, GameTag.QUEST_PROGRESS) + Number(1))


class DAL_173:
	"""Darkest Hour"""
	# Destroy all friendly minions. For each one, summon a random minion from your deck.
	play = Destroy(FRIENDLY_MINIONS).then(Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION)))


class DAL_602:
	"""Plot Twist"""
	# Shuffle your hand into your deck. Draw that many cards.
	def play(self):
		count = len(self.controller.hand)
		yield Shuffle(FRIENDLY_HAND)
		yield Draw(CONTROLLER) * count


class DAL_605:
	"""Impferno"""
	# Give your Demons +1 Attack. Deal $1 damage to all enemy minions.
	play = Buff(FRIENDLY_MINIONS + DEMON, "DAL_605e"), Hit(ENEMY_MINIONS, 1)


DAL_605e = buff(+1, +1)
