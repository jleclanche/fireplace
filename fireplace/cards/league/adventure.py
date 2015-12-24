from ..utils import *


##
# Zinaar

RandomWish = RandomID("LOEA02_03", "LOEA02_04", "LOEA02_05", "LOEA02_06", "LOEA02_10")

# Djinn's Intuition
class LOEA02_02:
	activate = Draw(CONTROLLER), Give(OPPONENT, RandomWish)

class LOEA02_02h:
	activate = Draw(CONTROLLER), GainMana(CONTROLLER, 1), Give(OPPONENT, RandomWish)


# Wish for Power
class LOEA02_03:
	play = Discover(RandomSpell())


# Wish for Valor
class LOEA02_04:
	play = Discover(RandomCollectible(cost=4))


# Wish for Glory
class LOEA02_05:
	play = Discover(RandomMinion())


# Wish for More Wishes
class LOEA02_06:
	play = Discover(RandomWish)


# Wish for Companionship
class LOEA02_10:
	play = Discover(RandomID("NEW1_032", "NEW1_033", "NEW1_034"))


# Leokk (Unused)
class LOEA02_10a:
	update = Refresh(FRIENDLY_MINIONS - SELF, buff="NEW1_033o")


##
# Sun Raider Phaerix

# Blessings of the Sun
class LOEA01_02:
	update = (
		Find(FRIENDLY_MINIONS + ID("LOEA01_11")) & (
			Refresh(FRIENDLY_HERO, {GameTag.CANT_BE_DAMAGED: True})
		),
		Find(ENEMY_MINIONS + ID("LOEA01_11")) & (
			Refresh(ENEMY_HERO, {GameTag.CANT_BE_DAMAGED: True})
		)
	)

class LOEA01_02h:
	events = Summon(CONTROLLER, ID("LOEA01_11h")).on(Buff(Summon.CARD, "LOEA01_11he"))
	update = (
		Find(FRIENDLY_MINIONS + ID("LOEA01_11h")) & (
			Refresh(FRIENDLY_HERO, {GameTag.CANT_BE_DAMAGED: True})
		)
	)

# Rod of the Sun
class LOEA01_11:
	deathrattle = Summon(OPPONENT, "LOEA01_11")

class LOEA01_11h:
	deathrattle = Summon(OPPONENT, "LOEA01_11h")

LOEA01_11he = buff(+3, +3)


# Tol'vir Hoplite
class LOEA01_12:
	deathrattle = Hit(ALL_HEROES, 5)

class LOEA01_12h:
	deathrattle = Hit(ALL_HEROES, 5)


##
# Temple Escape

# Pit of Spikes
class LOEA04_06:
	choose = ("LOEA04_06a", "LOEA04_06b")

# Swing Across
class LOEA04_06a:
	play = COINFLIP & Hit(FRIENDLY_HERO, 10)

# Walk Across Gingerly
class LOEA04_06b:
	play = Hit(FRIENDLY_HERO, 5)


# A Glowing Pool
class LOEA04_28:
	choose = ("LOEA04_28a", "LOEA04_28b")

# Drink Deeply
class LOEA04_28a:
	play = Draw(CONTROLLER)

# Wade Through
class LOEA04_28b:
	play = GainMana(CONTROLLER, 1)


# The Eye
class LOEA04_29:
	choose = ("LOEA04_29a", "LOEA04_29b")

# Touch It
class LOEA04_29a:
	play = Heal(FRIENDLY_HERO, 10)

# Investigate the Runes
class LOEA04_29b:
	play = Draw(CONTROLLER) * 2


# The Darkness
class LOEA04_30:
	choose = ("LOEA04_30a", "LOEA04_31b")

# Take the Shortcut
class LOEA04_30a:
	play = Summon(OPPONENT, "CS2_186")

# Do Nothing
class LOEA04_31b:
	pass


##
# Chieftain Scarvash

# Trogg Hate Minions!
class LOEA05_02:
	# Hearthstone implements Scarvash's Hero Power with LOEA05_02(h) which
	# switches every turn between LOEA05_02a and LOEA05_03. We don't need
	# to do that, we implement it as a Summon every turn instead.
	pass

class LOEA05_02a:
	update = Refresh(ENEMY_HAND + MINION, {GameTag.COST: +2})

class LOEA05_02h:
	pass

class LOEA05_02ha:
	update = Refresh(ENEMY_HAND + MINION, {GameTag.COST: SET(11)})


# Trogg Hate Spells
class LOEA05_03:
	update = Refresh(ENEMY_HAND + SPELL, {GameTag.COST: +2})

class LOEA05_03h:
	update = Refresh(ENEMY_HAND + SPELL, {GameTag.COST: SET(11)})


##
# Mine Cart Rush

# Throw Rocks
class LOEA07_29:
	activate = Hit(RANDOM_ENEMY_MINION, 3)


# Dynamite
class LOEA07_18:
	play = Hit(TARGET, 10)


# Boom!
class LOEA07_20:
	play = Hit(ENEMY_MINIONS, 3)


# Consult Brann
class LOEA07_26:
	play = Draw(CONTROLLER) * 3


# Repairs
class LOEA07_28:
	play = Heal(TARGET, 10)


##
# Lord Slitherspear

# Enraged!
class LOEA09_2:
	activate = Buff(FRIENDLY_HERO, "LOEA09_2e")

LOEA09_2e = buff(atk=2)

class LOEA09_2H:
	activate = Buff(FRIENDLY_HERO, "LOEA09_2e")

LOEA09_2eH = buff(atk=5)


