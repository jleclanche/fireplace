from ..utils import *


##
# Free basic minions

class CS2_122:
	"""Raid Leader"""
	update = Refresh(FRIENDLY_MINIONS - SELF, buff="CS2_122e")


CS2_122e = buff(atk=1)


class CS2_222:
	"""Stormwind Champion"""
	update = Refresh(FRIENDLY_MINIONS - SELF, buff="CS2_222o")


CS2_222o = buff(+1, +1)


class CS2_226:
	"""Frostwolf Warlord"""
	play = Buff(SELF, "CS2_226e") * Count(FRIENDLY_MINIONS - SELF)


CS2_226e = buff(+1, +1)


class EX1_011:
	"""Voodoo Doctor"""
	requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	play = Heal(TARGET, 2)


class EX1_015:
	"""Novice Engineer"""
	play = Draw(CONTROLLER)


class EX1_082:
	"""Mad Bomber"""
	play = Hit(RANDOM_OTHER_CHARACTER, 1) * 3


class EX1_102:
	"""Demolisher"""
	events = OWN_TURN_BEGIN.on(Hit(RANDOM_ENEMY_CHARACTER, 2))


class EX1_162:
	"""Dire Wolf Alpha"""
	update = Refresh(SELF_ADJACENT, buff="EX1_162o")


EX1_162o = buff(atk=1)


class EX1_399:
	"""Gurubashi Berserker"""
	events = SELF_DAMAGE.on(Buff(SELF, "EX1_399e"))


EX1_399e = buff(atk=3)


class EX1_508:
	"""Grimscale Oracle"""
	update = Refresh(FRIENDLY_MINIONS + MURLOC - SELF, buff="EX1_508o")


EX1_508o = buff(atk=1)


class EX1_593:
	"""Nightblade"""
	play = Hit(ENEMY_HERO, 3)


class EX1_595:
	"""Cult Master"""
	events = Death(FRIENDLY + MINION).on(Draw(CONTROLLER))


##
# Common basic minions

class CS2_117:
	"""Earthen Ring Farseer"""
	requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	play = Heal(TARGET, 3)


class CS2_141:
	"""Ironforge Rifleman"""
	requirements = {PlayReq.REQ_NONSELF_TARGET: 0, PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	play = Hit(TARGET, 1)


class CS2_146:
	"""Southsea Deckhand"""
	update = Find(FRIENDLY_WEAPON) & Refresh(SELF, {GameTag.CHARGE: True})


class CS2_147:
	"""Gnomish Inventor"""
	play = Draw(CONTROLLER)


class CS2_150:
	"""Stormpike Commando"""
	requirements = {PlayReq.REQ_NONSELF_TARGET: 0, PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	play = Hit(TARGET, 2)


class CS2_151:
	"""Silver Hand Knight"""
	play = Summon(CONTROLLER, "CS2_152")


class CS2_189:
	"""Elven Archer"""
	requirements = {PlayReq.REQ_NONSELF_TARGET: 0, PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	play = Hit(TARGET, 1)


class CS2_188:
	"""Abusive Sergeant"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	play = Buff(TARGET, "CS2_188o")


CS2_188o = buff(atk=2)


class CS2_196:
	"""Razorfen Hunter"""
	play = Summon(CONTROLLER, "CS2_boar")


class CS2_203:
	"""Ironbeak Owl"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	play = Silence(TARGET)


class CS2_221:
	"""Spiteful Smith"""
	enrage = Refresh(FRIENDLY_WEAPON, buff="CS2_221e")


CS2_221e = buff(atk=2)


class CS2_227:
	"""Venture Co. Mercenary"""
	update = Refresh(FRIENDLY_HAND + MINION, {GameTag.COST: +3})


class DS1_055:
	"""Darkscale Healer"""
	play = Heal(FRIENDLY_CHARACTERS, 2)


class EX1_007:
	"""Acolyte of Pain"""
	events = SELF_DAMAGE.on(Draw(CONTROLLER))


class EX1_019:
	"""Shattered Sun Cleric"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	play = Buff(TARGET, "EX1_019e")


EX1_019e = buff(+1, +1)


class EX1_025:
	"""Dragonling Mechanic"""
	play = Summon(CONTROLLER, "EX1_025t")


class EX1_029:
	"""Leper Gnome"""
	deathrattle = Hit(ENEMY_HERO, 2)


class EX1_046:
	"""Dark Iron Dwarf"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	play = Buff(TARGET, "EX1_046e")


EX1_046e = buff(atk=2)


class EX1_048:
	"""Spellbreaker"""
	requirements = {
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_NONSELF_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	play = Silence(TARGET)


class EX1_049:
	"""Youthful Brewmaster"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_NONSELF_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	play = Bounce(TARGET)


class EX1_057:
	"""Ancient Brewmaster"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_NONSELF_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	play = Bounce(TARGET)


class EX1_066:
	"""Acidic Swamp Ooze"""
	play = Destroy(ENEMY_WEAPON)


class EX1_096:
	"""Loot Hoarder"""
	deathrattle = Draw(CONTROLLER)


class EX1_283:
	"""Frost Elemental"""
	requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	play = Freeze(TARGET)


class EX1_390:
	"""Tauren Warrior"""
	enrage = Refresh(SELF, buff="EX1_390e")


EX1_390e = buff(atk=3)


class EX1_393:
	"""Amani Berserker"""
	enrage = Refresh(SELF, buff="EX1_393e")


EX1_393e = buff(atk=3)


class EX1_412:
	"""Raging Worgen"""
	enrage = Refresh(SELF, buff="EX1_412e")


class EX1_412e:
	tags = {GameTag.ATK: +1}
	windfury = SET(1)


class EX1_506:
	"""Murloc Tidehunter"""
	play = Summon(CONTROLLER, "EX1_506a")


class EX1_556:
	"""Harvest Golem"""
	deathrattle = Summon(CONTROLLER, "skele21")


class EX1_583:
	"""Priestess of Elune"""
	play = Heal(FRIENDLY_HERO, 4)


class NEW1_018:
	"""Bloodsail Raider"""
	play = Find(FRIENDLY_WEAPON) & Buff(SELF, "NEW1_018e", atk=ATK(FRIENDLY_WEAPON))


class NEW1_022:
	"""Dread Corsair"""
	cost_mod = -ATK(FRIENDLY_WEAPON)


class tt_004:
	"""Flesheating Ghoul"""
	events = Death(MINION).on(Buff(SELF, "tt_004o"))


tt_004o = buff(atk=1)


##
# Unused buffs

# Full Strength (Injured Blademaster)
CS2_181e = buff(atk=2)
