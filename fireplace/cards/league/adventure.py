from ..utils import *


##
# Zinaar

RandomWish = RandomID("LOEA02_03", "LOEA02_04", "LOEA02_05", "LOEA02_06", "LOEA02_10")


class LOEA02_02:
	"""Djinn’s Intuition"""
	activate = Draw(CONTROLLER), Give(OPPONENT, RandomWish)


class LOEA02_02h:
	activate = Draw(CONTROLLER), GainMana(CONTROLLER, 1), Give(OPPONENT, RandomWish)


class LOEA02_03:
	"""Wish for Power"""
	play = DISCOVER(RandomSpell())


class LOEA02_04:
	"""Wish for Valor"""
	play = DISCOVER(RandomCollectible(cost=4))


class LOEA02_05:
	"""Wish for Glory"""
	play = DISCOVER(RandomMinion())


class LOEA02_06:
	"""Wish for More Wishes"""
	play = Give(CONTROLLER, RandomWish) * 2


class LOEA02_10:
	"""Wish for Companionship"""
	play = DISCOVER(RandomID("NEW1_032", "NEW1_033", "NEW1_034"))


class LOEA02_10a:
	"""Leokk (Unused)"""
	requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
	update = Refresh(FRIENDLY_MINIONS - SELF, buff="NEW1_033o")


##
# Sun Raider Phaerix

class LOEA01_02:
	"""Blessings of the Sun"""
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


class LOEA01_11:
	"""Rod of the Sun"""
	deathrattle = Summon(OPPONENT, "LOEA01_11")


class LOEA01_11h:
	deathrattle = Summon(OPPONENT, "LOEA01_11h")


LOEA01_11he = buff(+3, +3)


class LOEA01_12:
	"""Tol'vir Hoplite"""
	deathrattle = Hit(ALL_HEROES, 5)


class LOEA01_12h:
	deathrattle = Hit(ALL_HEROES, 5)


##
# Temple Escape

class LOEA04_06:
	"""Pit of Spikes"""
	choose = ("LOEA04_06a", "LOEA04_06b")


class LOEA04_06a:
	"""Swing Across"""
	play = COINFLIP & Hit(FRIENDLY_HERO, 10)


class LOEA04_06b:
	"""Walk Across Gingerly"""
	play = Hit(FRIENDLY_HERO, 5)


class LOEA04_28:
	"""A Glowing Pool"""
	choose = ("LOEA04_28a", "LOEA04_28b")


class LOEA04_28a:
	"""Drink Deeply"""
	play = Draw(CONTROLLER)


class LOEA04_28b:
	"""Wade Through"""
	play = GainMana(CONTROLLER, 1)


class LOEA04_29:
	"""The Eye"""
	choose = ("LOEA04_29a", "LOEA04_29b")


class LOEA04_29a:
	"""Touch It"""
	play = Heal(FRIENDLY_HERO, 10)


class LOEA04_29b:
	"""Investigate the Runes"""
	play = Draw(CONTROLLER) * 2


class LOEA04_30:
	"""The Darkness"""
	choose = ("LOEA04_30a", "LOEA04_31b")


class LOEA04_30a:
	"""Take the Shortcut"""
	play = Summon(OPPONENT, "CS2_186")


class LOEA04_31b:
	"""No Way!"""
	pass


class LOEA04_25:
	"""Seething Statue"""
	events = OWN_TURN_END.on(Hit(ENEMY_CHARACTERS, 2))


class LOEA04_25h:
	events = OWN_TURN_END.on(Hit(ENEMY_CHARACTERS, 5))


class LOE_024t:
	"""Rolling Boulder"""
	events = OWN_TURN_END.on(Destroy(LEFT_OF(SELF)))


##
# Chieftain Scarvash

class LOEA05_02:
	"""Trogg Hate Minions!"""
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


class LOEA05_03:
	"""Trogg Hate Spells!"""
	update = Refresh(ENEMY_HAND + SPELL, {GameTag.COST: +2})


class LOEA05_03h:
	update = Refresh(ENEMY_HAND + SPELL, {GameTag.COST: SET(11)})


##
# Mine Cart Rush

class LOEA07_29:
	"""Throw Rocks"""
	activate = Hit(RANDOM_ENEMY_MINION, 3)


class LOEA07_18:
	"""Dynamite"""
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Hit(TARGET, 10)


