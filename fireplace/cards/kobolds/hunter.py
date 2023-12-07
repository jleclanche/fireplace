from ..utils import *


##
# Minions

class LOOT_078:
	"""Cave Hydra"""
	# Also damages the minions next to whomever this attacks.
	events = Attack(SELF).on(CLEAVE)


class LOOT_511:
	"""Kathrena Winterwisp"""
	# <b>Battlecry and Deathrattle:</b> <b>Recruit</b> a Beast.
	play = deathrattle = Recruit(BEAST)


class LOOT_520:
	"""Seeping Oozeling"""
	# <b>Battlecry:</b> Gain the <b>Deathrattle</b> of a random minion in your deck.
	play = Buff(SELF, "LOOT_520e").then(
		CopyDeathrattles(Buff.BUFF, RANDOM(FRIENDLY_DECK + MINION + DEATHRATTLE)))


LOOT_520e = buff(deathrattle=True)


##
# Spells

class LOOT_077:
	"""Flanking Strike"""
	# Deal $3 damage to a minion. Summon a 3/3 Wolf.
	play = Hit(3, TARGET), Summon(CONTROLLER, "LOOT_077t")


class LOOT_079:
	"""Wandering Monster"""
	# <b>Secret:</b> When an enemy attacks your hero, summon a 3-Cost minion as the new
	# target.
	secret = Attack(ENEMY_MINIONS, FRIENDLY_HERO).on(
		Reveal(SELF), Retarget(Attack.ATTACKER, Summon(CONTROLLER, RandomMinion(cost=3)))
	)


class LOOT_080:
	"""Lesser Emerald Spellstone"""
	# Summon two 3/3_Wolves. <i>(Play a <b>Secret</b> to upgrade.)</i>
	pass


class LOOT_217:
	"""To My Side!"""
	# [x]Summon an Animal Companion, or 2 if your deck has no minions.
	pass


class LOOT_522:
	"""Crushing Walls"""
	# Destroy your opponent's left and right-most minions.
	pass


##
# Weapons

class LOOT_085:
	"""Rhok'delar"""
	# <b>Battlecry:</b> If your deck has no minions, fill your_hand with Hunter_spells.
	pass


class LOOT_222:
	"""Candleshot"""
	# Your hero is <b>Immune</b> while attacking.
	pass
