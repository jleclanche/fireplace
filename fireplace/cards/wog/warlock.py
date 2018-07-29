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
			(CardClass.DRUID, "CS2_017"),
			(CardClass.HUNTER, "DS1h_292"),
			(CardClass.MAGE, "CS2_034"),
			(CardClass.PALADIN, "CS2_101"),
			(CardClass.PRIEST, "CS1h_001"),
			(CardClass.ROGUE, "CS2_083b"),
			(CardClass.SHAMAN, "CS2_049"),
			(CardClass.WARRIOR, "CS2_102")
		]
		hero_class, hero_power = random.choice(classes)
		yield Summon(CONTROLLER, hero_power)
		yield Morph(
			FRIENDLY + (IN_DECK | IN_HAND) + WARLOCK,
			RandomCollectible(card_class = hero_class)
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
