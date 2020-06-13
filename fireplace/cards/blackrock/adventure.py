from ..utils import *


##
# Hero Powers

class BRMA01_2:
	"""Pile On!"""
	requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
	activate = (
		Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION)),
		Summon(OPPONENT, RANDOM(ENEMY_DECK + MINION))
	)


class BRMA01_2H:
	"""Pile On! (Heroic)"""
	requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
	activate = (
		Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION) * 2),
		Summon(OPPONENT, RANDOM(ENEMY_DECK + MINION))
	)


class BRMA01_3:
	"""Dark Iron Bouncer"""
	tags = {
		enums.ALWAYS_WINS_BRAWLS: True,
	}


class BRMA02_2:
	"""Jeering Crowd"""
	requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
	activate = Summon(CONTROLLER, "BRMA02_2t")


class BRMA02_2H:
	"""Jeering Crowd (Heroic)"""
	requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
	activate = Summon(CONTROLLER, "BRMA02_2t")


class BRMA03_2:
	"""Power of the Firelord"""
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
	activate = Hit(TARGET, 2)


class BRMA04_2:
	"""Magma Pulse"""
	activate = Hit(ALL_MINIONS, 1)


class BRMA05_2:
	"""Ignite Mana"""
	activate = (
		(MANA(OPPONENT) <= USED_MANA(OPPONENT)) &
		Hit(ENEMY_HERO, 5)
	)


class BRMA05_2H:
	"""Ignite Mana (Heroic)"""
	activate = (
		(MANA(OPPONENT) <= USED_MANA(OPPONENT)) &
		Hit(ENEMY_HERO, 10)
	)


class BRMA06_2:
	"""The Majordomo"""
	requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
	activate = Summon(CONTROLLER, "BRMA06_4")


class BRMA06_2H:
	"""The Majordomo (Heroic)"""
	requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
	activate = Summon(CONTROLLER, "BRMA06_4H")


class BRMA07_2:
	"""ME SMASH"""
	requirements = {PlayReq.REQ_MINIMUM_ENEMY_MINIONS: 1}
	activate = Destroy(RANDOM(ENEMY_MINIONS + DAMAGED))


class BRMA07_2H:
	"""ME SMASH (Heroic)"""
	activate = Destroy(RANDOM_ENEMY_MINION)


class BRMA08_2:
	"""Intense Gaze"""
	update = (
		Refresh(ALL_PLAYERS, {GameTag.MAXRESOURCES: SET(1)}),
		Refresh(IN_HAND, {GameTag.COST: SET(1)})
	)


class BRMA08_2H:
	"""Intense Gaze (Heroic)"""
	update = (
		Refresh(CONTROLLER, {GameTag.MAXRESOURCES: SET(2)}),
		Refresh(OPPONENT, {GameTag.MAXRESOURCES: SET(1)}),
		Refresh(IN_HAND, {GameTag.COST: SET(1)})
	)


class BRMA09_2:
	"""Open the Gates"""
	requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
	entourage = ["BRMA09_3", "BRMA09_4"]
	activate = Summon(CONTROLLER, "BRMA09_2t") * 3, Summon(CONTROLLER, RandomEntourage())


class BRMA09_2H:
	"""Open the Gates (Heroic)"""
	entourage = ["BRMA09_3H", "BRMA09_4H"]
	activate = Summon(CONTROLLER, "BRMA09_2Ht") * 3, Summon(CONTROLLER, RandomEntourage())


class BRMA09_3:
	"""Old Horde"""
	requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
	entourage = ["BRMA09_2", "BRMA09_4", "BRMA09_5"]
	activate = Summon(CONTROLLER, "BRMA09_3t") * 2, Summon(CONTROLLER, RandomEntourage())


class BRMA09_3H:
	"""Old Horde (Heroic)"""
	entourage = ["BRMA09_2H", "BRMA09_4H", "BRMA09_5H"]
	activate = Summon(CONTROLLER, "BRMA09_3Ht") * 2, Summon(CONTROLLER, RandomEntourage())


class BRMA09_4:
	"""Blackwing"""
	requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
	entourage = ["BRMA09_2", "BRMA09_3", "BRMA09_5"]
	activate = Summon(CONTROLLER, "BRMA09_4t"), Summon(CONTROLLER, RandomEntourage())


class BRMA09_4H:
	"""Blackwing (Heroic)"""
	entourage = ["BRMA09_2H", "BRMA09_3H", "BRMA09_5H"]
	activate = Summon(CONTROLLER, "BRMA09_4Ht"), Summon(CONTROLLER, RandomEntourage())


class BRMA09_5:
	"""Dismount"""
	requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
	entourage = ["BRMA09_2", "BRMA09_3", "BRMA09_4"]
	activate = Summon(CONTROLLER, "BRMA09_5t"), Summon(CONTROLLER, RandomEntourage())


