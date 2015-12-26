from ..utils import *


##
# Hero Powers

# Pile On!
class BRMA01_2:
	activate = (
		Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION)),
		Summon(OPPONENT, RANDOM(ENEMY_DECK + MINION))
	)

class BRMA01_2H:
	activate = (
		Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION) * 2),
		Summon(OPPONENT, RANDOM(ENEMY_DECK + MINION))
	)


# Dark Iron Bouncer
class BRMA01_3:
	tags = {
		enums.ALWAYS_WINS_BRAWLS: True,
	}


# Jeering Crowd
class BRMA02_2:
	activate = Summon(CONTROLLER, "BRMA02_2t")

class BRMA02_2H:
	activate = Summon(CONTROLLER, "BRMA02_2t")


# Power of the Firelord
class BRMA03_2:
	activate = Hit(TARGET, 2)


# Magma Pulse
class BRMA04_2:
	activate = Hit(ALL_MINIONS, 1)


# Ignite Mana
class BRMA05_2:
	activate = (
		(MANA(OPPONENT) <= USED_MANA(OPPONENT)) &
		Hit(ENEMY_HERO, 5)
	)

class BRMA05_2H:
	activate = (
		(MANA(OPPONENT) <= USED_MANA(OPPONENT)) &
		Hit(ENEMY_HERO, 10)
	)


# The Majordomo
class BRMA06_2:
	activate = Summon(CONTROLLER, "BRMA06_4")

class BRMA06_2H:
	activate = Summon(CONTROLLER, "BRMA06_4H")


# ME SMASH
class BRMA07_2:
	activate = Destroy(RANDOM(ENEMY_MINIONS + DAMAGED))

class BRMA07_2H:
	activate = Destroy(RANDOM_ENEMY_MINION)


# Intense Gaze
class BRMA08_2:
	update = (
		Refresh(ALL_PLAYERS, {GameTag.MAXRESOURCES: SET(1)}),
		Refresh(IN_HAND, {GameTag.COST: SET(1)})
	)

class BRMA08_2H:
	update = (
		Refresh(CONTROLLER, {GameTag.MAXRESOURCES: SET(2)}),
		Refresh(OPPONENT, {GameTag.MAXRESOURCES: SET(1)}),
		Refresh(IN_HAND, {GameTag.COST: SET(1)})
	)


# Open the Gates
class BRMA09_2:
	activate = Summon(CONTROLLER, "BRMA09_2t") * 3, Summon(CONTROLLER, RandomEntourage())

class BRMA09_2H:
	activate = Summon(CONTROLLER, "BRMA09_2Ht") * 3, Summon(CONTROLLER, RandomEntourage())


# Old Horde
class BRMA09_3:
	activate = Summon(CONTROLLER, "BRMA09_3t") * 2, Summon(CONTROLLER, RandomEntourage())

class BRMA09_3H:
	activate = Summon(CONTROLLER, "BRMA09_3Ht") * 2, Summon(CONTROLLER, RandomEntourage())


# Blackwing
class BRMA09_4:
	activate = Summon(CONTROLLER, "BRMA09_4t"), Summon(CONTROLLER, RandomEntourage())

class BRMA09_4H:
	activate = Summon(CONTROLLER, "BRMA09_4Ht"), Summon(CONTROLLER, RandomEntourage())


# Dismount
class BRMA09_5:
	activate = Summon(CONTROLLER, "BRMA09_5t"), Summon(CONTROLLER, RandomEntourage())

class BRMA09_5H:
	activate = Summon(CONTROLLER, "BRMA09_5Ht"), Summon(CONTROLLER, RandomEntourage())


# The Rookery
class BRMA10_3:
	activate = Buff(ALL_MINIONS + ID("BRMA10_4"), "BRMA10_3e"), Summon(CONTROLLER, "BRMA10_4")

# The Rookery
class BRMA10_3H:
	activate = Buff(ALL_MINIONS + ID("BRMA10_4"), "BRMA10_3e"), Summon(CONTROLLER, "BRMA10_4")

BRMA10_3e = buff(health=1)


# Essence of the Red
class BRMA11_2:
	activate = Draw(ALL_PLAYERS) * 2

class BRMA11_2H:
	activate = Draw(ALL_PLAYERS) * 3, GainMana(CONTROLLER, 1)


# Brood Affliction
class BRMA12_2:
	activate = Give(OPPONENT, RandomEntourage())

class BRMA12_2H:
	activate = Give(OPPONENT, RandomEntourage())


