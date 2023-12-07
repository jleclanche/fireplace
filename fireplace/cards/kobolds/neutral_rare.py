from ..utils import *


##
# Minions

class LOOT_111:
	"""Scorp-o-matic"""
	# <b>Battlecry:</b> Destroy a minion with 1 or less Attack.
	play = Destroy(TARGET)


class LOOT_118:
	"""Ebon Dragonsmith"""
	# <b>Battlecry:</b> Reduce the Cost of a random weapon in your hand by (2).
	play = Buff(RANDOM(FRIENDLY_HAND + MINION), "LOOT_118e")


class LOOT_118e:
	events = REMOVED_IN_PLAY
	tags = {GameTag.COST: -2}


class LOOT_124:
	"""Lone Champion"""
	# <b>Battlecry:</b> If you control no other minions, gain <b>Taunt</b> and <b>Divine
	# Shield</b>.
	play = Find(FRIENDLY_MINIONS - SELF) | Buff(SELF, "LOOT_124e"), GiveDivineShield(SELF)


LOOT_124e = buff(taunt=True)


class LOOT_150:
	"""Furbolg Mossbinder"""
	# <b>Battlecry:</b> Transform a friendly minion into a 6/6_Elemental.
	play = Morph(TARGET, "LOOT_150t1")


class LOOT_154:
	"""Gravelsnout Knight"""
	# <b>Battlecry:</b> Summon a random 1-Cost minion for_your opponent.
	play = Summon(OPPONENT, RandomMinion(cost=1))


class LOOT_218:
	"""Feral Gibberer"""
	# After this minion attacks a hero, add a copy of it to_your hand.
	events = Attack(SELF, ENEMY_HERO).after(Give(CONTROLLER, Copy(SELF)))


class LOOT_382:
	"""Kobold Monk"""
	# Your hero can't be targeted by spells or Hero_Powers.
	update = Refresh(FRIENDLY_HERO, {
		GameTag.CANT_BE_TARGETED_BY_ABILITIES: True,
		GameTag.CANT_BE_TARGETED_BY_HERO_POWERS: True,
	})


class LOOT_383:
	"""Hungry Ettin"""
	# <b>Taunt</b> <b>Battlecry:</b> Summon a random 2-Cost minion for your opponent.
	play = Summon(OPPONENT, RandomMinion(cost=2))


class LOOT_394:
	"""Shrieking Shroom"""
	# At the end of your turn, summon a random 1-Cost minion.
	events = OWN_TURN_END.on(Summon(CONTROLLER, RandomMinion(cost=1)))