class LOEA07_20:
	"""Boom!"""
	play = Hit(ENEMY_MINIONS, 3)


class LOEA07_26:
	"""Consult Brann"""
	play = Draw(CONTROLLER) * 3


class LOEA07_28:
	"""Repairs"""
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Heal(TARGET, 10)


##
# Archaedas

class LOEA06_02:
	"""Stonesculpting"""
	activate = Summon(ALL_PLAYERS, "LOEA06_02t")


class LOEA06_02h:
	activate = Summon(CONTROLLER, "LOEA06_02t"), Summon(OPPONENT, "LOEA06_02th")


class LOEA06_03:
	"""Animate Earthen"""
	requirements = {PlayReq.REQ_MINIMUM_TOTAL_MINIONS: 1}
	play = Buff(FRIENDLY_MINIONS, "LOEA06_03e")


LOEA06_03e = buff(+1, +1, taunt=True)


class LOEA06_03h:
	play = Buff(FRIENDLY_MINIONS, "LOEA06_03eh")


LOEA06_03eh = buff(+3, +3, taunt=True)


class LOEA06_04:
	"""Shattering Spree"""
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = (
		Hit(TARGET, Count(ALL_MINIONS + ID("LOEA06_02t"))),
		Destroy(ALL_MINIONS + ID("LOEA06_02t"))
	)


class LOEA06_04h:
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = (
		Hit(TARGET, Count(ALL_MINIONS + ID("LOEA06_02th")) * 3),
		Destroy(ALL_MINIONS + ID("LOEA06_02th"))
	)


##
# Lord Slitherspear

HUNGRY_NAGA = (
	ID("LOEA09_5") |
	ID("LOEA09_5H") |
	ID("LOEA09_10") |
	ID("LOEA09_11") |
	ID("LOEA09_12") |
	ID("LOEA09_13")
)


class LOEA09_2:
	"""Enraged!"""
	activate = Buff(FRIENDLY_HERO, "LOEA09_2e")


LOEA09_2e = buff(atk=2)


class LOEA09_2H:
	"""Enraged! (Heroic)"""
	activate = Buff(FRIENDLY_HERO, "LOEA09_2e")


LOEA09_2eH = buff(atk=5)


class LOEA09_3:
	"""Getting Hungry"""
	activate = Summon("LOEA09_5").then(
		Buff(Summon.CARD, "LOEA09_3a") * Attr(
			CONTROLLER, GameTag.NUM_TIMES_HERO_POWER_USED_THIS_GAME
		)
	)


LOEA09_3a = buff(atk=1)


class LOEA09_3H:
	"""Getting Hungry (Heroic)"""
	activate = Summon("LOEA09_5").then(
		Buff(Summon.CARD, "LOEA09_3aH") * Attr(
			CONTROLLER, GameTag.NUM_TIMES_HERO_POWER_USED_THIS_GAME
		)
	)


LOEA09_3aH = buff(+1, +1)


class LOEA09_3b:
	"""Getting Hungry (Unused versions)"""
	activate = Summon(CONTROLLER, "LOEA09_11")


class LOEA09_3c:
	activate = Summon(CONTROLLER, "LOEA09_10")


class LOEA09_3d:
	activate = Summon(CONTROLLER, "LOEA09_13")


