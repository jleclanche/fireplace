from ..utils import *


##
# Hero Powers

# Pile On!
class BRMA01_2:
	activate = (
		Summon(CONTROLLER, RANDOM(CONTROLLER_DECK + MINION)),
		Summon(OPPONENT, RANDOM(OPPONENT_DECK + MINION))
	)

class BRMA01_2H:
	activate = (
		Summon(CONTROLLER, RANDOM(CONTROLLER_DECK + MINION) * 2),
		Summon(OPPONENT, RANDOM(OPPONENT_DECK + MINION))
	)


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
		(Attr(OPPONENT, GameTag.RESOURCES) <= Attr(OPPONENT, GameTag.RESOURCES_USED)) &
		Hit(ENEMY_HERO, 5)
	)

class BRMA05_2H:
	activate = (
		(Attr(OPPONENT, GameTag.RESOURCES) <= Attr(OPPONENT, GameTag.RESOURCES_USED)) &
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


# The Rookery
class BRMA10_3:
	activate = Buff(ALL_MINIONS + ID("BRMA10_4"), "BRMA10_3e"), Summon(CONTROLLER, "BRMA10_4")

# The Rookery
class BRMA10_3H:
	activate = Buff(ALL_MINIONS + ID("BRMA10_4"), "BRMA10_3e"), Summon(CONTROLLER, "BRMA10_4")


# Essence of the Red
class BRMA11_2:
	activate = Draw(ALL_PLAYERS) * 2

class BRMA11_2H:
	activate = Draw(ALL_PLAYERS) * 3, GainMana(CONTROLLER, 1)


# Wild Magic
class BRMA13_4:
	activate = Give(CONTROLLER, RandomSpell(card_class=Attr(TARGET, GameTag.CLASS)))

class BRMA13_4H:
	activate = Give(CONTROLLER, RandomSpell(card_class=Attr(TARGET, GameTag.CLASS)))


# Echolocate
class BRMA16_2:
	activate = Summon(CONTROLLER, "BRMA16_5")

class BRMA16_2H:
	activate = Summon(CONTROLLER, "BRMA16_5")


# Mutation (Unused)
class BRMA12_10:
	activate = Discard(RANDOM(CONTROLLER_HAND))


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
	# The attack targeting is done at the AI level. But we could do this:
	# attack_targets = ENEMY_HERO | TAUNT

class BRMA03_3H:
	update = Refresh(ALL_HERO_POWERS + ID("BRMA03_2"), {GameTag.CANT_PLAY: True})


# Corrupted Egg
class BRMA10_4:
	update = (Attr(SELF, "health") >= 4) & (Destroy(SELF), Summon(CONTROLLER, "BRMA10_5"))

class BRMA10_4H:
	update = (Attr(SELF, "health") >= 5) & (Destroy(SELF), Summon(CONTROLLER, "BRMA10_5H"))


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


# DIE, INSECT!
class BRMA13_8:
	play = Hit(RANDOM_ENEMY_CHARACTER, 8)


# Release the Aberrations!
class BRMA15_3:
	play = Summon(CONTROLLER, "BRMA15_4") * 3


# Sonic Breath
class BRMA16_3:
	play = Hit(TARGET, 3), Buff(FRIENDLY_WEAPON, "BRMA16_3e")


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


# Dragonteeth
class BRMA16_5:
	events = Play(OPPONENT).on(Buff(SELF, "BRMA16_5e"))
