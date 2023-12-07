from ..utils import *


##
# Minions

class LOOT_170:
	"""Raven Familiar"""
	# <b>Battlecry:</b> Reveal a spell in each deck. If yours costs more, draw it.
	play = JOUST_SPELL & ForceDraw(Joust.CHALLENGER)


class LOOT_231:
	"""Arcane Artificer"""
	# Whenever you cast a spell, gain Armor equal to its_Cost.
	events = Play(CONTROLLER, SPELL).after(GainArmor(FRIENDLY_HERO, COST(Play.CARD)))


class LOOT_535:
	"""Dragoncaller Alanna"""
	# <b>Battlecry:</b> Summon a 5/5 Dragon for each spell you cast this game that costs
	# (5) or more.
	play = SummonBothSides(CONTROLLER, "LOOT_535t") * Count(
		CARDS_PLAYED_THIS_GAME + SPELL + (COST >= 5))


class LOOT_537:
	"""Leyline Manipulator"""
	# <b>Battlecry:</b> If you're holding any cards that didn't start in your deck, reduce
	# their Cost by (2).
	play = Buff(FRIENDLY_HAND + STARTING_DECK, "LOOT_537e")


@custom_card
class LOOT_537e:
	tags = {
		GameTag.CARDNAME: "Leyline Manipulator Buff",
		GameTag.CARDTYPE: CardType.ENCHANTMENT,
		GameTag.COST: -2,
	}
	events = REMOVED_IN_PLAY


##
# Spells

class LOOT_101:
	"""Explosive Runes"""
	# <b>Secret:</b> After your opponent plays a minion, deal $6 damage to it and any
	# excess to their hero.
	secret = Play(OPPONENT, MINION).on(
		Reveal(SELF), HitAndExcessDamageToHero(Play.CARD, 6)
	)


class LOOT_103:
	"""Lesser Ruby Spellstone"""
	# Add 1 random Mage spell to your hand. @<i>(Play 2 Elementals to_upgrade.)</i>
	play = Give(CONTROLLER, RandomSpell(card_class=CardClass.MAGE))
	progress_total = 2
	reward = Morph(SELF, "LOOT_103t1")

	class Hand:
		events = Play(CONTROLLER, ELEMENTAL).after(AddProgress(SELF, Play.CARD))


class LOOT_103t1:
	"""Ruby Spellstone"""
	# Add 2 random Mage spells to your hand. @
	play = Give(CONTROLLER, RandomSpell(card_class=CardClass.MAGE)) * 2
	progress_total = 2
	reward = Morph(SELF, "LOOT_103t2")

	class Hand:
		events = Play(CONTROLLER, ELEMENTAL).after(AddProgress(SELF, Play.CARD))


class LOOT_103t2:
	"""Greater Ruby Spellstone"""
	# Add 3 random Mage spells to your hand.
	play = Give(CONTROLLER, RandomSpell(card_class=CardClass.MAGE)) * 3


class LOOT_104:
	"""Shifting Scroll"""
	# Each turn this is in your hand, transform it into a random Mage spell.
	class Hand:
		events = OWN_TURN_BEGIN.on(
			Morph(SELF, RandomSpell(card_class=CardClass.MAGE)).then(
				Buff(Morph.CARD, "LOOT_104e"))
		)


class LOOT_104e:
	class Hand:
		events = OWN_TURN_BEGIN.on(
			Morph(SELF, RandomSpell(card_class=CardClass.MAGE)).then(
				Buff(Morph.CARD, "LOOT_104e"))
		)
	events = REMOVED_IN_PLAY


class LOOT_106:
	"""Deck of Wonders"""
	# Shuffle 5 Scrolls into your deck. When drawn, cast a random spell.
	play = Shuffle(CONTROLLER, "LOOT_106t") * 5


class LOOT_106t:
	"""Scroll of Wonder"""
	# Cast a random spell. Draw a card. Cast this when drawn.
	play = CastSpell(RandomSpell())
	draw = CAST_WHEN_DRAWN


class LOOT_172:
	"""Dragon's Fury"""
	# Reveal a spell from your deck. Deal damage equal to its Cost to all_minions.
	play = Reveal(RANDOM(FRIENDLY_DECK + SPELL)).then(
		Hit(ALL_MINIONS, COST(Reveal.TARGET))
	)


##
# Weapons

class LOOT_108:
	"""Aluneth"""
	# At the end of your turn, draw 3 cards.
	events = OWN_TURN_END.on(Draw(CONTROLLER) * 3)