# Mutation (Unused)
class BRMA12_10:
	activate = Discard(RANDOM(FRIENDLY_HAND))


# Wild Magic
class BRMA13_4:
	activate = Give(CONTROLLER, RandomSpell(card_class=ENEMY_CLASS))

class BRMA13_4H:
	activate = Give(CONTROLLER, RandomSpell(card_class=ENEMY_CLASS))


# Activate Arcanotron
class BRMA14_2:
	activate = Summon(CONTROLLER, "BRMA14_3"), Summon(CONTROLLER, "BRMA14_4")

class BRMA14_2H:
	activate = Summon(CONTROLLER, "BRMA14_3"), Summon(CONTROLLER, "BRMA14_4H")


# Activate Toxitron
class BRMA14_4:
	activate = Summon(CONTROLLER, "BRMA14_5"), Summon(CONTROLLER, "BRMA14_6")

class BRMA14_4H:
	activate = Summon(CONTROLLER, "BRMA14_5H"), Summon(CONTROLLER, "BRMA14_6H")


# Activate Electron
class BRMA14_6:
	activate = Summon(CONTROLLER, "BRMA14_7"), Summon(CONTROLLER, "BRMA14_8")

class BRMA14_6H:
	activate = Summon(CONTROLLER, "BRMA14_7H"), Summon(CONTROLLER, "BRMA14_8H")


# Activate Magmatron
class BRMA14_8:
	activate = Summon(CONTROLLER, "BRMA14_9"), Summon(CONTROLLER, "BRMA14_10")

class BRMA14_8H:
	activate = Summon(CONTROLLER, "BRMA14_9H"), Summon(CONTROLLER, "BRMA14_10H")


# Activate!
class BRMA14_10:
	activate = Summon(CONTROLLER, RandomEntourage())

class BRMA14_10H:
	activate = Summon(CONTROLLER, RandomEntourage())


# Potion of Might (The Alchemist)
BRMA15_2He = buff(+2, +2)


# Echolocate
class BRMA16_2:
	activate = Summon(CONTROLLER, "BRMA16_5")

class BRMA16_2H:
	activate = Summon(CONTROLLER, "BRMA16_5")


# Bone Minions
class BRMA17_5:
	activate = Summon(CONTROLLER, "BRMA17_6") * 2

class BRMA17_5H:
	activate = Summon(CONTROLLER, "BRMA17_6H") * 2


##
# Minions

# Moira Bronzebeard
class BRMA03_3:
	update = Refresh(ALL_HERO_POWERS + ID("BRMA03_2"), {GameTag.CANT_PLAY: True})

class BRMA03_3H:
	update = Refresh(ALL_HERO_POWERS + ID("BRMA03_2"), {GameTag.CANT_PLAY: True})


# Corrupted Egg
class BRMA10_4:
	update = (CURRENT_HEALTH(SELF) >= 4) & (Destroy(SELF), Summon(CONTROLLER, "BRMA10_5"))

class BRMA10_4H:
	update = (CURRENT_HEALTH(SELF) >= 5) & (Destroy(SELF), Summon(CONTROLLER, "BRMA10_5H"))


# Firesworn
class BRMA04_3:
	deathrattle = Hit(ENEMY_HERO, Count(ID("BRMA04_3") + KILLED_THIS_TURN))

class BRMA04_3H:
	deathrattle = Hit(ENEMY_HERO, Count(ID("BRMA04_3H") + KILLED_THIS_TURN))


# Chromatic Dragonkin
class BRMA12_8t:
	# That ID is... correct. What?
	events = Play(OPPONENT, SPELL).on(Buff(SELF, "GVG_100e"))


# Son of the Flame
class BRMA13_5:
	play = Hit(TARGET, 6)


##
# Spells

# Flameheart
class BRMA_01:
	play = Draw(CONTROLLER) * 2, GainArmor(FRIENDLY_HERO, 4)


# Get 'em!
class BRMA01_4:
	play = Summon(CONTROLLER, "BRMA01_4t") * 4


# Living Bomb
class BRMA05_3:
	play = Buff(TARGET, "BRMA05_3e")

class BRMA05_3e:
	events = OWN_TURN_BEGIN.on(Hit(ENEMY_CHARACTERS, 5))

class BRMA05_3H:
	play = Buff(TARGET, "BRMA05_3He")

class BRMA05_3He:
	events = OWN_TURN_BEGIN.on(Hit(ENEMY_CHARACTERS, 10))


