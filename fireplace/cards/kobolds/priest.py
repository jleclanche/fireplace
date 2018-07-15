from ..utils import *

class LOOT_008:
	"""
	Psychic Scream - (Spell)
	Shuffle all minions into your opponent's deck.
	https://hearthstone.gamepedia.com/Psychic_Scream
	"""
	play = Shuffle(OPPONENT, ALL_MINIONS)


class LOOT_187:
	"""
	Twilight's Call - (Spell)
	Summon 1/1 copies of 2 friendly Deathrattle minions that died this game.
	https://hearthstone.gamepedia.com/Twilight%27s_Call
	"""
	play = Summon(CONTROLLER, Copy(RANDOM(FRIENDLY + KILLED + MINION + DEATHRATTLE))).then(
		Buff(Summon.CARD, "LOOT_187e")
	) * 2

class LOOT_187e:
	atk = SET(1)
	max_health = SET(1)


class LOOT_209:
	"""
	Dragon Soul - (Weapon)
	After you cast 3 spells in a turn, summon a 5/5 Dragon.
	https://hearthstone.gamepedia.com/Dragon_Soul
	"""
	event = [
		Play(CONTROLLER, SPELL).then(UpdateSpellStone(1, 3)),
		OWN_TURN_END.on(Refresh(SELF, {"quest_progress": 0}))
	]
	reward = Summon(CONTROLLER, "LOOT_209t")


class LOOT_278:
	"""
	Unidentified Elixir - (Spell)
	Give a minion +2/+2. Gains a bonus effect in_your hand.
	https://hearthstone.gamepedia.com/Unidentified_Elixir
	"""
	play = Buff(TARGET, "LOOT_278e")
	draw = Morph(SELF, RandomID("LOOT_278t1","LOOT_278t2","LOOT_278t3","LOOT_278t4"))

LOOT_278e = buff(+2, +2)


class LOOT_278t1:
	"""
	Elixir of Life - (Spell)
	Give a minion +2/+2 and Lifesteal.
	https://hearthstone.gamepedia.com/Elixir_of_Life
	"""
	play = Buff(TARGET, "LOOT_278t1e")

LOOT_278t1e = buff(+2, +2, lifesteal = True)


class LOOT_278t2:
	"""
	Elixir of Purity - (Spell)
	Give a minion +2/+2 and Divine Shield.
	https://hearthstone.gamepedia.com/Elixir_of_Purity
	"""
	play = Buff(TARGET, "LOOT_278t2e"), GiveDivineShield(TARGET)

LOOT_278t2e = buff(+2, +2)


class LOOT_278t3:
	"""
	Elixir of Shadows - (Spell)
	Give a minion +2/+2. Summon a 1/1 copy of_it.
	https://hearthstone.gamepedia.com/Elixir_of_Shadows
	"""
	play = Buff(TARGET, "LOOT_278t3e"), Summon(CONTROLLER, ExactCopy(TARGET)).then(Buff(Summon.CARD, "LOOT_278t3e2"))

LOOT_278t3e = buff(+2, +2)

class LOOT_278t3e2:
	atk = SET(1)
	max_health = SET(1)


class LOOT_278t4:
	"""
	Elixir of Hope - (Spell)
	Give a minion +2/+2 and "Deathrattle: Return this minion to your hand."
	https://hearthstone.gamepedia.com/Elixir_of_Hope
	"""
	play = Buff(TARGET, "LOOT_278t4e")

class LOOT_278t4e:
	deathrattle = Bounce(OWNER)
	tag = {
		GameTag.ATK: +2,
		GameTag.HEALTH: +2,
		GameTag.DEATHRATTLE: True
	}


class LOOT_353:
	"""
	Psionic Probe - (Spell)
	Copy a spell in your opponent's deck and add it to your hand.
	https://hearthstone.gamepedia.com/Psionic_Probe
	"""
	play = Give(CONTROLLER, Copy(RANDOM(ENEMY_DECK)))


class LOOT_410:
	"""
	Duskbreaker - (Minion)
	Battlecry: If you're holding a Dragon, deal 3 damage to all other minions.
	https://hearthstone.gamepedia.com/Duskbreaker
	"""
	powered_up = HOLDING_DRAGON
	play = powered_up & Hit(ALL_MINIONS - SELF, 3)


class LOOT_507:
	"""
	Lesser Diamond Spellstone - (Spell)
	Resurrect 2 different friendly minions. @
	https://hearthstone.gamepedia.com/Lesser_Diamond_Spellstone
	"""
	play = Summon(CONTROLLER, Copy(RANDOM(FRIENDLY + KILLED + MINION + DEATHRATTLE) * 2))
	reward = Morph(SELF, "LOOT_507t")
	class Hand:
		events = Play(CONTROLLER, SPELL).on(UpdateSpellStone(1, 4))


class LOOT_507t:
	"""
	Diamond Spellstone - (Spell)
	Resurrect 3 different friendly minions. @
	https://hearthstone.gamepedia.com/Diamond_Spellstone
	"""
	play = Summon(CONTROLLER, Copy(RANDOM(FRIENDLY + KILLED + MINION + DEATHRATTLE) * 3))
	reward = Morph(SELF, "LOOT_507t2")
	class Hand:
		events = Play(CONTROLLER, SPELL).on(UpdateSpellStone(1, 4))


class LOOT_507t2:
	"""
	Greater Diamond Spellstone - (Spell)
	Resurrect 4 different friendly minions.
	https://hearthstone.gamepedia.com/Greater_Diamond_Spellstone
	"""
	play = Summon(CONTROLLER, Copy(RANDOM(FRIENDLY + KILLED + MINION + DEATHRATTLE) * 4))


class LOOT_528:
	"""
	Twilight Acolyte - (Minion)
	Battlecry: If you're holding a Dragon, swap this minion's Attack with another minion's.
	https://hearthstone.gamepedia.com/Twilight_Acolyte
	"""
	powered_up = HOLDING_DRAGON
	play = powered_up & SwapAtk(SELF, TARGET, "LOOT_528e")

class LOOT_528e:
	pass


class LOOT_534:
	"""
	Gilded Gargoyle - (Minion)
	Deathrattle: Add a Coin to your hand.
	https://hearthstone.gamepedia.com/Gilded_Gargoyle
	"""
	deathrattle = Give(CONTROLLER, "GAME_005e")


class LOOT_538:
	"""
	Temporus - (Minion)
	Battlecry: Your opponent takes two turns. Then you take two turns.
	https://hearthstone.gamepedia.com/Temporus
	"""
	play = Buff(OPPONENT, "LOOT_538e")


class LOOT_538e:
	"""
	Time Spiraling - (Enchantment)
	Take an extra turn.
	https://hearthstone.gamepedia.com/Time_Spiraling
	"""
	tag = {
		GameTag.EXTRA_TURNS_TAKEN_THIS_GAME: True
	}
	events = OWN_TURN_END.on(Destroy(SELF), Buff(OPPONENT, "LOOT_538e2"))


class LOOT_538e2:
	"""
	Revenge - (Enchantment)
	Take an extra turn.
	https://hearthstone.gamepedia.com/Revenge
	"""
	tag = {
		GameTag.EXTRA_TURNS_TAKEN_THIS_GAME: True
	}
	events = OWN_TURN_END.on(Destroy(SELF))