# Slithering Archer
class LOEA09_6:
	play = Hit(TARGET, 1)

class LOEA09_6H:
	play = Hit(ENEMY_MINIONS, 2)


# Cauldron
class LOEA09_7:
	deathrattle = Give(OPPONENT, "LOE_076"), Summon(CONTROLLER, "LOEA09_2")

# Cauldron (Unused)
class LOEA09_7H:
	deathrattle = Give(OPPONENT, "LOE_076"), Summon(CONTROLLER, "LOEA09_2H")


##
# Giantfin

# Mrglmrgl MRGL!
class LOEA16_2:
	activate = DrawUntil(CONTROLLER, Count(ENEMY_HAND))

class LOEA16_2H:
	activate = Draw(CONTROLLER) * 2


# Mrgl Mrgl Nyah Nyah
class LOEA10_5:
	play = Summon(CONTROLLER, Copy(RANDOM(KILLED + MURLOC) * 5))

class LOEA10_5H:
	play = Summon(CONTROLLER, Copy(RANDOM(KILLED + MURLOC) * 5))


##
# Arch-Thief Rafaam

# Unstable Portal
class LOEA15_2:
	activate = Give(CONTROLLER, RandomMinion()).then(Buff(Give.CARD, "GVG_003e"))

class LOEA15_2H:
	activate = Give(CONTROLLER, RandomMinion()).then(Buff(Give.CARD, "GVG_003e"))


# Rare Spear
class LOEA09_4:
	events = Play(OPPONENT, RARE).on(Buff(SELF, "EX1_409e"))

class LOEA09_4H:
	events = Play(OPPONENT, RARE).on(Buff(SELF, "EX1_409e"))


##
# Rafaam Unleashed

# Rummage
class LOEA16_16:
	activate = Give(CONTROLLER, RandomEntourage())

class LOEA16_16H:
	activate = Give(CONTROLLER, RandomEntourage())


# Shard of Sulfuras
class LOEA16_6:
	play = Hit(ALL_CHARACTERS, 5)


# Benediction Splinter
class LOEA16_7:
	play = Heal(ALL_CHARACTERS, 10)


# Putress' Vial
class LOEA16_8:
	play = Destroy(RANDOM_ENEMY_MINION)


# Lothar's Left Greave
class LOEA16_9:
	play = Hit(ENEMY_CHARACTERS, 3)


# Hakkari Blood Goblet
class LOEA16_10:
	play = Morph(TARGET, "LOE_010")


# Crown of Kael'thas
class LOEA16_11:
	play = Hit(RANDOM_CHARACTER, 1) * 10


# Medivh's Locket
class LOEA16_12:
	play = Morph(FRIENDLY_HAND, "GVG_003")


# Khadgar's Pipe
class LOEA16_14:
	play = (
		Give(OPPONENT, RandomSpell()),
		Give(PLAYER, RandomSpell()).then(Buff(Give.CARD, "LOEA16_14e"))
	)

@custom_card
class LOEA16_14e:
	tags = {
		GameTag.CARDNAME: "Khadgar's Pipe Buff",
		GameTag.CARDTYPE: CardType.ENCHANTMENT,
	}
	cost = SET(0)


# Ysera's Tear
class LOEA16_15:
	play = ManaThisTurn(CONTROLLER, 4)


# Zinaar
class LOEA16_18:
	events = OWN_TURN_END.on(Give(CONTROLLER, RandomWish))

class LOEA16_18H:
	events = OWN_TURN_END.on(Give(CONTROLLER, RandomWish))


# Sun Raider Phaerix
class LOEA16_19:
	events = OWN_TURN_END.on(Give(CONTROLLER, "LOEA16_20"))

class LOEA16_19H:
	update = Refresh(FRIENDLY_MINIONS - SELF, {GameTag.CANT_BE_DAMAGED: True})


# Chieftain Scarvash
class LOEA16_21:
	update = Refresh(ENEMY_HAND, {GameTag.COST: +1})

class LOEA16_21H:
	update = Refresh(ENEMY_HAND, {GameTag.COST: +2})


# Archaedas
class LOEA16_22:
	events = OWN_TURN_END.on(Morph(RANDOM_ENEMY_MINION, "LOEA06_02t"))

class LOEA16_22H:
	events = OWN_TURN_END.on(Morph(RANDOM_ENEMY_MINION, "LOEA06_02t"))


# Lord Slitherspear
class LOEA16_23:
	events = OWN_TURN_END.on(Summon(CONTROLLER, "LOEA09_5") * Count(ENEMY_MINIONS))

class LOEA16_23H:
	events = OWN_TURN_END.on(Summon(CONTROLLER, "LOEA09_5") * Count(ENEMY_MINIONS))


# Giantfin
class LOEA16_24:
	events = OWN_TURN_END.on(DrawUntil(CONTROLLER, Count(ENEMY_HAND)))

class LOEA16_24H:
	events = OWN_TURN_END.on(Draw(CONTROLLER) * 2)


# Blessing of the Sun
class LOEA16_20:
	play = Buff(TARGET, "LOEA16_20e")

LOEA16_20e = buff(immune=True)


##
# Unused

# Eye of Hakkar
class LOE_008:
	play = Summon(CONTROLLER, RANDOM(ENEMY_DECK + SECRET))

class LOE_008H:
	play = Summon(CONTROLLER, RANDOM(ENEMY_DECK + SECRET))


# Boneraptor
class LOEA15_3:
	play = Steal(ENEMY_WEAPON)

class LOEA15_3H:
	play = Steal(ENEMY_WEAPON)
