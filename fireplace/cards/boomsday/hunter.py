from ..utils import *


##
# Minions

class BOT_034:
	"""Boommaster Flark"""
	# <b>Battlecry:</b> Summon four 0/2 Goblin Bombs.
	play = SummonBothSides(CONTROLLER, "BOT_031") * 4


class BOT_035:
	"""Venomizer"""
	# <b>Magnetic</b> <b>Poisonous</b>
	magnetic = MAGNETIC("BOT_035e")


BOT_035e = buff(poisonous=True)


class BOT_038:
	"""Fireworks Tech"""
	# [x]<b>Battlecry:</b> Give a friendly Mech +1/+1. If it has <b>Deathrattle</b>,
	# trigger it.
	requirements = {
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_WITH_RACE: 17,
	}
	play = (
		Buff(TARGET, "BOT_038e"),
		Find(TARGET + DEATHRATTLE) & Deathrattle(TARGET)
	)


BOT_038e = buff(+1, +1)


class BOT_039:
	"""Necromechanic"""
	# Your <b>Deathrattles</b> trigger twice.
	update = Refresh(CONTROLLER, {GameTag.EXTRA_DEATHRATTLES: True})


class BOT_251:
	"""Spider Bomb"""
	# <b>Magnetic</b> <b>Deathrattle:</b> Destroy a random_enemy_minion.
	magnetic = MAGNETIC("BOT_251e")
	deathrattle = Destroy(RANDOM(ENEMY_MINIONS))


class BOT_251e:
	tags = {GameTag.DEATHRATTLE: True}
	deathrattle = Destroy(RANDOM(ENEMY_MINIONS))


##
# Spells

class BOT_033:
	"""Bomb Toss"""
	# Deal $2 damage. Summon a 0/2 Goblin_Bomb.
	requirements = {
		PlayReq.REQ_TARGET_TO_PLAY: 0,
	}
	play = Hit(TARGET, 2), Summon(CONTROLLER, "BOT_031")


class BOT_402:
	"""Secret Plan"""
	# <b>Discover</b> a <b>Secret</b>.
	play = WITH_SECRECTS & (
		DISCOVER(RandomSpell(secret=True))
	) | (
		DISCOVER(RandomSpell(secret=True, card_class=CardClass.HUNTER))
	)


class BOT_429:
	"""Flark's Boom-Zooka"""
	# [x]Summon 3 minions from your deck. They attack enemy minions, then die.
	requirements = {
		PlayReq.REQ_NUM_MINION_SLOTS: 1,
	}
	play = Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION)).then(
		Attack(Summon.CARD, RANDOM_ENEMY_MINION),
		Destroy(Summon.CARD)
	) * 3


class BOT_437:
	"""Goblin Prank"""
	# Give a friendly minion +3/+3 and <b>Rush</b>. It_dies at end of turn.
	requirements = {
		PlayReq.REQ_TARGET_TO_PLAY: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_FRIENDLY_TARGET: 0,
	}
	play = Buff(TARGET, "BOT_437e")


class BOT_437e:
	tags = {
		GameTag.ATK: 3,
		GameTag.HEALTH: 3,
		GameTag.RUSH: True,
	}
	events = OWN_TURN_END.on(Destroy(OWNER))


class BOT_438:
	"""Cybertech Chip"""
	# Give your minions "<b>Deathrattle:</b> Add a random Mech to your_hand."
	play = Buff(FRIENDLY_MINIONS, "BOT_438e")


class BOT_438e:
	tags = {GameTag.DEATHRATTLE: True}
	deathrattle = Give(CONTROLLER, RandomMech())