# TIME FOR SMASH
class BRMA07_3:
	play = Hit(RANDOM_ENEMY_MINION, 5), GainArmor(FRIENDLY_HERO, 5)


# Drakkisath's Command
class BRMA08_3:
	play = Destroy(TARGET), GainArmor(FRIENDLY_HERO, 10)


# The True Warchief
class BRMA09_6:
	play = Destroy(TARGET)


# Rock Out
class BRMA04_4:
	play = Summon(CONTROLLER, "BRMA04_3") * 3

class BRMA04_4H:
	play = Summon(CONTROLLER, "BRMA04_3H") * 3


# Burning Adrenaline
class BRMA11_3:
	play = Hit(ENEMY_HERO, 2)


# Chromatic Mutation (Unused)
class BRMA12_8:
	play = Morph(TARGET, "BRMA12_8t")


# Recharge
class BRMA14_11:
	play = FillMana(CONTROLLER, USED_MANA(CONTROLLER))


# DIE, INSECT!
class BRMA13_8:
	play = Hit(RANDOM_ENEMY_CHARACTER, 8)


# Release the Aberrations!
class BRMA15_3:
	play = Summon(CONTROLLER, "BRMA15_4") * 3


# Arcanotron
class BRMA14_3:
	update = Refresh(ALL_PLAYERS, {GameTag.SPELLPOWER: +2})


# Toxitron
class BRMA14_5:
	events = OWN_TURN_BEGIN.on(Hit(ALL_MINIONS - SELF, 1))

class BRMA14_5H:
	events = OWN_TURN_BEGIN.on(Hit(ALL_MINIONS - SELF, 1))


# Electron
class BRMA14_7:
	update = Refresh(IN_HAND + SPELL, {GameTag.COST: -3})

class BRMA14_7H:
	update = Refresh(IN_HAND + SPELL, {GameTag.COST: -3})


# Magmatron
class BRMA14_9:
	events = Play().on(Hit(ALL_HEROES + CONTROLLED_BY(Play.PLAYER)))

# Magmatron
class BRMA14_9H:
	events = Play().on(Hit(ALL_HEROES + CONTROLLED_BY(Play.PLAYER)))


# Sonic Breath
class BRMA16_3:
	play = Hit(TARGET, 3), Buff(FRIENDLY_WEAPON, "BRMA16_3e")

BRMA16_3e = buff(atk=3)


# Reverberating Gong
class BRMA16_4:
	play = Destroy(ENEMY_WEAPON)


# LAVA!
class BRMA17_4:
	play = Hit(ALL_MINIONS, 2)


##
# Weapons

# Razorgore's Claws (Unused)
class BRMA10_6:
	events = Death(MINION + ID("BRMA10_4")).on(Buff(SELF, "BRMA10_6e"))

BRMA10_6e = buff(atk=1)


# Dragonteeth
class BRMA16_5:
	events = Play(OPPONENT).on(Buff(SELF, "BRMA16_5e"))

BRMA16_5e = buff(atk=1)


##
# Brood Afflictions (Chromaggus)

# Brood Affliction: Red
class BRMA12_3:
	class Hand:
		events = OWN_TURN_BEGIN.on(Hit(FRIENDLY_HERO, 1))

class BRMA12_3H:
	class Hand:
		events = OWN_TURN_BEGIN.on(Hit(FRIENDLY_HERO, 3))


# Brood Affliction: Green
class BRMA12_4:
	class Hand:
		events = OWN_TURN_BEGIN.on(Heal(ENEMY_HERO, 2))

class BRMA12_4H:
	class Hand:
		events = OWN_TURN_BEGIN.on(Heal(ENEMY_HERO, 6))


# Brood Affliction: Blue
class BRMA12_5:
	class Hand:
		update = Refresh(ENEMY_HAND + SPELL, {GameTag.COST: -1})

class BRMA12_5H:
	class Hand:
		update = Refresh(ENEMY_HAND + SPELL, {GameTag.COST: -3})


# Brood Affliction: Black
class BRMA12_6:
	class Hand:
		events = Draw(OPPONENT).on(Give(OPPONENT, Copy(Draw.CARD)))

class BRMA12_6H:
	class Hand:
		events = Draw(OPPONENT).on(Give(OPPONENT, Copy(Draw.CARD)))


# Brood Affliction: Bronze
class BRMA12_7:
	class Hand:
		update = Refresh(ENEMY_HAND + MINION, {GameTag.COST: -1})

class BRMA12_7H:
	class Hand:
		update = Refresh(ENEMY_HAND + MINION, {GameTag.COST: -3})
