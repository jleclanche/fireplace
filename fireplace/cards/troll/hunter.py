from ..utils import *


##
# Minions

class TRL_348:
	"""Springpaw"""
	# [x]<b>Rush</b> <b>Battlecry:</b> Add a 1/1 Lynx with <b>Rush</b> to your hand.
	play = Give(CONTROLLER, "TRL_348t")


class TRL_349:
	"""Bloodscalp Strategist"""
	# <b>Battlecry:</b> If you have a weapon equipped, <b>Discover</b> a spell.
	play = Find(FRIENDLY_WEAPON) & DISCOVER(RandomSpell())


class TRL_900:
	"""Halazzi, the Lynx"""
	# <b>Battlecry:</b> Fill your hand with 1/1 Lynxes that have_<b>Rush</b>.
	play = Give(CONTROLLER, "TRL_348t") * (
		MAX_HAND_SIZE(CONTROLLER) - Count(FRIENDLY_HAND)
	)


class TRL_901:
	"""Spirit of the Lynx"""
	# [x]<b>Stealth</b> for 1 turn. Whenever you summon a Beast, give it +1/+1.
	events = (
		OWN_TURN_BEGIN.on(Unstealth(SELF)),
		Summon(CONTROLLER, BEAST).on(Buff(Summon.CARD, "TRL_901e"))
	)


TRL_901e = buff(+1, +1)


##
# Spells

class TRL_119:
	"""The Beast Within"""
	# Give a friendly Beast +1/+1, then it attacks a random enemy minion.
	play = Buff(TARGET, "TRL_119e").then(Attack(TARGET, RANDOM(ENEMY_MINIONS)))


TRL_119e = buff(+1, +1)


class TRL_339:
	"""Master's Call"""
	# <b>Discover</b> a minion in your deck. If all 3 are Beasts, draw them all.
	# TODO need test
	def play(self):
		entities = (RANDOM(DeDuplicate(FRIENDLY_DECK + BEAST)) * 3).eval(self.game, self)
		if all(Race.BEAST in entity.races for entity in entities):
			yield Give(CONTROLLER, entities)
		else:
			yield GenericChoice(CONTROLLER, entities)


class TRL_347:
	"""Baited Arrow"""
	# Deal $3 damage. <b>Overkill:</b> Summon a 5/5 Devilsaur.
	play = Hit(TARGET, 3)
	overkill = Summon(CONTROLLER, "TRL_347t")


class TRL_566:
	"""Revenge of the Wild"""
	# Summon your Beasts that died this turn.
	play = Summon(CONTROLLER, Copy(FRIENDLY + BEAST + KILLED_THIS_TURN))


##
# Weapons

class TRL_111:
	"""Headhunter's Hatchet"""
	# [x]<b>Battlecry:</b> If you control a Beast, gain +1 Durability.
	play = Find(FRIENDLY_MINIONS + BEAST) & Buff(SELF, "TRL_111e")


TRL_111e = buff(health=1)


##
# Heros

class TRL_065:
	"""Zul'jin"""
	# [x]<b>Battlecry:</b> Cast all spells you've played this game <i>(targets chosen
	# randomly)</i>.
	play = CastSpell(CARDS_PLAYED_THIS_GAME + SPELL)


class TRL_065h:
	activate = Hit(TARGET, 2)
