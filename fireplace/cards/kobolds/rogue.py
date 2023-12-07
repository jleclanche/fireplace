from ..utils import *


##
# Minions

class LOOT_026:
	"""Fal'dorei Strider"""
	# [x]<b>Battlecry:</b> Shuffle 3 Ambushes into your deck. When drawn, summon a 4/4
	# Spider.
	play = Shuffle(CONTROLLER, "LOOT_026e") * 3


class LOOT_026e:
	"""Spider Ambush!"""
	# Summon a 4/4 Spider. Draw a card. Cast this when drawn.
	play = Summon(CONTROLLER, "LOOT_026t")
	draw = CAST_WHEN_DRAWN


class LOOT_033:
	"""Cavern Shinyfinder"""
	# <b>Battlecry:</b> Draw a weapon from your deck.
	play = ForceDraw(RANDOM(FRIENDLY_DECK + WEAPON))


class LOOT_165:
	"""Sonya Shadowdancer"""
	# After a friendly minion dies, add a 1/1 copy of it to your hand. It costs (1).
	events = Death(FRIENDLY + MINION).on(
		Give(CONTROLLER, Buff(Death.ENTITY, "LOOT_165e"))
	)


class LOOT_165e:
	atk = SET(1)
	max_health = SET(1)


class LOOT_211:
	"""Elven Minstrel"""
	# <b>Combo:</b> Draw 2 minions from your deck.
	combo = ForceDraw(RANDOM(FRIENDLY_DECK + MINION))


class LOOT_412:
	"""Kobold Illusionist"""
	# <b>Deathrattle:</b> Summon a 1/1 copy of a minion from your hand.
	deathrattle = Summon(CONTROLLER, Buff(RANDOM(FRIENDLY_HAND + MINION), "LOOT_412e"))


class LOOT_412e:
	atk = SET(1)
	max_health = SET(1)


##
# Spells

class LOOT_204:
	"""Cheat Death"""
	# <b>Secret:</b> When a friendly minion dies, return it to your hand. It costs (2)
	# less.
	secret = Death(FRIENDLY + MINION).on(
		Reveal(SELF),
		Bounce(Buff(Death.ENTITY, "LOOT_204e"))
	)


class LOOT_204e:
	tags = {GameTag.COST: -2}
	events = REMOVED_IN_PLAY


class LOOT_210:
	"""Sudden Betrayal"""
	# <b>Secret:</b> When a minion attacks your hero, instead it attacks one of_its
	# neighbors.
	secret = Attack(MINION, FRIENDLY_HERO).on(Find(ADJACENT(Attack.ATTACKER)) & (
		Reveal(SELF), Retarget(Attack.ATTACKER, RANDOM(ADJACENT(Attack.ATTACKER)))
	))


class LOOT_214:
	"""Evasion"""
	# <b>Secret:</b> After your hero takes damage, become <b>Immune</b> this turn.
	secret = Damage(FRIENDLY_HERO).on(
		Buff(FRIENDLY_HERO, "LOOT_214e")
	)


LOOT_214e = buff(immune=True)


class LOOT_503:
	"""Lesser Onyx Spellstone"""
	# Destroy 1 random enemy minion. @<i>(Play 3 <b>Deathrattle</b> cards to upgrade.)</i>
	play = Destroy(RANDOM_ENEMY_MINION)
	progress_total = 3
	reward = Morph(SELF, "LOOT_503t")

	class Hand:
		events = Play(CONTROLLER, DEATHRATTLE).after(AddProgress(SELF, Play.CARD))


class LOOT_503t:
	"""Onyx Spellstone"""
	# Destroy up to 2 random enemy minions. @
	play = Destroy(RANDOM_ENEMY_MINION * 2)
	progress_total = 3
	reward = Morph(SELF, "LOOT_503t")

	class Hand:
		events = Play(CONTROLLER, DEATHRATTLE).after(AddProgress(SELF, Play.CARD))


class LOOT_503t2:
	"""Greater Onyx Spellstone"""
	# Destroy up to 3 random enemy minions.
	play = Destroy(RANDOM_ENEMY_MINION * 3)


##
# Weapons

class LOOT_542:
	"""Kingsbane"""
	# [x]<b>Deathrattle:</b> Shuffle this into your deck. It keeps any enchantments.
	tags = {enums.KEEP_BUFF: True}
	deathrattle = Shuffle(CONTROLLER, SELF)
