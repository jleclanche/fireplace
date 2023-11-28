from ..utils import *


##
# Minions

class OG_042:
	"""Y'Shaarj, Rage Unbound"""
	events = OWN_TURN_END.on(Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION)))


class OG_122:
	"""Mukla, Tyrant of the Vale"""
	play = Give(CONTROLLER, "EX1_014t") * 2


class OG_317:
	"""Deathwing, Dragonlord"""
	deathrattle = Summon(CONTROLLER, FRIENDLY_HAND + DRAGON)


class OG_318:
	"""Hogger, Doom of Elwynn"""
	events = SELF_DAMAGE.on(Summon(CONTROLLER, "OG_318t"))


class OG_338:
	"""Nat, the Darkfisher"""
	events = BeginTurn(OPPONENT).on(COINFLIP & Draw(OPPONENT))


class OG_123:
	"""Shifter Zerus"""
	class Hand:
		events = OWN_TURN_BEGIN.on(
			Morph(SELF, RandomMinion()).then(Buff(Morph.CARD, "OG_123e"))
		)


class OG_123e:
	class Hand:
		events = OWN_TURN_BEGIN.on(
			Morph(OWNER, RandomMinion()).then(Buff(Morph.CARD, "OG_123e"))
		)
	events = REMOVED_IN_PLAY


class OG_300:
	"""The Boogeymonster"""
	events = Attack(SELF, ALL_MINIONS).after(
		Dead(ALL_MINIONS + Attack.DEFENDER) & Buff(SELF, "OG_300e")
	)


OG_300e = buff(+2, +2)


class OG_133:
	"""N'Zoth, the Corruptor"""
	play = Summon(CONTROLLER, Copy(FRIENDLY + KILLED + MINION))


class OG_134:
	"""Yogg-Saron, Hope's End"""
	def play(self):
		times = TIMES_SPELL_PLAYED_THIS_GAME.evaluate(self)
		for _ in range(times):
			if self.dead or self.silenced or self.zone != Zone.PLAY:
				break
			self.game.main_power(self, (CastSpell(RandomSpell()), ), None)


class OG_280:
	"""C'Thun"""
	play = Hit(RANDOM_ENEMY_CHARACTER, 1) * ATK(SELF)


class OG_131:
	"""Twin Emperor Vek'lor"""
	play = CHECK_CTHUN & Summon(CONTROLLER, "OG_319")