class BRMA09_5H:
	"""Dismount (Heroic)"""
	entourage = ["BRMA09_2H", "BRMA09_3H", "BRMA09_4H"]
	activate = Summon(CONTROLLER, "BRMA09_5Ht"), Summon(CONTROLLER, RandomEntourage())


class BRMA10_3:
	"""The Rookery"""
	activate = Buff(ALL_MINIONS + ID("BRMA10_4"), "BRMA10_3e"), Summon(CONTROLLER, "BRMA10_4")


class BRMA10_3H:
	"""The Rookery"""
	activate = Buff(ALL_MINIONS + ID("BRMA10_4"), "BRMA10_3e"), Summon(CONTROLLER, "BRMA10_4")


BRMA10_3e = buff(health=1)


class BRMA11_2:
	"""Essence of the Red"""
	activate = Draw(ALL_PLAYERS) * 2


class BRMA11_2H:
	"""Essence of the Red (Heroic)"""
	activate = Draw(ALL_PLAYERS) * 3, GainMana(CONTROLLER, 1)


class BRMA12_2:
	"""Brood Affliction"""
	entourage = ["BRMA12_6", "BRMA12_5", "BRMA12_7", "BRMA12_4", "BRMA12_3"]
	activate = Give(OPPONENT, RandomEntourage())


class BRMA12_2H:
	"""Brood Affliction (Heroic)"""
	entourage = ["BRMA12_3H", "BRMA12_4H", "BRMA12_5H", "BRMA12_6H", "BRMA12_7H"]
	activate = Give(OPPONENT, RandomEntourage())


class BRMA12_10:
	"""Mutation (Unused)"""
	activate = Discard(RANDOM(FRIENDLY_HAND))


class BRMA13_2:
	"""True Form"""
	activate = (
		Summon(CONTROLLER, "BRMA13_3"),
		Draw(CONTROLLER) * 2,
		GainArmor(CONTROLLER, 30)
	)


class BRMA13_2H:
	"""True Form (Heroic)"""
	activate = (
		Summon(CONTROLLER, "BRMA13_3H"),
		Draw(CONTROLLER) * 2,
		GainArmor(CONTROLLER, 30)
	)


class BRMA13_4:
	"""Wild Magic"""
	activate = Give(CONTROLLER, RandomSpell(card_class=ENEMY_CLASS))


class BRMA13_4H:
	"""Wild Magic (Heroic)"""
	activate = Give(CONTROLLER, RandomSpell(card_class=ENEMY_CLASS))


class BRMA14_2:
	"""Activate Arcanotron"""
	activate = Summon(CONTROLLER, "BRMA14_3"), Summon(CONTROLLER, "BRMA14_4")


class BRMA14_2H:
	"""Activate Arcanotron (Heroic)"""
	activate = Summon(CONTROLLER, "BRMA14_3"), Summon(CONTROLLER, "BRMA14_4H")


class BRMA14_4:
	"""Activate Toxitron"""
	activate = Summon(CONTROLLER, "BRMA14_5"), Summon(CONTROLLER, "BRMA14_6")


class BRMA14_4H:
	"""Activate Toxitron (Heroic)"""
	activate = Summon(CONTROLLER, "BRMA14_5H"), Summon(CONTROLLER, "BRMA14_6H")


class BRMA14_6:
	"""Activate Electron"""
	activate = Summon(CONTROLLER, "BRMA14_7"), Summon(CONTROLLER, "BRMA14_8")


class BRMA14_6H:
	"""Activate Electron (Heroic)"""
	activate = Summon(CONTROLLER, "BRMA14_7H"), Summon(CONTROLLER, "BRMA14_8H")


class BRMA14_8:
	"""Activate Magmatron"""
	activate = Summon(CONTROLLER, "BRMA14_9"), Summon(CONTROLLER, "BRMA14_10")


class BRMA14_8H:
	"""Activate Magmatron (Heroic)"""
	activate = Summon(CONTROLLER, "BRMA14_9H"), Summon(CONTROLLER, "BRMA14_10H")


class BRMA14_10:
	"""Activate!"""
	entourage = ["BRMA14_3", "BRMA14_5", "BRMA14_7", "BRMA14_9"]
	activate = Summon(CONTROLLER, RandomEntourage())


class BRMA14_10H:
	"""Activate! (Heroic)"""
	entourage = ["BRMA14_3", "BRMA14_5H", "BRMA14_7H", "BRMA14_9H"]
	activate = Summon(CONTROLLER, RandomEntourage())


class BRMA15_2:
	"""The Alchemist"""
	events = Summon(ALL_PLAYERS, MINION).on(Buff(Summon.CARD, "BRMA15_2e"))


