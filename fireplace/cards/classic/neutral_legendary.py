from ..utils import *


class EX1_002:
	"""The Black Knight"""
	requirements = {
		PlayReq.REQ_ENEMY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_MUST_TARGET_TAUNTER: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	play = Destroy(TARGET)


class EX1_012:
	"""Bloodmage Thalnos"""
	deathrattle = Draw(CONTROLLER)


class EX1_014:
	"""King Mukla"""
	play = Give(OPPONENT, "EX1_014t") * 2


class EX1_014t:
	"""Bananas"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Buff(TARGET, "EX1_014te")


EX1_014te = buff(+1, +1)


class EX1_016:
	"""Sylvanas Windrunner"""
	deathrattle = Steal(RANDOM_ENEMY_MINION)


class EX1_062:
	"""Old Murk-Eye"""
	update = Refresh(SELF, {GameTag.ATK: Count(ALL_MINIONS + MURLOC - SELF)})


class EX1_083:
	"""Tinkmaster Overspark"""
	play = Morph(RANDOM(ALL_MINIONS - SELF), RandomID("EX1_tk28", "EX1_tk29"))


class EX1_100:
	"""Lorewalker Cho"""
	events = Play(ALL_PLAYERS, SPELL).on(Give(Opponent(Play.PLAYER), Copy(Play.CARD)))


class EX1_110:
	"""Cairne Bloodhoof"""
	deathrattle = Summon(CONTROLLER, "EX1_110t")


class EX1_112:
	"""Gelbin Mekkatorque"""
	entourage = ["Mekka1", "Mekka2", "Mekka3", "Mekka4"]
	play = Summon(CONTROLLER, RandomEntourage())


class Mekka1:
	"""Homing Chicken"""
	events = OWN_TURN_BEGIN.on(Destroy(SELF), Draw(CONTROLLER) * 3)


class Mekka2:
	"""Repair Bot"""
	events = OWN_TURN_END.on(Heal(RANDOM(DAMAGED_CHARACTERS), 6))


class Mekka3:
	"""Emboldener 3000"""
	events = OWN_TURN_END.on(Buff(RANDOM_MINION, "Mekka3e"))


Mekka3e = buff(+1, +1)


class Mekka4:
	"""Poultryizer"""
	events = OWN_TURN_BEGIN.on(Morph(RANDOM_MINION, "Mekka4t"))


class EX1_116:
	"""Leeroy Jenkins"""
	play = Summon(OPPONENT, "EX1_116t") * 2


class EX1_249:
	"""Baron Geddon"""
	events = OWN_TURN_END.on(Hit(ALL_CHARACTERS - SELF, 2))


class EX1_298:
	"""Ragnaros the Firelord"""
	events = OWN_TURN_END.on(Hit(RANDOM_ENEMY_CHARACTER, 8))


class EX1_557:
	"""Nat Pagle"""
	events = OWN_TURN_BEGIN.on(COINFLIP & Draw(CONTROLLER))


class EX1_558:
	"""Harrison Jones"""
	play = (
		Draw(CONTROLLER) * Attr(ENEMY_WEAPON, GameTag.DURABILITY),
		Destroy(ENEMY_WEAPON)
	)


class EX1_560:
	"""Nozdormu"""
	update = Refresh(ALL_PLAYERS, {GameTag.TIMEOUT: lambda self, i: 15})


class EX1_561:
	"""Alexstrasza"""
	requirements = {PlayReq.REQ_HERO_TARGET: 0, PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	play = (
		(Attr(TARGET, GameTag.HEALTH) <= 15) & Buff(TARGET, "EX1_561e"),
		SetCurrentHealth(TARGET, 15)
	)


class EX1_561e:
	max_health = SET(15)


class EX1_562:
	"""Onyxia"""
	play = Summon(CONTROLLER, "ds1_whelptoken") * 7


class EX1_572:
	"""Ysera"""
	events = OWN_TURN_END.on(
		Give(CONTROLLER, RandomCard(card_class=CardClass.DREAM))
	)


class DREAM_02:
	"""Ysera Awakens"""
	play = Hit(ALL_CHARACTERS - ID("EX1_572"), 5)


class DREAM_04:
	"""Dream"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Bounce(TARGET)


class DREAM_05:
	"""Nightmare"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Buff(TARGET, "DREAM_05e")


class DREAM_05e:
	events = OWN_TURN_BEGIN.on(Destroy(SELF))


class EX1_577:
	"""The Beast"""
	deathratte = Summon(OPPONENT, "EX1_finkle")


class EX1_614:
	"""Xavius"""
	events = OWN_CARD_PLAY.on(Summon(CONTROLLER, "EX1_614t"))


class NEW1_024:
	"""Captain Greenskin"""
	play = Buff(FRIENDLY_WEAPON, "NEW1_024o")


NEW1_024o = buff(+1, +1)


class NEW1_029:
	"""Millhouse Manastorm"""
	play = Buff(ENEMY_HERO, "NEW1_029t")


class NEW1_029t:
	update = Refresh(ENEMY_HAND + SPELL, {GameTag.COST: lambda self, i: 0})
	events = OWN_TURN_BEGIN.on(Destroy(SELF))


class NEW1_030:
	"""Deathwing"""
	play = Destroy(ALL_MINIONS - SELF), Discard(FRIENDLY_HAND)


class NEW1_038:
	"""Gruul"""
	events = TURN_END.on(Buff(SELF, "NEW1_038o"))


NEW1_038o = buff(+1, +1)


class NEW1_040:
	"""Hogger"""
	events = OWN_TURN_END.on(Summon(CONTROLLER, "NEW1_040t"))


class PRO_001:
	"""Elite Tauren Chieftain"""
	entourage = ["PRO_001a", "PRO_001b", "PRO_001c"]
	play = Give(ALL_PLAYERS, RandomEntourage())


class PRO_001a:
	"""I Am Murloc"""
	requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
	play = Summon(CONTROLLER, "PRO_001at") * RandomNumber(3, 4, 5)


class PRO_001b:
	"""Rogues Do It..."""
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Hit(TARGET, 4), Draw(CONTROLLER)


class PRO_001c:
	"""Power of the Horde"""
	requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
	entourage = ["CS2_121", "EX1_021", "EX1_023", "EX1_110", "EX1_390", "CS2_179"]
	play = Summon(CONTROLLER, RandomEntourage())
