from ..utils import *


##
# Minions

class OG_303:
	"""Cult Sorcerer"""
	events = OWN_SPELL_PLAY.after(Buff(CTHUN, "OG_303e"))


OG_303e = buff(+1, +1)


class OG_083:
	"""Twilight Flamecaller"""
	play = Hit(ENEMY_MINIONS, 1)


class OG_085:
	"""Demented Frostcaller"""
	events = OWN_SPELL_PLAY.after(Freeze(RANDOM(ENEMY_CHARACTERS - MORTALLY_WOUNDED - FROZEN)))


class OG_120:
	"""Anomalus"""
	deathrattle = Hit(ALL_MINIONS, 8)


class OG_207:
	"""Faceless Summoner"""
	play = Summon(CONTROLLER, RandomMinion(cost=3))


class OG_087:
    """Servant of Yogg-Saron"""
    play = CastSpell(RandomSpell(id="DS1_184"))


##
# Spells

class OG_081:
	"""Shatter"""
	play = Destroy(TARGET)


class OG_090:
	"""Cabalist's Tome"""
	play = Give(CONTROLLER, RandomSpell(card_class=CardClass.MAGE)) * 3


class OG_086:
	"""Forbidden Flame"""
	def play(self):
		mana = self.controller.mana
		yield SpendMana(CONTROLLER, mana)
		yield Hit(TARGET, mana)