class LOEA09_6:
	"""Slithering Archer"""
	requirements = {PlayReq.REQ_NONSELF_TARGET: 0, PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	play = Hit(TARGET, 1)


class LOEA09_6H:
	"""Slithering Archer (Heroic)"""
	play = Hit(ENEMY_MINIONS, 2)


class LOEA09_7:
	"""Cauldron"""
	deathrattle = Give(OPPONENT, "LOE_076"), Summon(CONTROLLER, "LOEA09_2")


class LOEA09_7H:
	"""Cauldron (Unused)"""
	deathrattle = Give(OPPONENT, "LOE_076"), Summon(CONTROLLER, "LOEA09_2H")


class LOEA09_9:
	"""Naga Repellent"""
	play = Destroy(ALL_MINIONS + HUNGRY_NAGA)


class LOEA09_9H:
	"""Naga Repellent (Heroic)"""
	play = Buff(ALL_MINIONS + HUNGRY_NAGA, "EX1_360e")


##
# Giantfin

class LOEA10_2:
	"""Mrglmrgl MRGL!"""
	activate = DrawUntil(CONTROLLER, Count(ENEMY_HAND))


class LOEA10_2H:
	"""Mrglmrgl MRGL! (Heroic)"""
	activate = Draw(CONTROLLER) * 2


class LOEA10_5:
	"""Mrgl Mrgl Nyah Nyah"""
	play = Summon(CONTROLLER, Copy(RANDOM(KILLED + MURLOC) * 5))


class LOEA10_5H:
	"""Mrgl Mrgl Nyah Nyah (Heroic)"""
	play = Summon(CONTROLLER, Copy(RANDOM(KILLED + MURLOC) * 5))


##
# Skelesaurus Hex

class LOEA13_2:
	"""Ancient Power"""
	activate = Give(ALL_PLAYERS, RandomCollectible()).then(Buff(Give.CARD, "LOEA13_2e"))


class LOEA13_2H:
	"""Ancient Power (Heroic)"""
	activate = Give(CONTROLLER, RandomCollectible()).then(Buff(Give.CARD, "LOEA13_2e"))


@custom_card
class LOEA13_2e:
	tags = {
		GameTag.CARDNAME: "Ancient Power buff",
		GameTag.CARDTYPE: CardType.ENCHANTMENT,
	}
	cost = SET(0)


##
# The Steel Sentinel

class LOEA14_2:
	"""Platemail Armor"""
	update = Refresh(FRIENDLY_HERO, {GameTag.HEAVILY_ARMORED: True})


class LOEA14_2H:
	"""Platemail Armor (Heroic)"""
	update = Refresh(FRIENDLY_CHARACTERS, {GameTag.HEAVILY_ARMORED: True})


##
# Arch-Thief Rafaam

class LOEA15_2:
	"""Unstable Portal"""
	activate = Give(CONTROLLER, RandomMinion()).then(Buff(Give.CARD, "GVG_003e"))


class LOEA15_2H:
	"""Unstable Portal (Heroic)"""
	activate = Give(CONTROLLER, RandomMinion()).then(Buff(Give.CARD, "GVG_003e"))


class LOEA09_4:
	"""Rare Spear"""
	events = Play(OPPONENT, RARE).on(Buff(SELF, "EX1_409e"))


class LOEA09_4H:
	"""Rare Spear (Heroic)"""
	events = Play(OPPONENT, RARE).on(Buff(SELF, "EX1_409e"))


##
# Rafaam Unleashed

class LOEA16_2:
	"""Staff of Origination"""
	update = Refresh(FRIENDLY_HERO, {GameTag.CANT_BE_DAMAGED: True})


class LOEA16_2H:
	"""Staff of Origination (Heroic)"""
	update = Refresh(FRIENDLY_HERO, {GameTag.CANT_BE_DAMAGED: True})


class LOEA16_16:
	"""Rummage"""
	entourage = [
		"LOEA16_10", "LOEA16_11", "LOEA16_14", "LOEA16_15", "LOEA16_6",
		"LOEA16_7", "LOEA16_9", "LOEA16_12", "LOEA16_13", "LOEA16_8"]
	activate = Give(CONTROLLER, RandomEntourage())


class LOEA16_16H:
	"""Rummage (Heroic)"""
	entourage = [
		"LOEA16_10", "LOEA16_11", "LOEA16_14", "LOEA16_15", "LOEA16_6",
		"LOEA16_7", "LOEA16_9", "LOEA16_12", "LOEA16_13", "LOEA16_8"]
	activate = Give(CONTROLLER, RandomEntourage())


class LOEA16_6:
	"""Shard of Sulfuras"""
	play = Hit(ALL_CHARACTERS, 5)


class LOEA16_7:
	"""Benediction Splinter"""
	play = Heal(ALL_CHARACTERS, 10)


class LOEA16_8:
	"""Putress' Vial"""
	play = Destroy(RANDOM_ENEMY_MINION)


# Putressed (Unused)
LOEA16_8a = AttackHealthSwapBuff()


class LOEA16_9:
	"""Lothar's Left Greave"""
	play = Hit(ENEMY_CHARACTERS, 3)


class LOEA16_10:
	"""Hakkari Blood Goblet"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Morph(TARGET, "LOE_010")


class LOEA16_11:
	"""Crown of Kael'thas"""
	play = Hit(RANDOM_CHARACTER, 1) * 10


class LOEA16_12:
	"""Medivh's Locket"""
	play = Morph(FRIENDLY_HAND, "GVG_003")


class LOEA16_14:
	"""Khadgar's Pipe"""
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


class LOEA16_15:
	"""Ysera's Tear"""
	play = ManaThisTurn(CONTROLLER, 4)


class LOEA16_18:
	"""Zinaar"""
	events = OWN_TURN_END.on(Give(CONTROLLER, RandomWish))


class LOEA16_18H:
	"""Zinaar (Heroic)"""
	events = OWN_TURN_END.on(Give(CONTROLLER, RandomWish))


class LOEA16_19:
	"""Sun Raider Phaerix"""
	events = OWN_TURN_END.on(Give(CONTROLLER, "LOEA16_20"))


class LOEA16_19H:
	"""Sun Raider Phaerix (Heroic)"""
	update = Refresh(FRIENDLY_MINIONS - SELF, {GameTag.CANT_BE_DAMAGED: True})


LOEA16_20H = buff(immune=True)


class LOEA16_21:
	"""Chieftain Scarvash"""
	update = Refresh(ENEMY_HAND, {GameTag.COST: +1})


class LOEA16_21H:
	"""Chieftain Scarvash (Heroic)"""
	update = Refresh(ENEMY_HAND, {GameTag.COST: +2})


class LOEA16_22:
	"""Archaedas"""
	events = OWN_TURN_END.on(Morph(RANDOM_ENEMY_MINION, "LOEA06_02t"))


class LOEA16_22H:
	"""Archaedas (Heroic)"""
	events = OWN_TURN_END.on(Morph(RANDOM_ENEMY_MINION, "LOEA06_02t"))


class LOEA16_23:
	"""Lord Slitherspear"""
	events = OWN_TURN_END.on(Summon(CONTROLLER, "LOEA09_5") * Count(ENEMY_MINIONS))


class LOEA16_23H:
	"""Lord Slitherspear (Heroic)"""
	events = OWN_TURN_END.on(Summon(CONTROLLER, "LOEA09_5") * Count(ENEMY_MINIONS))


class LOEA16_24:
	"""Giantfin"""
	events = OWN_TURN_END.on(DrawUntil(CONTROLLER, Count(ENEMY_HAND)))


class LOEA16_24H:
	"""Giantfin (Heroic)"""
	events = OWN_TURN_END.on(Draw(CONTROLLER) * 2)


class LOEA16_26:
	"""Skelesaurus Hex"""
	events = OWN_TURN_END.on(
		Give(ALL_PLAYERS, RandomCollectible()).then(Buff(Give.CARD, "LOEA13_2e"))
	)


class LOEA16_26H:
	"""Skelesaurus Hex (Heroic)"""
	events = OWN_TURN_END.on(
		Give(CONTROLLER, RandomCollectible()).then(Buff(Give.CARD, "LOEA13_2e"))
	)


class LOEA16_27:
	"""The Steel Sentinel"""
	tags = {GameTag.HEAVILY_ARMORED: True}


class LOEA16_27H:
	"""The Steel Sentinel (Heroic)"""
	tags = {GameTag.HEAVILY_ARMORED: True}


class LOEA16_20:
	"""Blessing of the Sun"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Buff(TARGET, "LOEA16_20e")


LOEA16_20e = buff(immune=True)


##
# Misc.

class LOE_008:
	"""Eye of Hakkar (Unused)"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0}
	play = Summon(CONTROLLER, RANDOM(ENEMY_DECK + SECRET))


class LOE_008H:
	"""Eye of Hakkar (Unused) (Heroic)"""
	play = Summon(CONTROLLER, RANDOM(ENEMY_DECK + SECRET))


class LOEA_01:
	"""Looming Presence"""
	play = Draw(CONTROLLER) * 2, GainArmor(FRIENDLY_HERO, 4)


class LOEA_01H:
	"""Looming Presence (Heroic)"""
	play = Draw(CONTROLLER) * 3, GainArmor(FRIENDLY_HERO, 6)


class LOEA15_3:
	"""Boneraptor (Unused)"""
	play = Steal(ENEMY_WEAPON)


class LOEA15_3H:
	"""Boneraptor (Unused) (Heroic)"""
	play = Steal(ENEMY_WEAPON)
