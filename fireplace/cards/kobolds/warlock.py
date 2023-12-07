from ..utils import *


##
# Minions

class LOOT_013:
	"""Vulgar Homunculus"""
	# <b>Taunt</b> <b>Battlecry:</b> Deal 2 damage to your hero.
	play = Hit(FRIENDLY_HERO, 2)


class LOOT_014:
	"""Kobold Librarian"""
	# <b>Battlecry:</b> Draw a card. Deal 2 damage to your_hero.
	play = Draw(CONTROLLER), Hit(FRIENDLY_HERO, 2)


class LOOT_018:
	"""Hooked Reaver"""
	# <b>Battlecry:</b> If you have 15 or_less Health, gain +3/+3_and <b>Taunt</b>.
	play = (CURRENT_HEALTH(FRIENDLY_HERO) <= 15) & Buff(SELF, "LOOT_018e")


LOOT_018e = buff(+3, +3, taunt=True)


class LOOT_306:
	"""Possessed Lackey"""
	# <b>Deathrattle:</b> <b>Recruit</b> a_Demon.
	deathrattle = Recruit(DEMON)


class LOOT_368:
	"""Voidlord"""
	# [x]<b>Taunt</b> <b>Deathrattle:</b> Summon three 1/3 Demons with <b>Taunt</b>.
	deathrattle = Summon(CONTROLLER, "CS2_065") * 3


class LOOT_415:
	"""Rin, the First Disciple"""
	# <b>Taunt</b> <b>Deathrattle:</b> Add 'The First Seal' to your hand.
	deathrattle = Give(CONTROLLER, "LOOT_415t1")


class LOOT_415t1:
	"""The First Seal"""
	# Summon a 2/2 Demon. Add 'The Second Seal' to your hand.
	play = Summon(CONTROLLER, "LOOT_415t1t"), Give(CONTROLLER, "LOOT_415t2")


class LOOT_415t2:
	"""The Second Seal"""
	# Summon a 3/3 Demon. Add 'The Third Seal' to your hand.
	play = Summon(CONTROLLER, "LOOT_415t2t"), Give(CONTROLLER, "LOOT_415t3")


class LOOT_415t3:
	"""The Third Seal"""
	# Summon a 4/4 Demon. Add 'The Fourth Seal' to your hand.
	play = Summon(CONTROLLER, "LOOT_415t3t"), Give(CONTROLLER, "LOOT_415t4")


class LOOT_415t4:
	"""The Fourth Seal"""
	# Summon a 5/5 Demon. Add 'The Final Seal' to your hand.
	play = Summon(CONTROLLER, "LOOT_415t4t"), Give(CONTROLLER, "LOOT_415t5")


class LOOT_415t5:
	"""The Final Seal"""
	# [x]Summon a 6/6 Demon. Add 'Azari, the Devourer' to your hand.
	play = Summon(CONTROLLER, "LOOT_415t5t"), Give(CONTROLLER, "LOOT_415t6")


class LOOT_415t6:
	"""Azari, the Devourer"""
	# <b>Battlecry:</b> Destroy your opponent's deck.
	play = Destroy(ENEMY_DECK)


##
# Spells

class LOOT_017:
	"""Dark Pact"""
	# Destroy a friendly minion. Restore #8 Health to your hero.
	play = Destroy(TARGET), Heal(FRIENDLY_HERO, 8)


class LOOT_043:
	"""Lesser Amethyst Spellstone"""
	# <b>Lifesteal.</b> Deal $3 damage to a minion. <i>(Take damage from your cards to
	# upgrade.)</i>
	play = Hit(TARGET, 3)

	class Hand:
		events = Damage(FRIENDLY_HERO, None, FRIENDLY).on(Morph(SELF, "LOOT_043t2"))


class LOOT_043t2:
	"""Amethyst Spellstone"""
	# <b>Lifesteal.</b> Deal $5 damage to a minion. <i>(Take damage from your cards to
	# upgrade.)</i>
	play = Hit(TARGET, 5)

	class Hand:
		events = Damage(FRIENDLY_HERO, None, FRIENDLY).on(Morph(SELF, "LOOT_043t3"))


class LOOT_043t3:
	"""Greater Amethyst Spellstone"""
	# <b>Lifesteal.</b> Deal $7 damage to a minion.
	play = Hit(TARGET, 7)


class LOOT_417:
	"""Cataclysm"""
	# Destroy all minions. Discard your hand.
	play = Destroy(ALL_MINIONS), Discard(FRIENDLY_HAND)


##
# Weapons

class LOOT_420:
	"""Skull of the Man'ari"""
	# At the start of your turn, summon a Demon from your hand.
	events = OWN_TURN_BEGIN.on(Give(CONTROLLER, RandomDemon()))
