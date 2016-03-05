"""
Battle of the Builds
Deal Your Fate
"""

from .banana_brawl import RandomBanana
from ..utils import *


RandomFate = RandomID(
	"TB_PickYourFate_2", "TB_PickYourFate_5", "TB_PickYourFate_6",
	"TB_PickYourFate_7", "TB_PickYourFate_8rand", "TB_PickYourFate_12"
)

RandomDireFate = RandomID(
	"TB_PickYourFate_1", "TB_PickYourFate_3", "TB_PickYourFate_4",
	"TB_PickYourFate_6_2nd", "TB_PickYourFate_7_2nd", "TB_PickYourFate_11rand"
)


# Pick Your Fate Random
class TB_PickYourFateRandom:
	events = OWN_TURN_BEGIN.on(
		GenericChoice(CONTROLLER, RandomFate * 4), Destroy(SELF)
	)


# Pick Your Fate Randon 2nd
class TB_PickYourFate_2nd:
	events = OWN_TURN_BEGIN.on((CURRENT_HEALTH(FRIENDLY_HERO) <= 20) & (
		GenericChoice(CONTROLLER, RandomDireFate * 4), Destroy(SELF)
	))


# Fate: Bananas
class TB_PickYourFate_2:
	play = Buff(ALL_PLAYERS, "TB_PickYourFate_2_Ench")

class TB_PickYourFate_2_Ench:
	events = Summon(CONTROLLER, MINION).on(Buff(Summon.CARD, "TB_PickYourFate_2_EnchMinion"))

class TB_PickYourFate_2_EnchMinion:
	deathrattle = Give(CONTROLLER, RandomBanana)
	tags = {GameTag.DEATHRATTLE: True}


# Fate: Spells
class TB_PickYourFate_5:
	play = Buff(ALL_PLAYERS, "TB_PickYourFate_5_Ench")

class TB_PickYourFate_5_Ench:
	update = Refresh(FRIENDLY_HAND + SPELL, {GameTag.COST: -1})


# Fate: Portals
class TB_PickYourFate_6:
	play = Shuffle(ALL_PLAYERS, "GVG_003") * 10


# Fate: Coin
class TB_PickYourFate_7:
	play = (
		Buff(ALL_PLAYERS, "TB_PickYourFate_7Ench"),
		Buff(ALL_MINIONS, "TB_PickYourFate_7_EnchMinion"),
	)

class TB_PickYourFate_7Ench:
	events = Summon(CONTROLLER, MINION).on(Buff(Summon.CARD, "TB_PickYourFate_7_EnchMinion"))

class TB_PickYourFate_7_EnchMinion:
	deathrattle = Give(CONTROLLER, "TB_011")
	tags = {GameTag.DEATHRATTLE: True}


# Fate: Armor
class TB_PickYourFate_8rand:
	play = Buff(ALL_PLAYERS, "TB_PickYourFate_8_EnchRand")

class TB_PickYourFate_8_EnchRand:
	events = OWN_TURN_BEGIN.on(GainArmor(FRIENDLY_HERO, 2))


# Fate: Confusion
class TB_PickYourFate_12:
	play = Buff(ALL_PLAYERS, "TB_PickYourFate_12_Ench")

class TB_PickYourFate_12_Ench:
	events = OWN_TURN_END.on(Buff(ALL_MINIONS, "TB_PickYourFate_Confused"))

TB_PickYourFate_Confused = AttackHealthSwapBuff()


# Dire Fate: Taunt and Charge
class TB_PickYourFate_1:
	play = (
		Buff(ALL_PLAYERS, "TB_PickYourFate_1_Ench"),
		Buff(ALL_MINIONS, "TB_AllMinionsTauntCharge")
	)

class TB_PickYourFate_1_Ench:
	events = Play(CONTROLLER, MINION).on(Buff(Play.CARD, "TB_AllMinionsTauntCharge"))

TB_AllMinionsTauntCharge = buff(taunt=True, charge=True)


