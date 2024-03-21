from ..utils import *


##
# Minions

class ULD_158:
	"""Sandstorm Elemental"""
	# <b>Battlecry:</b> Deal 1 damage to all enemy minions. <b>Overload:</b> (1)
	play = Heal(ENEMY_MINIONS, 1)


class ULD_169:
	"""Mogu Fleshshaper"""
	# [x]<b>Rush</b>. Costs (1) less for each minion on the battlefield.
	cost_mod = -Count(ALL_MINIONS)


class ULD_170:
	"""Weaponized Wasp"""
	# <b>Battlecry:</b> If you control a <b>Lackey</b>, deal 3_damage.
	requirements = {
		PlayReq.REQ_TARGET_IF_AVAILABLE_AND_FRIENDLY_LACKEY: 0,
	}
	play = Hit(TARGET, 3)


class ULD_173:
	"""Vessina"""
	# While you're <b>Overloaded</b>, your other minions have +2 Attack.
	update = OVERLOADED(CONTROLLER) & Refresh(FRIENDLY_MINIONS - SELF, {GameTag.ATK: 2})


class ULD_276:
	"""EVIL Totem"""
	# At the end of your turn, add a <b>Lackey</b> to your hand.
	events = OWN_TURN_END.on(Give(CONTROLLER, RandomLackey()))


##
# Spells

class ULD_171:
	"""Totemic Surge"""
	# Give your Totems +2_Attack.
	play = Buff(FRIENDLY_MINIONS + TOTEM, "ULD_171e")


ULD_171e = buff(atk=2)


class ULD_172:
	"""Plague of Murlocs"""
	# Transform all minions into random Murlocs.
	play = Morph(ALL_MINIONS, RandomMurloc())


class ULD_181:
	"""Earthquake"""
	# Deal $5 damage to all minions, then deal $2 damage to all minions.
	play = Hit(ALL_MINIONS, 5), Hit(ALL_MINIONS, 2)


class ULD_291:
	"""Corrupt the Waters"""
	# [x]<b>Quest:</b> Play 6 <b>Battlecry</b> cards. <b>Reward:</b> Heart of Vir'naal.
	progress_total = 6
	quest = Play(CONTROLLER, BATTLECRY).after(AddProgress(SELF, Play.CARD))
	reward = Summon(CONTROLLER, "ULD_291p")


class ULD_291p:
	"""Heart of Vir'naal"""
	# <b>Hero Power</b> Your <b>Battlecries</b> trigger twice this turn.
	activate = Buff(CONTROLLER, "ULD_291pe")


class ULD_291pe:
	tags = {enums.EXTRA_BATTLECRIES: True}


##
# Weapons

class ULD_413:
	"""Splitting Axe"""
	# <b>Battlecry:</b> Summon copies of your Totems.
	play = Summon(CONTROLLER, ExactCopy(FRIENDLY_MINIONS + TOTEM))
