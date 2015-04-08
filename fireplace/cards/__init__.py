import logging
import os
from pkg_resources import Requirement, resource_filename
from ..enums import CardType, GameTag
from .game import *
from .classic import *
from .debug import *
from .gvg import *
from .naxxramas import *
from .. import cardxml


def _initTags(carddef, cls):
	"""
	Iterate over the class attributes, mapping them to the tags dict
	Note that this only needs to be done once per class, hence why we
	do it here instead of in Card.__new__()
	"""
	for attr, value in carddef.__dict__.items():
		# GameTag.DAMAGE is unused and conflicts with the DAMAGE event
		if attr.isupper() and hasattr(GameTag, attr) and attr is not "DAMAGE":
			cls.tags[getattr(GameTag, attr)] = value


def merge(id):
	"""
	Find the xmlcard and the card definition of \a id
	Then return a merged class of the two
	"""
	xmlcard = db[id]
	carddef = globals().get(id)
	if not carddef:
		cls = type(id, (), {})
	else:
		if hasattr(carddef, "id"):
			# This basically means the card has already been merged...
			return carddef
		cls = type(id, (carddef, ), {})
	cls.tags = xmlcard.tags
	cls.enrageTags = xmlcard.enrageTags
	if carddef:
		if hasattr(carddef, "Enrage"):
			# Initialize the Enrage virtual card too
			carddef.Enrage.tags = {}
			_initTags(carddef.Enrage, carddef.Enrage)
		_initTags(carddef, cls)
	cls.requirements = xmlcard.requirements
	cls.powerUpRequirements = xmlcard.powerUpRequirements
	cls.entourage = xmlcard.entourage
	cls.chooseCards = xmlcard.chooseCards
	cls.heroPower = xmlcard.heroPower
	cls.auras = xmlcard.auras
	cls.id = id
	return cls


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