class BRMA15_2e(AttackHealthSwapBuff()):
	tags = {
		GameTag.CARDNAME: "The Alchemist Attack/Health Swap Buff"""
	}


class BRMA15_2H:
	"""The Alchemist (Heroic)"""
	events = (
		Summon(ALL_PLAYERS, MINION).on(Buff(Summon.CARD, "BRMA15_2e")),
		Summon(CONTROLLER, MINION).on(Buff(Summon.CARD, "BRMA15_2He"))
	)


# Potion of Might (The Alchemist)
BRMA15_2He = buff(+2, +2)


class BRMA16_2:
	"""Echolocate"""
	activate = Summon(CONTROLLER, "BRMA16_5")


class BRMA16_2H:
	"""Echolocate (Heroic)"""
	activate = Summon(CONTROLLER, "BRMA16_5")


class BRMA17_5:
	"""Bone Minions"""
	requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
	activate = Summon(CONTROLLER, "BRMA17_6") * 2


class BRMA17_5H:
	"""Bone Minions (Heroic)"""
	requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
	activate = Summon(CONTROLLER, "BRMA17_6H") * 2


class BRMA17_8:
	"""Nefarian Strikes!"""
	activate = Hit(ENEMY_HERO, 1) * RandomNumber(0, 1, 2, 3, 4, 20)


class BRMA17_8H:
	"""Nefarian Strikes! (Heroic)"""
	activate = Hit(ENEMY_HERO, 1) * RandomNumber(0, 1, 2, 3, 4, 20)


##
# Minions

class BRMA03_3:
	"""Moira Bronzebeard"""
	update = Refresh(ALL_HERO_POWERS + ID("BRMA03_2"), {GameTag.CANT_PLAY: True})


class BRMA03_3H:
	"""Moira Bronzebeard (Heroic)"""
	update = Refresh(ALL_HERO_POWERS + ID("BRMA03_2"), {GameTag.CANT_PLAY: True})


class BRMA10_4:
	"""Corrupted Egg"""
	update = (CURRENT_HEALTH(SELF) >= 4) & (Destroy(SELF), Summon(CONTROLLER, "BRMA10_5"))


class BRMA10_4H:
	"""Corrupted Egg (Heroic)"""
	update = (CURRENT_HEALTH(SELF) >= 5) & (Destroy(SELF), Summon(CONTROLLER, "BRMA10_5H"))


class BRMA04_3:
	"""Firesworn"""
	deathrattle = Hit(ENEMY_HERO, Count(ID("BRMA04_3") + KILLED_THIS_TURN))


class BRMA04_3H:
	"""Firesworn (Heroic)"""
	deathrattle = Hit(ENEMY_HERO, Count(ID("BRMA04_3H") + KILLED_THIS_TURN))


class BRMA12_8t:
	"""Chromatic Dragonkin"""
	events = Play(OPPONENT, SPELL).on(Buff(SELF, "BRMA12_8te"))


BRMA12_8te = buff(+2, +2)


class BRMA13_5:
	"""Son of the Flame"""
	requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	play = Hit(TARGET, 6)


##
# Spells

class BRMA_01:
	"""Flameheart"""
	play = Draw(CONTROLLER) * 2, GainArmor(FRIENDLY_HERO, 4)


class BRMA01_4:
	"""Get 'em!"""
	play = Summon(CONTROLLER, "BRMA01_4t") * 4


