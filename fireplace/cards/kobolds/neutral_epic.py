from ..utils import *


##
# Minions

class LOOT_130:
	"""Arcane Tyrant"""
	# Costs (0) if you've cast a spell that costs (5) or more this turn.
	class Hand:
		events = Play(CONTROLLER, SPELL + (COST >= 5)).after(Buff(SELF, "LOOT_130e"))


@custom_card
class LOOT_130e:
	tags = {
		GameTag.CARDNAME: "Arcane Tyrant Buff",
		GameTag.CARDTYPE: CardType.ENCHANTMENT,
		GameTag.TAG_ONE_TURN_EFFECT: True,
	}
	cost = SET(0)
	events = REMOVED_IN_PLAY


class LOOT_149:
	"""Corridor Creeper"""
	# Costs (1) less whenever a minion dies while this is_in_your hand.
	class Hand:
		events = Death(MINION).on(Buff(SELF, "LOOT_149e"))


LOOT_149e = buff(cost=-1)


class LOOT_161:
	"""Carnivorous Cube"""
	# <b>Battlecry:</b> Destroy a friendly minion. <b>Deathrattle:</b> Summon 2 copies of
	# it.
	play = Destroy(TARGET)
	deathrattle = Summon(CONTROLLER, TARGET) * 2


class LOOT_193:
	"""Shimmering Courser"""
	# Only you can target this with spells and Hero Powers.
	tags = {
		enums.CANT_BE_TARGETED_BY_OP_ABILITIES: True,
		enums.CANT_BE_TARGETED_BY_OP_HERO_POWERS: True,
	}


class LOOT_389:
	"""Rummaging Kobold"""
	# <b>Battlecry:</b> Return one of your destroyed weapons to your hand.
	play = Give(CONTROLLER, Copy(RANDOM(FRIENDLY + KILLED + WEAPON)))


class LOOT_414:
	"""Grand Archivist"""
	# At the end of your turn, cast a spell from your deck <i>(targets chosen
	# randomly)</i>.
	events = OWN_TURN_END.on(CastSpell(RANDOM(FRIENDLY_DECK + SPELL)))


class LOOT_529:
	"""Void Ripper"""
	# <b>Battlecry:</b> Swap the Attack and Health of all_other_minions.
	play = Buff(ALL_MINIONS, "LOOT_529e")


LOOT_529e = AttackHealthSwapBuff()


class LOOT_539:
	"""Spiteful Summoner"""
	# [x]<b>Battlecry:</b> Reveal a spell from your deck. Summon a random minion with the
	# same Cost.
	play = Reveal(RANDOM(FRIENDLY_DECK + SPELL)).then(
		Summon(CONTROLLER, RandomMinion(cost=COST(Reveal.TARGET)))
	)


class LOOT_540:
	"""Dragonhatcher"""
	# At the end of your turn, <b>Recruit</b> a Dragon.
	events = OWN_TURN_END.on(Recruit(DRAGON))
