from ..utils import *


##
# Minions

class UNG_020:
	"""Arcanologist"""
	play = ForceDraw(SECRET)


class UNG_021:
	"""Steam Surger"""
	play = PLAYED_ELEMENTAL_LAST_TURN(CONTROLLER) & Give(CONTROLLER, "UNG_018")


class UNG_027:
	"""Pyros"""
	deathrattle = Morph(SELF, "UNG_027t2").then(Give(CONTROLLER, Morph.CARD))


class UNG_027t4:
	deathrattle = Morph(SELF, "UNG_027t4").then(Give(CONTROLLER, Morph.CARD))


class UNG_846:
	"""Shimmering Tempest"""
	deathrattle = Give(CONTROLLER, RandomSpell(card_class=CardClass.MAGE))


##
# Spells

class UNG_018:
	"""Flame Geyser"""
	play = Hit(TARGET, 2), Give(CONTROLLER, "UNG_809t1")


class UNG_024:
	"""Mana Bind"""
	# Whether it will trigger when the hand is full ?
	secret = Play(OPPONENT, SPELL, MINION).on(FULL_BOARD | (
		Reveal(SELF), Give(CONTROLLER, Copy(Play.CARD)).then(Buff(Give.CARD, "UNG_024e"))
	))


class UNG_024e:
	cost = SET(0)
	events = REMOVED_IN_PLAY


class UNG_028:
	"""Open the Waygate"""
	events = Play(CONTROLLER, SPELL - IN_START_DECK).after(CompleteQuest(SELF))
	reward = Destroy(SELF), Give(CONTROLLER, "UNG_028t")


class UNG_028t:
	def play(self):
		self.game.extra_turn_stack.append(self.controller)


class UNG_941:
	"""Primordial Glyph"""
	play = DISCOVER(RandomSpell()).then(Buff(Discover.CARDS, "UNG_941e"))


UNG_941e = buff(cost=-2)


class UNG_948:
	"""Molten Reflection"""
	play = Summon(CONTROLLER, ExactCopy(TARGET))


class UNG_955:
	"""Meteor"""
	play = Hit(TARGET, 15), Hit(TARGET_ADJACENT, 3)
