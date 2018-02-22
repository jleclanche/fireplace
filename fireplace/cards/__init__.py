import os
from pkg_resources import resource_filename
from hearthstone import cardxml
from hearthstone.enums import CardType, GameTag
from ..logging import log
from ..rules import POISONOUS, LIFESTEAL
from ..utils import get_script_definition


class CardDB(dict):
	def __init__(self):
		self.initialized = False

	@staticmethod
	def setup_zone_script_defaults(card, zone_name):
		if not hasattr(card.scripts, zone_name):
			setattr(card.scripts, zone_name, type(zone_name, (), {}))

		zone = getattr(card.scripts, zone_name)

		if not hasattr(zone, "events"):
			zone.events = []

		if not hasattr(zone.events, "__iter__"):
			zone.events = [zone.events]

		if not hasattr(zone, "update"):
			zone.update = ()

		if not hasattr(zone.update, "__iter__"):
			zone.update = (zone.update, )



	@staticmethod
	def merge(id, card, cardscript=None):
		"""
		Find the xmlcard and the card definition of \a id
		Then return a merged class of the two
		"""
		if card is None:
			card = cardxml.CardXML(id)

		if cardscript is None:
			cardscript = get_script_definition(id)

		if cardscript:
			card.scripts = type(id, (cardscript, ), {})
		else:
			card.scripts = type(id, (), {})

		scriptnames = (
			"activate", "combo", "deathrattle", "draw", "inspire", "play",
			"enrage", "update", "powered_up", "reward"
		)

		for script in scriptnames:
			actions = getattr(card.scripts, script, None)
			if actions is None:
				# Set the action by default to avoid runtime hasattr() calls
				setattr(card.scripts, script, [])
			elif not callable(actions):
				if not hasattr(actions, "__iter__"):
					# Ensure the actions are always iterable
					setattr(card.scripts, script, (actions, ))

		for script in ("events", "secret", "quest"):
			events = getattr(card.scripts, script, None)
			if events is None:
				setattr(card.scripts, script, [])
			elif not hasattr(events, "__iter__"):
				setattr(card.scripts, script, [events])

		if not hasattr(card.scripts, "cost_mod"):
			card.scripts.cost_mod = None

		#Setup Hand defaults
		CardDB.setup_zone_script_defaults(card, "Hand")
		#Setup Deck defaults
		CardDB.setup_zone_script_defaults(card, "Deck")
		#Setup Discard defaults
		CardDB.setup_zone_script_defaults(card, "Discard")

		# Set choose one cards
		if hasattr(cardscript, "choose"):
			card.choose_cards = cardscript.choose[:]
		else:
			card.choose_cards = []

		if hasattr(cardscript, "tags"):
			for tag, value in cardscript.tags.items():
				card.tags[tag] = value

		# Set some additional events based on the base tags...
		if card.poisonous:
			card.scripts.events.append(POISONOUS)

		if GameTag.LIFESTEAL in card.tags:  # fix until replaced in python-hearthstone. then: if card.lifesteal
			card.scripts.events.append(LIFESTEAL)

		return card

	def initialize(self):
		log.info("Initializing card database")
		self.initialized = True
		db, xml = cardxml.load()
		for id, card in db.items():
			self[id] = self.merge(id, card)

		log.info("Merged %i cards", len(self))

	def filter(self, **kwargs):
		"""
		Returns a list of card IDs matching the given filters. Each filter, if not
		None, is matched against the registered card database.
		cards.
		Examples arguments:
		\a collectible: Whether the card is collectible or not.
		\a type: The type of the card (hearthstone.enums.CardType)
		\a race: The race (tribe) of the card (hearthstone.enums.Race)
		\a rarity: The rarity of the card (hearthstone.enums.Rarity)
		\a cost: The mana cost of the card
		"""
		if not self.initialized:
			self.initialize()

		cards = self.values()

		if "type" not in kwargs:
			kwargs["type"] = [CardType.SPELL, CardType.WEAPON, CardType.MINION]

		for attr, value in kwargs.items():
			if value is not None:
				# What? this doesn't work?
				# cards = __builtins__["filter"](lambda c: getattr(c, attr) == value, cards)
				cards = [
					card for card in cards if (isinstance(value, list) and getattr(card, attr) in value) or
					getattr(card, attr) == value
				]

		return [card.id for card in cards]


# Here we import every card from every set and load the cardxml database.
# For every card, we will "merge" the class with its Python definition if
# it exists.
if "db" not in globals():
	db = CardDB()
	filter = db.filter
