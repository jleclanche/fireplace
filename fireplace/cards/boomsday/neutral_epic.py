from ..utils import *


##
# Minions

class BOT_280:
	"""Holomancer"""
	# After your opponent plays a minion, summon a 1/1_copy of it.
	events = Play(OPPONENT, MINION).after(
		Summon(CONTROLLER, Buff(ExactCopy(Play.CARD), "BOT_280e"))
	)


class BOT_280e:
	atk = SET(1)
	max_health = SET(1)


class BOT_296:
	"""Omega Defender"""
	# [x]<b>Taunt</b> <b>Battlecry:</b> If you have 10 Mana Crystals, gain +10 Attack.
	play = AT_MAX_MANA(CONTROLLER) & Buff(SELF, "BOT_296e")


BOT_296e = buff(atk=10)


class BOT_401:
	"""Weaponized Piñata"""
	# <b>Deathrattle:</b> Add a random <b>Legendary</b> minion to your_hand.
	deathrattle = Give(CONTROLLER, RandomLegendaryMinion())


class BOT_447:
	"""Crystallizer"""
	# [x]<b>Battlecry:</b> Deal 5 damage to your hero. Gain 5 Armor.
	play = Hit(FRIENDLY_HERO, 5), GainArmor(FRIENDLY_HERO, 5)


class BOT_511:
	"""Seaforium Bomber"""
	# [x]<b>Battlecry:</b> Shuffle a Bomb into your opponent's deck. When drawn, it
	# explodes for 5 damage.
	play = Shuffle(OPPONENT, "BOT_511t")


class BOT_511t:
	play = Hit(FRIENDLY_HERO, 5)
	draw = CAST_WHEN_DRAWN


class BOT_540:
	"""E.M.P. Operative"""
	# <b>Battlecry:</b> Destroy a Mech.
	requirements = {
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
		PlayReq.REQ_TARGET_WITH_RACE: 17,
		PlayReq.REQ_MINION_TARGET: 0,
	}
	play = Destroy(TARGET)


class BOT_544:
	"""Loose Specimen"""
	# <b>Battlecry:</b> Deal 6 damage randomly split among other friendly minions.
	play = Hit(RANDOM_FRIENDLY_MINION, 1) * 6


class BOT_552:
	"""Star Aligner"""
	# [x]<b>Battlecry:</b> If you control 3 minions with 7 Health, deal 7 damage to all
	# enemies.
	play = (Count(FRIENDLY_MINIONS + (CURRENT_HEALTH == 7)) >= 3) & Hit(ENEMY_CHARACTERS, 7)


class BOT_559:
	"""Augmented Elekk"""
	# Whenever you shuffle a card into a deck, shuffle in_an extra copy.
	events = Shuffle(source=FRIENDLY - ID("BOT_559")).after(
		Shuffle(CONTROLLER, ExactCopy(Shuffle.CARD))
	)
