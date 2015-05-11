import logging
import os
from pkg_resources import Requirement, resource_filename
from .blackrock import *
from .game import *
from .classic import *
from .debug import *
from .gvg import *
from .naxxramas import *
from .. import cardxml


def merge(id):
	"""
	Find the xmlcard and the card definition of \a id
	Then return a merged class of the two
	"""
	card = db[id]
	carddef = globals().get(id)
	if not carddef:
		cls = type(id, (), {})
	else:
		if hasattr(carddef, "scripts"):
			# This basically means the card has already been merged...
			return card
		cls = type(id, (carddef, ), {})
	card.scripts = cls
	return card


def filter(**kwargs):
	"""
	Returns a list of card IDs matching the given filters. Each filter, if not
	None, is matched against the registered card database.
	cards.
	\a collectible: Whether the card is collectible or not.
	\a type: The type of the card (fireplace.enums.CardType)
	\a race: The race (tribe) of the card (fireplace.enums.Race)
	\a rarity: The rarity of the card (fireplace.enums.Rarity)
	\a cost: The mana cost of the card
	"""
	cards = db.values()

	for attr, value in kwargs.items():
		if value is not None:
			# What? this doesn't work?
			# cards = __builtins__["filter"](lambda c: getattr(c, attr) == value, cards)
			cards = [card for card in cards if getattr(card, attr) == value]

	return [card.id for card in cards]


# Here we import every card from every set and load the cardxml database.
# For every card, we will "merge" the class with its Python definition if
# it exists.
# This code is only ran once, at initial import.

if "cardlist" not in globals():
	xmlfile = resource_filename(__name__, "enUS.xml")
	if not os.path.exists(xmlfile):
		raise RuntimeError("%r does not exist - generate it!" % (xmlfile))

	with open(xmlfile, "r") as f:
		db, xml = cardxml.load(xmlfile)
		cardlist = []
		for id in db:
			globals()[id] = merge(id)
			cardlist.append(id)
