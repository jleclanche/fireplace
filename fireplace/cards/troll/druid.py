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
	events = Attack(FRIENDLY_HERO, ALL_MINIONS).after(
		Dead(ALL_MINIONS + Attack.DEFENDER) & ExtraAttack(SELF)
	)


class TRL_341:
	"""Treespeaker"""
	# <b>Battlecry:</b> Transform your Treants into 5/5 Ancients.
	play = Morph(FRIENDLY_MINIONS + TREANT, "TRL_341t")


class TRL_343:
	"""Wardruid Loti"""
	# <b>Choose One - </b>Transform into one of Loti's four dinosaur forms.
	choose = ("TRL_343at2", "TRL_343bt2", "TRL_343ct2", "TRL_343dt2")
	play = ChooseBoth(CONTROLLER) & Morph(SELF, "TRL_343et1")


class TRL_343at2:
	play = Morph(SELF, "TRL_343at1")


class TRL_343bt2:
	play = Morph(SELF, "TRL_343bt1")


class TRL_343ct2:
	play = Morph(SELF, "TRL_343ct1")


class TRL_343dt2:
	play = Morph(SELF, "TRL_343dt1")


##
# Spells

class TRL_243:
	"""Pounce"""
	# Give your hero +2_Attack this turn.
	play = Buff(FRIENDLY_HERO, "TRL_243e")


TRL_243e = buff(atk=2)


class TRL_244:
	"""Predatory Instincts"""
	# [x]Draw a Beast from your deck. Double its Health.
	play = ForceDraw(RANDOM(FRIENDLY_DECK + BEAST)).then(
		Buff(ForceDraw.TARGET, "TRL_244e", max_health=CURRENT_HEALTH(ForceDraw.TARGET))
	)


class TRL_254:
	"""Mark of the Loa"""
	# <b>Choose One</b> - Give a minion +2/+4 and <b>Taunt</b>; or Summon two 3/2 Raptors.
	choose = ("TRL_254a", "TRL_254b")
	play = ChooseBoth(CONTROLLER) & (
		Buff(TARGET, "TRL_254ae"),
		Summon(CONTROLLER, "TRL_254t") * 2
	)


class TRL_254a:
	play = Buff(TARGET, "TRL_254ae")


TRL_254ae = buff(+2, +4, taunt=True)


class TRL_254b:
	play = Summon(CONTROLLER, "TRL_254t") * 2


class TRL_255:
	"""Stampeding Roar"""
	# Summon a random Beast from your hand and give it <b>Rush</b>.
	play = Summon(CONTROLLER, RANDOM(FRIENDLY_HAND + BEAST)).then(
		Buff(Summon.CARD, "TRL_255e")
	)


TRL_255e = buff(rush=True)