class BRMA05_3:
	"""Living Bomb"""
	requirements = {
		PlayReq.REQ_ENEMY_TARGET: 0, PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Buff(TARGET, "BRMA05_3e")


class BRMA05_3e:
	events = OWN_TURN_BEGIN.on(Hit(ENEMY_CHARACTERS, 5))


class BRMA05_3H:
	"""Living Bomb (Heroic)"""
	requirements = {
		PlayReq.REQ_ENEMY_TARGET: 0, PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Buff(TARGET, "BRMA05_3He")


class BRMA05_3He:
	events = OWN_TURN_BEGIN.on(Hit(ENEMY_CHARACTERS, 10))


class BRMA07_3:
	"""TIME FOR SMASH"""
	play = Hit(RANDOM_ENEMY_MINION, 5), GainArmor(FRIENDLY_HERO, 5)


class BRMA08_3:
	"""Drakkisath's Command"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Destroy(TARGET), GainArmor(FRIENDLY_HERO, 10)


class BRMA09_6:
	"""The True Warchief"""
	requirements = {
		PlayReq.REQ_LEGENDARY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Destroy(TARGET)


class BRMA04_4:
	"""Rock Out"""
	play = Summon(CONTROLLER, "BRMA04_3") * 3


class BRMA04_4H:
	"""Rock Out (Heroic)"""
	play = Summon(CONTROLLER, "BRMA04_3H") * 3


class BRMA11_3:
	"""Burning Adrenaline"""
	play = Hit(ENEMY_HERO, 2)


class BRMA12_8:
	"""Chromatic Mutation (Unused)"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Morph(TARGET, "BRMA12_8t")


class BRMA14_11:
	"""Recharge"""
	play = FillMana(CONTROLLER, USED_MANA(CONTROLLER))


class BRMA13_8:
	"""DIE, INSECT!"""
	play = Hit(RANDOM_ENEMY_CHARACTER, 8)


class BRMA15_3:
	"""Release the Aberrations!"""
	requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
	play = Summon(CONTROLLER, "BRMA15_4") * 3


class BRMA14_3:
	"""Arcanotron"""
	update = Refresh(ALL_PLAYERS, {GameTag.SPELLPOWER: +2})


class BRMA14_5:
	"""Toxitron"""
	events = OWN_TURN_BEGIN.on(Hit(ALL_MINIONS - SELF, 1))


class BRMA14_5H:
	"""Toxitron (Heroic)"""
	events = OWN_TURN_BEGIN.on(Hit(ALL_MINIONS - SELF, 1))


class BRMA14_7:
	"""Electron"""
	update = Refresh(IN_HAND + SPELL, {GameTag.COST: -3})


class BRMA14_7H:
	"""Electron (Heroic)"""
	update = Refresh(IN_HAND + SPELL, {GameTag.COST: -3})


class BRMA14_9:
	"""Magmatron"""
	events = Play().on(Hit(ALL_HEROES + CONTROLLED_BY(Play.PLAYER)))


class BRMA14_9H:
	"""Magmatron"""
	events = Play().on(Hit(ALL_HEROES + CONTROLLED_BY(Play.PLAYER)))


class BRMA16_3:
	"""Sonic Breath"""
	requirements = {
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_TO_PLAY: 0,
		PlayReq.REQ_WEAPON_EQUIPPED: 0}
	play = Hit(TARGET, 3), Buff(FRIENDLY_WEAPON, "BRMA16_3e")


BRMA16_3e = buff(atk=3)


class BRMA16_4:
	"""Reverberating Gong"""
	requirements = {PlayReq.REQ_ENEMY_WEAPON_EQUIPPED: 0}
	play = Destroy(ENEMY_WEAPON)


class BRMA17_4:
	"""LAVA!"""
	play = Hit(ALL_MINIONS, 2)


##
# Weapons

class BRMA10_6:
	"""Razorgore's Claws (Unused)"""
	events = Death(MINION + ID("BRMA10_4")).on(Buff(SELF, "BRMA10_6e"))


BRMA10_6e = buff(atk=1)


class BRMA16_5:
	"""Dragonteeth"""
	events = Play(OPPONENT).on(Buff(SELF, "BRMA16_5e"))


BRMA16_5e = buff(atk=1)


##
# Brood Afflictions (Chromaggus)

class BRMA12_3:
	"""Brood Affliction: Red"""
	class Hand:
		events = OWN_TURN_BEGIN.on(Hit(FRIENDLY_HERO, 1))


class BRMA12_3H:
	"""Brood Affliction: Red (Heroic)"""
	class Hand:
		events = OWN_TURN_BEGIN.on(Hit(FRIENDLY_HERO, 3))


class BRMA12_4:
	"""Brood Affliction: Green"""
	class Hand:
		events = OWN_TURN_BEGIN.on(Heal(ENEMY_HERO, 2))


class BRMA12_4H:
	"""Brood Affliction: Green (Heroic)"""
	class Hand:
		events = OWN_TURN_BEGIN.on(Heal(ENEMY_HERO, 6))


class BRMA12_5:
	"""Brood Affliction: Blue"""
	class Hand:
		update = Refresh(ENEMY_HAND + SPELL, {GameTag.COST: -1})


class BRMA12_5H:
	"""Brood Affliction: Blue (Heroic)"""
	class Hand:
		update = Refresh(ENEMY_HAND + SPELL, {GameTag.COST: -3})


class BRMA12_6:
	"""Brood Affliction: Black"""
	class Hand:
		events = Draw(OPPONENT).on(Give(OPPONENT, Copy(Draw.CARD)))


class BRMA12_6H:
	"""Brood Affliction: Black (Heroic)"""
	class Hand:
		events = Draw(OPPONENT).on(Give(OPPONENT, Copy(Draw.CARD)))


class BRMA12_7:
	"""Brood Affliction: Bronze"""
	class Hand:
		update = Refresh(ENEMY_HAND + MINION, {GameTag.COST: -1})


class BRMA12_7H:
	"""Brood Affliction: Bronze (Heroic)"""
	class Hand:
		update = Refresh(ENEMY_HAND + MINION, {GameTag.COST: -3})
