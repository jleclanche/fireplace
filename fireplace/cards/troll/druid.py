from ..utils import *


##
# Minions

class TRL_223:
	"""Spirit of the Raptor"""
	# [x]<b>Stealth</b> for 1 turn. After your hero attacks and __kills a minion, draw a
	# card.__
	events = (
		OWN_TURN_BEGIN.on(Unstealth(SELF)),
		Attack(FRIENDLY_HERO, ALL_MINIONS).after(
			Dead(ALL_MINIONS + Attack.DEFENDER) & Draw(CONTROLLER)
		)
	)


class TRL_232:
	"""Ironhide Direhorn"""
	# <b>Overkill:</b> Summon a 5/5_Ironhide Runt.
	overkill = Summon(CONTROLLER, "TRL_232t")


class TRL_240:
	"""Savage Striker"""
	# <b>Battlecry:</b> Deal damage to an enemy minion equal to your hero's Attack.
	play = Hit(TARGET, ATK(FRIENDLY_HERO))


class TRL_241:
	"""Gonk, the Raptor"""
	# After your hero attacks and_kills a minion, it may_attack again.
	pass


class TRL_341:
	"""Treespeaker"""
	# <b>Battlecry:</b> Transform your Treants into 5/5 Ancients.
	pass


class TRL_343:
	"""Wardruid Loti"""
	# <b>Choose One - </b>Transform into one of Loti's four dinosaur forms.
	pass


##
# Spells

class TRL_243:
	"""Pounce"""
	# Give your hero +2_Attack this turn.
	pass


class TRL_244:
	"""Predatory Instincts"""
	# [x]Draw a Beast from your deck. Double its Health.
	pass


class TRL_254:
	"""Mark of the Loa"""
	# <b>Choose One</b> - Give a minion +2/+4 and <b>Taunt</b>; or Summon two 3/2 Raptors.
	pass


class TRL_255:
	"""Stampeding Roar"""
	# Summon a random Beast from your hand and give it <b>Rush</b>.
	pass
