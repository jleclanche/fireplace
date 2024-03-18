from ..utils import *


##
# Minions

class LOOT_069:
	"""Sewer Crawler"""
	# <b>Battlecry:</b> Summon a 2/3_Giant Rat.
	requirements = {
		PlayReq.REQ_MINION_TARGET: 0,
	}
	play = Summon(CONTROLLER, "LOOT_069t")


class LOOT_122:
	"""Corrosive Sludge"""
	# <b>Battlecry:</b> Destroy your opponent's weapon.
	play = Destroy(ENEMY_WEAPON)


class LOOT_131:
	"""Green Jelly"""
	# At the end of your turn, summon a 1/2 Ooze with_<b>Taunt</b>.
	events = OWN_TURN_END.on(Summon(CONTROLLER, "LOOT_131t1"))


class LOOT_132:
	"""Dragonslayer"""
	# <b>Battlecry:</b> Deal 6 damage to a Dragon.
	requirements = {
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
		PlayReq.REQ_TARGET_WITH_RACE: 24,
	}
	play = Hit(TARGET, 6)


class LOOT_134:
	"""Toothy Chest"""
	# At the start of your turn, set this minion's Attack to 4.
	events = OWN_TURN_BEGIN.on(Buff(SELF, "LOOT_134e"))


class LOOT_134e:
	atk = SET(4)


class LOOT_136:
	"""Sneaky Devil"""
	# <b>Stealth</b> Your other minions have +1 Attack.
	update = Refresh(FRIENDLY_MINIONS - SELF, buff="LOOT_136e")


LOOT_136e = buff(atk=1)


class LOOT_144:
	"""Hoarding Dragon"""
	# <b>Deathrattle:</b> Give your opponent two Coins.
	deathrattle = Give(OPPONENT, THE_COIN) * 2


class LOOT_152:
	"""Boisterous Bard"""
	# <b>Battlecry:</b> Give your other minions +1 Health.
	play = Buff(FRIENDLY_MINIONS - SELF, "LOOT_152e")


LOOT_152e = buff(health=1)


class LOOT_153:
	"""Violet Wurm"""
	# <b>Deathrattle:</b> Summon seven 1/1 Grubs.
	deathrattle = Summon(CONTROLLER, "LOOT_153t1") * 7


class LOOT_167:
	"""Fungalmancer"""
	# <b>Battlecry:</b> Give adjacent minions +2/+2.
	play = Buff(SELF_ADJACENT, "LOOT_167e")


LOOT_167e = buff(+2, +2)


class LOOT_184:
	"""Silver Vanguard"""
	# <b>Deathrattle:</b> <b>Recruit</b> an 8-Cost minion.
	deathrattle = Recruit(COST == 8)


class LOOT_233:
	"""Cursed Disciple"""
	# <b>Deathrattle:</b> Summon a 5/1 Revenant.
	deathrattle = Summon(CONTROLLER, "LOOT_233t")


class LOOT_291:
	"""Shroom Brewer"""
	# <b>Battlecry:</b> Restore 4_Health.
	requirements = {
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
	}
	play = Heal(TARGET, 4)


class LOOT_347:
	"""Kobold Apprentice"""
	# <b>Battlecry:</b> Deal 3 damage randomly split among all_enemies.
	play = Hit(RANDOM_ENEMY_MINION, 1) * 3


class LOOT_375:
	"""Guild Recruiter"""
	# <b>Battlecry:</b> <b>Recruit</b> a minion that costs (4) or less.
	play = Recruit(COST <= 4)


class LOOT_388:
	"""Fungal Enchanter"""
	# <b>Battlecry:</b> Restore 2 Health to all friendly characters.
	play = Heal(FRIENDLY_CHARACTERS, 2)


class LOOT_413:
	"""Plated Beetle"""
	# <b>Deathrattle:</b> Gain 3 Armor.
	deathrattle = GainArmor(FRIENDLY_HERO, 3)