# Dire Fate: Windfury
class TB_PickYourFate_3:
	play = (
		Buff(ALL_PLAYERS, "TB_PickYourFate_3_Ench"),
		Buff(ALL_MINIONS - WINDFURY, "TB_PickYourFate_Windfury")
	)


class TB_PickYourFate_3_Ench:
	events = Play(CONTROLLER, MINION).on(Buff(Play.CARD, "TB_PickYourFate_Windfury"))


class TB_PickYourFate_Windfury:
	windfury = SET(1)


# Dire Fate: Card
class TB_PickYourFate_4:
	play = (
		Buff(ALL_PLAYERS, "TB_PickYourFate_4_Ench"),
		Buff(ALL_MINIONS, "TB_PickYourFate_4_EnchMinion")
	)

class TB_PickYourFate_4_Ench:
	events = Summon(CONTROLLER, MINION).on(Buff(Summon.CARD, "TB_PickYourFate_4_EnchMinion"))

class TB_PickYourFate_4_EnchMinion:
	deathrattle = Draw(CONTROLLER)
	tags = {GameTag.DEATHRATTLE: True}


# Dire Fate: Unstable Portals
class TB_PickYourFate_6_2nd:
	play = Give(ALL_PLAYERS, "GVG_003") * 3


# Dire Fate: Manaburst
class TB_PickYourFate_7_2nd:
	play = (
		Buff(ALL_PLAYERS, "TB_PickYourFate_7_Ench_2nd"),
		Buff(ALL_MINIONS, "TB_PickYourFate_7_EnchMiniom2nd")
	)

class TB_PickYourFate_7_Ench_2nd:
	events = Summon(CONTROLLER, MINION).on(Buff(Summon.CARD, "TB_PickYourFate_7_EnchMiniom2nd"))

class TB_PickYourFate_7_EnchMiniom2nd:
	deathrattle = Buff(RANDOM(FRIENDLY_HAND + (COST > 0)), "TB_PickYourFate_7_EnchMiniom2nde")

@custom_card
class TB_PickYourFate_7_EnchMiniom2nde:
	tags = {
		GameTag.CARDNAME: "Dire Fate: Manaburst Minion Deathrattle Trigger Buff",
		GameTag.CARDTYPE: CardType.ENCHANTMENT,
	}
	cost = SET(0)


# Dire Fate: Murlocs
class TB_PickYourFate_11rand:
	play = Morph(ALL_MINIONS, "LOEA10_3")


# Murlocs (Unused)
class TB_PickYourFate_11:
	play = Buff(ALL_PLAYERS, "TB_PickYourFate_11_Ench")

class TB_PickYourFate_11_Ench:
	events = OWN_TURN_END.on(Summon(CONTROLLER, "LOEA10_3"))


##
# Battle of the Builds

# Spell Bonus
class TB_PickYourFate_8:
	play = Buff(CONTROLLER, "TB_PickYourFate_8_Ench")

class TB_PickYourFate_8_Ench:
	events = OWN_SPELL_PLAY.on(GainArmor(FRIENDLY_HERO, 3))


# Deathrattle Bonus
class TB_PickYourFate_9:
	play = Buff(CONTROLLER, "TB_PickYourFate_9_Ench")

class TB_PickYourFate_9_Ench:
	update = Refresh(FRIENDLY_MINIONS + DEATHRATTLE, "TB_PickYourFate_9_EnchMinion")

TB_PickYourFate_9_EnchMinion = buff(+1, +1)


# Battlecry Bonus
class TB_PickYourFate_10:
	play = Buff(CONTROLLER, "TB_PickYourFate_10_Ench")

class TB_PickYourFate_10_Ench:
	update = Refresh(FRIENDLY_MINIONS + BATTLECRY, "TB_PickYourFate_10_EnchMinion")

TB_PickYourFate_10_EnchMinion = buff(+1, +1)


# Murloc Bonus
class TB_PickYourFate_11b:
	play = Buff(CONTROLLER, "TB_PickYourFate_11_Ench")

class TB_PickYourFate_11_Ench:
	events = OWN_TURN_END.on(Summon(CONTROLLER, "LOEA10_3"))
