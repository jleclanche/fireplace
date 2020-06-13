from ..utils import *


##
# Minions

class OG_109:
	"""Darkshire Librarian"""
	play = Discard(RANDOM(FRIENDLY_HAND))
	deathrattle = Draw(CONTROLLER)


class OG_113:
	"""Darkshire Councilman"""
	events = Summon(MINION, CONTROLLER).on(Buff(SELF, "OG_113e"))


OG_113e = buff(atk=1)


class OG_121:
	"""Cho'gall"""
	play = Buff(CONTROLLER, "OG_121e")


class OG_121e:
	events = OWN_SPELL_PLAY.on(Destroy(SELF))
	update = Refresh(CONTROLLER, {GameTag.SPELLS_COST_HEALTH: True})


class OG_241:
	"""Possessed Villager"""
	deathrattle = Summon(CONTROLLER, "OG_241a")


class OG_302:
	"""Usher of Souls"""
	events = Death(FRIENDLY + MINION).on(Buff(CTHUN, "OG_281e", atk=1, max_health=1))


##
# Spells

class OG_116:
	"""Spreading Madness"""
	play = Hit(RANDOM_CHARACTER, 1) * 9


class OG_118:
	"""Renounce Darkness"""
	def play(self):
		import random
		classes = [
			(CardClass.DRUID, "HERO_06bp"),
			(CardClass.HUNTER, "HERO_05bp"),
			(CardClass.MAGE, "HERO_08bp"),
			(CardClass.PALADIN, "HERO_04bp"),
			(CardClass.PRIEST, "HERO_09bp"),
			(CardClass.ROGUE, "HERO_03bp"),
			(CardClass.SHAMAN, "HERO_02bp"),
			(CardClass.WARRIOR, "HERO_07bp")
		]
		hero_class, hero_power = random.choice(classes)
		yield Summon(CONTROLLER, hero_power)
		yield Morph(
			FRIENDLY + WARLOCK + (IN_HAND | IN_DECK),
			RandomCollectible(card_class=hero_class)
		).then(
			Buff(Morph.CARD, "OG_118e")
		)


class OG_118e:
	events = REMOVED_IN_PLAY
	tags = {GameTag.COST: -1}


class OG_239:
	"""DOOM!"""
	def play(self):
		minion_count = len(self.controller.field) + len(self.controller.opponent.field)
		yield Destroy(ALL_MINIONS)
		yield Draw(CONTROLLER) * minion_count


class OG_114:
	"""Forbidden Ritual"""
	def play(self):
		mana = self.controller.mana
		yield SpendMana(CONTROLLER, mana)
		yield Summon(CONTROLLER, "OG_114a") * mana
