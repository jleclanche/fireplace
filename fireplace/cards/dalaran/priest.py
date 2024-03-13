from ..utils import *


##
# Minions

class DAL_030:
	"""Shadowy Figure"""
	# <b>Battlecry:</b> Transform into a_2/2 copy of a friendly <b>Deathrattle</b> minion.
	play = Morph(SELF, ExactCopy(TARGET)).then(
		Buff(Morph.CARD, "DAL_030e"))


class DAL_030e:
	atk = SET(2)
	max_health = SET(2)


class DAL_039:
	"""Convincing Infiltrator"""
	# [x]<b><b>Taunt</b></b> <b>Deathrattle:</b> Destroy a random enemy minion.
	deathrattle = Destroy(RANDOM(ENEMY_MINIONS))


class DAL_040:
	"""Hench-Clan Shadequill"""
	# <b>Deathrattle:</b> Restore 5 Health to the enemy hero.
	deathrattle = Heal(ENEMY_HERO, 5)


class DAL_413:
	"""EVIL Conscripter"""
	# <b>Deathrattle:</b> Add a <b>Lackey</b> to your hand.
	deathrattle = Give(CONTROLLER, RandomLackey())


class DAL_721:
	"""Catrina Muerte"""
	# [x]At the end of your turn, summon a friendly minion that died this game.
	events = OWN_TURN_END.on(Summon(CONTROLLER, Copy(RANDOM(FRIENDLY + KILLED + MINION))))


class DAL_729:
	"""Madame Lazul"""
	# [x]<b>Battlecry:</b> <b>Discover</b> a copy of a card in your opponent's hand.
	play = GenericChoice(CONTROLLER, Copy(RANDOM(DeDuplicate(ENEMY_HAND)) * 3))


##
# Spells

class DAL_011:
	"""Lazul's Scheme"""
	# Reduce the Attack of an enemy minion by @ until your next turn. <i>(Upgrades each
	# turn!)</i>
	# TODO need test
	class Hand:
		events = OWN_TURN_BEGIN.on(AddProgress(SELF, SELF))

	play = Buff(ENEMY_MINIONS, "DAL_011e") * (Attr(SELF, GameTag.QUEST_PROGRESS) + Number(1))


class DAL_011e:
	tags = {GameTag.ATK: -1}
	events = OWN_TURN_BEGIN.on(Destroy(SELF))


class DAL_065:
	"""Unsleeping Soul"""
	# <b>Silence</b> a friendly minion, then summon a copy of it.
	play = Silence(TARGET), Summon(CONTROLLER, ExactCopy(TARGET))


class DAL_723:
	"""Forbidden Words"""
	# [x]Spend all your Mana. Destroy a minion with that much Attack or less.
	play = SpendMana(CONTROLLER, CURRENT_MANA(CONTROLLER)), Destroy(TARGET)


class DAL_724:
	"""Mass Resurrection"""
	# Summon 3 friendly minions that died this game.
	pass
