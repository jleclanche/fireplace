from ..utils import *

class LOOT_047:
	"""
	Barkskin - (Spell)
	Give a minion +3 Health. Gain 3 Armor.
	https://hearthstone.gamepedia.com/Barkskin
	"""
	play = Buff(TARGET, "LOOT_047e"), GainArmor(FRIENDLY_HERO, 3)

LOOT_047e = buff(health=3)

class LOOT_048:
	"""
	Ironwood Golem - (Minion)
	Taunt Can only attack if you have 3 or more Armor.
	https://hearthstone.gamepedia.com/Ironwood_Golem
	"""
	update = (ARMOR(FRIENDLY_HERO) < 3) & Refresh(SELF, {GameTag.CANT_ATTACK: True})


class LOOT_051:
	"""
	Lesser Jasper Spellstone - (Spell)
	Deal $2 damage to a minion. @
	https://hearthstone.gamepedia.com/Lesser_Jasper_Spellstone
	"""
	play = Hit(TARGET, 2)
	reward = Morph(SELF, "LOOT_051t1")
	class Hand:
		events = GainArmor(FRIENDLY_HERO).on(UpdateSpellStone(GainArmor.AMOUNT, 3))


class LOOT_051t1:
	"""
	Jasper Spellstone - (Spell)
	Deal $4 damage to a minion. @
	https://hearthstone.gamepedia.com/Jasper_Spellstone
	"""
	play = Hit(TARGET, 4)
	reward = Morph(SELF, "LOOT_051t2")
	class Hand:
		events = GainArmor(FRIENDLY_HERO).on(UpdateSpellStone(GainArmor.AMOUNT, 3, "LOOT_051t2"))

class LOOT_051t2:
	"""
	Greater Jasper Spellstone - (Spell)
	Deal $6 damage to a minion.
	https://hearthstone.gamepedia.com/Greater_Jasper_Spellstone
	"""
	play = Hit(TARGET, 6)


class LOOT_054:
	"""
	Branching Paths - (Spell)
	Choose Twice - Draw a card; Give your minions  +1 Attack; Gain 6 Armor.
	https://hearthstone.gamepedia.com/Branching_Paths
	"""
	play = GenericChoice(CONTROLLER, ["LOOT_054d","LOOT_054b","LOOT_054c"]), GenericChoice(CONTROLLER, ["LOOT_054d","LOOT_054b","LOOT_054c"])


class LOOT_054b:
	"""
	Explore the Darkness - (Spell)
	Give your minions +1 Attack.
	https://hearthstone.gamepedia.com/Explore_the_Darkness
	"""
	play = Buff(FRIENDLY_MINIONS, "LOOT_054be")

LOOT_054be = buff(atk=1)

class LOOT_054c:
	"""
	Loot the Chest - (Spell)
	Gain 6 Armor.
	https://hearthstone.gamepedia.com/Loot_the_Chest
	"""
	play = GainArmor(FRIENDLY_HERO, 6)


class LOOT_054d:
	"""
	Eat the Mushroom - (Spell)
	Draw a card.
	https://hearthstone.gamepedia.com/Eat_the_Mushroom
	"""
	play = Draw(CONTROLLER)


class LOOT_056:
	"""
	Astral Tiger - (Minion)
	Deathrattle: Shuffle a  copy of this minion into_your_deck.
	https://hearthstone.gamepedia.com/Astral_Tiger
	"""
	deathrattle = Shuffle(CONTROLLER, Copy(SELF))


class LOOT_309:
	"""
	Oaken Summons - (Spell)
	Gain 6 Armor. Recruit a minion that costs (4) or less.
	https://hearthstone.gamepedia.com/Oaken_Summons
	"""
	play = GainArmor(CONTROLLER, 6), Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION + (COST <= 4)))


class LOOT_314:
	"""
	Grizzled Guardian - (Minion)
	Taunt Deathrattle: Recruit 2_minions that cost (4)_or_less.
	https://hearthstone.gamepedia.com/Grizzled_Guardian
	"""
	deathrattle = Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION + (COST <= 4))) * 2


class LOOT_329:
	"""
	Ixlid, Fungal Lord - (Minion)
	After you play a minion, summon a copy of it.
	https://hearthstone.gamepedia.com/Ixlid%2C_Fungal_Lord
	"""
	events = Summon(CONTROLLER).on(Summon(CONTROLLER, ExactCopy(Summon.CARD)))


class LOOT_351:
	"""
	Greedy Sprite - (Minion)
	Deathrattle: Gain an empty Mana Crystal.
	https://hearthstone.gamepedia.com/Greedy_Sprite
	"""
	deathrattle = GainEmptyMana(CONTROLLER, 1)


class LOOT_392:
	"""
	Twig of the World Tree - (Weapon)
	Deathrattle: Gain 10 Mana Crystals.
	https://hearthstone.gamepedia.com/Twig_of_the_World_Tree
	"""
	deathrattle = GainMana(CONTROLLER, 10)