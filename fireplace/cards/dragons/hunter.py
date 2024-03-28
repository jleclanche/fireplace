from ..utils import *


##
# Minions

class DRG_010:
	"""Diving Gryphon"""
	# <b>Rush</b> <b>Battlecry:</b> Draw a <b>Rush</b> minion_from_your_deck.
	play = ForceDraw(RANDOM(FRIENDLY_DECK + MINION + RUSH))


class DRG_095:
	"""Veranus"""
	# <b>Battlecry:</b> Change the Health of all enemy minions to 1.
	play = Buff(ENEMY_MINIONS, "DRG_095e")


class DRG_095e:
	max_health = SET(1)


class DRG_252:
	"""Phase Stalker"""
	# [x]After you use your Hero Power, cast a <b>Secret</b> from your deck.
	events = Activate(CONTROLLER, FRIENDLY_HERO_POWER).after(
		Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + SECRET))
	)


class DRG_253:
	"""Dwarven Sharpshooter"""
	# Your Hero Power can target_minions.
	# TODO need test
	update = Refresh(FRIENDLY_HERO_POWER, {GameTag.STEADY_SHOT_CAN_TARGET: True})


class DRG_254:
	"""Primordial Explorer"""
	# <b>Poisonous</b> <b>Battlecry:</b> <b>Discover</b> a Dragon.
	play = DISCOVER(RandomDragon())


class DRG_256:
	"""Dragonbane"""
	# After you use your Hero Power, deal 5 damage to a random enemy.
	events = Activate(CONTROLLER, FRIENDLY_HERO_POWER).after(
		Hit(ENEMY_HERO, 5)
	)


##
# Spells

class DRG_006:
	"""Corrosive Breath"""
	# [x]Deal $3 damage to a minion. If you're holding a Dragon, it also hits the enemy
	# hero.
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	powered_up = HOLDING_DRAGON
	play = Hit(TARGET, 3), powered_up & Hit(ENEMY_HERO, 3)


class DRG_251:
	"""Clear the Way"""
	# [x]<b>Sidequest:</b> Summon 3 <b>Rush</b> minions. <b>Reward:</b> Summon a 4/4
	# Gryphon with <b>Rush</b>.
	progress_total = 3
	sidequest = Summon(CONTROLLER, RUSH + MINION).after(AddProgress(SELF, Summon.CARD))
	reward = Summon(CONTROLLER, "DRG_251t")


class DRG_255:
	"""Toxic Reinforcements"""
	# [x]<b>Sidequest:</b> Use your Hero Power three times. <b>Reward:</b> Summon three 1/1
	# Leper Gnomes.
	progress_total = 3
	sidequest = Activate(CONTROLLER, FRIENDLY_HERO_POWER).after(
		AddProgress(SELF, FRIENDLY_HERO_POWER))
	reward = Summon(CONTROLLER, "DRG_251t")


##
# Weapons

class DRG_007:
	"""Stormhammer"""
	# Doesn't lose Durability while you control a_Dragon.
	update = Find(FRIENDLY_MINIONS + DRAGON) & Refresh(SELF, buff="DRG_007e")


DRG_007e = buff(immune=True)
