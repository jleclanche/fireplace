from ..utils import *

class LOOT_101:
	"""
	Explosive Runes - (Spell)
	Secret: After your opponent plays a minion, deal $6 damage to it and any excess to their hero.
	https://hearthstone.gamepedia.com/Explosive_Runes
	"""
	pass
	# secret = Play(OPPONENT, MINION).after(
	# 	Reveal(SELF), Hit(Play.CARD, min(CURRENT_HEALTH(Play.CARD)), 6).then(Hit(ENEMY_HERO, ))
	# )

class LOOT_103:
	"""
	Lesser Ruby Spellstone - (Spell)
	Add 1 random Mage spell to your hand. @
	https://hearthstone.gamepedia.com/Lesser_Ruby_Spellstone
	"""
	play = Give(RandomSpell(card_class=CardClass.MAGE))
	reward = Morph(SELF, "LOOT_103t1")
	class Hand:
		events = Play(CONTROLLER, ELEMENTAL).on(UpdateSpellStone(1, 2))

class LOOT_103t1:
	"""
	Ruby Spellstone - (Spell)
	Add 2 random Mage spells to your hand. @
	https://hearthstone.gamepedia.com/Ruby_Spellstone
	"""
	play = Give(RandomSpell(card_class=CardClass.MAGE)) * 2
	reward = Morph(SELF, "LOOT_103t2")
	class Hand:
		events = Play(CONTROLLER, ELEMENTAL).on(UpdateSpellStone(1, 2))


class LOOT_103t2:
	"""
	Greater Ruby Spellstone - (Spell)
	Add 3 random Mage spells to your hand.
	https://hearthstone.gamepedia.com/Greater_Ruby_Spellstone
	"""
	play = Give(RandomSpell(card_class=CardClass.MAGE)) * 3


class LOOT_104:
	"""
	Shifting Scroll - (Spell)
	Each turn this is in your hand, transform it into a random Mage spell.
	https://hearthstone.gamepedia.com/Shifting_Scroll
	"""
	class Hand:
		events = OWN_TURN_BEGIN.on(Morph(SELF, RandomSpell(card_class=CardClass.MAGE)).then(
			Buff(Morph.CARD, "LOOT_104e"))
		)

class LOOT_104e:
	"""
	Shifting - (Enchantment)
	Transforming into random Mage spells.
	https://hearthstone.gamepedia.com/Shifting
	"""
	class Hand:
		events = OWN_TURN_BEGIN.on(Morph(SELF, RandomSpell(card_class=CardClass.MAGE)).then(
			Buff(Morph.CARD, "LOOT_104e"))
		)


class LOOT_106:
	"""
	Deck of Wonders - (Spell)
	Shuffle 5 Scrolls into your deck. When drawn, cast a random spell.
	https://hearthstone.gamepedia.com/Deck_of_Wonders
	"""
	play = Shuffle(CONTROLLER, "LOOT_106t") * 5


class LOOT_106t:
	"""
	Scroll of Wonder - (Spell)
	Cast a random spell. Draw a card. Cast this when drawn.
	https://hearthstone.gamepedia.com/Scroll_of_Wonder
	"""
	draw = Destroy(SELF), CastSpell(CastSpell(RandomSpell())), Draw(CONTROLLER)


class LOOT_108:
	"""
	Aluneth - (Weapon)
	At the end of your turn, draw 3 cards.
	https://hearthstone.gamepedia.com/Aluneth
	"""
	events = OWN_TURN_END.on(Draw(CONTROLLER) * 3)


class LOOT_170:
	"""
	Raven Familiar - (Minion)
	Battlecry: Reveal a spell in each deck. If yours costs more, draw it.
	https://hearthstone.gamepedia.com/Raven_Familiar
	"""
	play = JOUST_SPELL & Draw(CONTROLLER, Joust.CHALLENGER)


class LOOT_172:
	"""
	Dragon's Fury - (Spell)
	Reveal a spell from your deck. Deal damage equal to its Cost to all_minions.
	https://hearthstone.gamepedia.com/Dragon%27s_Fury
	"""
	play = Hit(ALL_MINIONS, COST(RANDOM(FRIENDLY_DECK + SPELL)))


class LOOT_231:
	"""
	Arcane Artificer - (Minion)
	Whenever you cast a spell, gain Armor equal to its_Cost.
	https://hearthstone.gamepedia.com/Arcane_Artificer
	"""
	play = Play(CONTROLLER, SPELL).on(GainArmor(CONTROLLER, COST(Play.CARD)))


class LOOT_535:
	"""
	Dragoncaller Alanna - (Minion)
	Battlecry: Summon a 5/5 Dragon for each spell you cast this game that costs (5) or more.
	https://hearthstone.gamepedia.com/Dragoncaller_Alanna
	"""
	play = Summon(CONTROLLER, "LOOT_535t") * Attr(CONTROLLER, "spells_played_this_game_cost_ge_5")


class LOOT_537:
	"""
	Leyline Manipulator - (Minion)
	Battlecry: If you're holding any cards that didn't start in your deck, reduce their Cost by (2).
	https://hearthstone.gamepedia.com/Leyline_Manipulator
	"""
	# TODO: Add 
	play = Buff(FRIENDLY_HAND - STARTING_DECK, "LOOT_537e")

LOOT_537e = buff(cost=-2)