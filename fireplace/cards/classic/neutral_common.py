from ..utils import *


##
# Free basic minions

# Raid Leader
class CS2_122:
	update = Refresh(FRIENDLY_MINIONS - SELF, buff="CS2_122e")


# Stormwind Champion
class CS2_222:
	update = Refresh(FRIENDLY_MINIONS - SELF, buff="CS2_222o")


# Frostwolf Warlord
class CS2_226:
	play = Buff(SELF, "CS2_226e") * Count(FRIENDLY_MINIONS)


# Voodoo Doctor
class EX1_011:
	play = Heal(TARGET, 2)


# Novice Engineer
class EX1_015:
	play = Draw(CONTROLLER)


# Mad Bomber
class EX1_082:
	play = Hit(RANDOM_CHARACTER, 1) * 3


# Demolisher
class EX1_102:
	events = OWN_TURN_BEGIN.on(Hit(RANDOM_ENEMY_CHARACTER, 2))


# Dire Wolf Alpha
class EX1_162:
	update = Refresh(SELF_ADJACENT, buff="EX1_162o")


# Arathi Weaponsmith
class EX1_398:
	play = Summon(CONTROLLER, "EX1_398t")


# Gurubashi Berserker
class EX1_399:
	events = SELF_DAMAGE.on(Buff(SELF, "EX1_399e"))


# Grimscale Oracle
class EX1_508:
	update = Refresh(ALL_MINIONS + MURLOC - SELF, buff="EX1_508o")


# Nightblade
class EX1_593:
	play = Hit(ENEMY_HERO, 3)


# Cult Master
class EX1_595:
	events = Death(FRIENDLY + MINION).on(Draw(CONTROLLER))


##
# Common basic minions

# Earthen Ring Farseer
class CS2_117:
	play = Heal(TARGET, 3)


# Ironforge Rifleman
class CS2_141:
	play = Hit(TARGET, 1)


# Southsea Deckhand
class CS2_146:
	update = Find(FRIENDLY_WEAPON) & Refresh(SELF, {GameTag.CHARGE: True})


# Gnomish Inventor
class CS2_147:
	play = Draw(CONTROLLER)


# Stormpike Commando
class CS2_150:
	play = Hit(TARGET, 2)


# Silver Hand Knight
class CS2_151:
	play = Summon(CONTROLLER, "CS2_152")


# Elven Archer
class CS2_189:
	play = Hit(TARGET, 1)


# Abusive Sergeant
class CS2_188:
	play = Buff(TARGET, "CS2_188o")


# Razorfen Hunter
class CS2_196:
	play = Summon(CONTROLLER, "CS2_boar")


# Ironbeak Owl
class CS2_203:
	play = Silence(TARGET)


# Spiteful Smith
class CS2_221:
	enrage = Refresh(FRIENDLY_WEAPON, buff="CS2_221e")


# Venture Co. Mercenary
class CS2_227:
	update = Refresh(FRIENDLY + MINION + IN_HAND, {GameTag.COST: +3})


# Darkscale Healer
class DS1_055:
	play = Heal(FRIENDLY_CHARACTERS, 2)


# Acolyte of Pain
class EX1_007:
	events = SELF_DAMAGE.on(Draw(CONTROLLER))


# Shattered Sun Cleric
class EX1_019:
	play = Buff(TARGET, "EX1_019e")


# Dragonling Mechanic
class EX1_025:
	play = Summon(CONTROLLER, "EX1_025t")


# Leper Gnome
class EX1_029:
	deathrattle = Hit(ENEMY_HERO, 2)


# Dark Iron Dwarf
class EX1_046:
	play = Buff(TARGET, "EX1_046e")


# Spellbreaker
class EX1_048:
	play = Silence(TARGET)


# Youthful Brewmaster
class EX1_049:
	play = Bounce(TARGET)


# Ancient Brewmaster
class EX1_057:
	play = Bounce(TARGET)


# Acidic Swamp Ooze
class EX1_066:
	play = Destroy(ENEMY_WEAPON)


# Loot Hoarder
class EX1_096:
	deathrattle = Draw(CONTROLLER)


# Frost Elemental
class EX1_283:
	play = Freeze(TARGET)


# Tauren Warrior
class EX1_390:
	enrage = Refresh(SELF, {GameTag.ATK: +3})


# Amani Berserker
class EX1_393:
	enrage = Refresh(SELF, {GameTag.ATK: +3})


# Raging Worgen
class EX1_412:
	enrage = Refresh(SELF, {GameTag.ATK: +1, GameTag.WINDFURY: True})


# Murloc Tidehunter
class EX1_506:
	play = Summon(CONTROLLER, "EX1_506a")


# Harvest Golem
class EX1_556:
	deathrattle = Summon(CONTROLLER, "skele21")


# Priestess of Elune
class EX1_583:
	play = Heal(FRIENDLY_HERO, 4)


# Bloodsail Raider
class NEW1_018:
	play = Find(FRIENDLY_WEAPON) & Buff(SELF, "NEW1_018e", atk=Attr(FRIENDLY_WEAPON, GameTag.ATK))


# Dread Corsair
class NEW1_022:
	cost_mod = -Attr(FRIENDLY_WEAPON, GameTag.ATK)


# Flesheating Ghoul
class tt_004:
	events = Death(MINION).on(Buff(SELF, "tt_004o"))
