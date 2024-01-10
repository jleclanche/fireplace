from ..utils import *


##
# Minions

class GIL_508:
	"""Duskbat"""
	# <b>Battlecry:</b> If your hero took damage this turn, summon two 1/1 Bats.
	powered_up = DAMAGED_THIS_TURN(FRIENDLY_HERO) >= 0
	play = powered_up & SummonBothSides(CONTROLLER, "GIL_508t")


class GIL_515:
	"""Ratcatcher"""
	# <b>Rush</b> <b>Battlecry:</b> Destroy a friendly minion and gain its Attack and
	# Health.
	play = (
		Buff(SELF, "GIL_515e", atk=ATK(TARGET), max_health=CURRENT_HEALTH(TARGET)),
		Destroy(TARGET)
	)


class GIL_565:
	"""Deathweb Spider"""
	# <b>Battlecry:</b> If your hero took damage this turn, gain <b>Lifesteal</b>.
	powered_up = DAMAGED_THIS_TURN(FRIENDLY_HERO) >= 0
	play = powered_up & GiveLifesteal(SELF)


class GIL_608:
	"""Witchwood Imp"""
	# [x]<b>Stealth</b> <b>Deathrattle:</b> Give a random friendly minion +2 Health.
	deathrattle = Buff(RANDOM_OTHER_FRIENDLY_MINION, "GIL_608e")


GIL_608e = buff(health=2)


class GIL_618:
	"""Glinda Crowskin"""
	# Minions in your hand have_<b>Echo</b>.
	update = Refresh(FRIENDLY_HAND + MINION, {GameTag.ECHO: True})


class GIL_693:
	"""Blood Witch"""
	# At the start of your turn, deal 1 damage to your_hero.
	events = OWN_TURN_BEGIN.on(Hit(FRIENDLY_HERO, 1))


class GIL_825:
	"""Lord Godfrey"""
	# [x]<b>Battlecry:</b> Deal 2 damage to all other minions. If any die, repeat this
	# <b>Battlecry</b>.
	progress_total = 14
	play = Hit(ALL_MINIONS - SELF, 2), Dead(ALL_MINIONS) & (
		Deaths(),
		AddProgress(SELF, None),
		FINISH_PROGRESS | ExtraBattlecry(SELF, None)
	)


##
# Spells

class GIL_191:
	"""Fiendish Circle"""
	# [x]Summon four 1/1 Imps.
	play = Summon(CONTROLLER, "GIL_191t") * 4


class GIL_543:
	"""Dark Possession"""
	# Deal $2 damage to a friendly character. <b>Discover</b> a Demon.
	play = Hit(TARGET, 2), DISCOVER(RandomDemon())


class GIL_665:
	"""Curse of Weakness"""
	# <b>Echo</b> Give all enemy minions -2_Attack until your next_turn.
	play = Buff(ENEMY_MINIONS, "GIL_665e")


class GIL_665e:
	tags = {GameTag.ATK: -2}
	events = OWN_TURN_BEGIN.on(Destroy(SELF))
