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


tagnames = {
	"Atk": GameTag.ATK,
	"Aura": GameTag.AURA,
	"Charge": GameTag.CHARGE,
	"Cost": GameTag.COST,
	"Deathrattle": GameTag.DEATHRATTLE,
	"ExtraDeathrattles": GameTag.EXTRA_DEATHRATTLES,
	"Name": GameTag.CARDNAME,
}

def _initTags(carddef, cls):
	"""
	Iterate over the class attributes, mapping them to the tags dict
	Note that this only needs to be done once per class, hence why we
	do it here instead of in Card.__new__()
	"""
	for attr, value in carddef.__dict__.items():
		if attr in tagnames:
			cls.tags[tagnames[attr]] = value

	if hasattr(carddef, "Aura"):
		# Virtual card. Init its tags.
		carddef.Aura.tags = {}
		carddef.Aura.id = None
		_initTags(carddef.Aura, carddef.Aura)
		carddef.Aura.tags[GameTag.CARDTYPE] = CardType.ENCHANTMENT


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
	cls.entourage = xmlcard.entourage
	cls.chooseCards = xmlcard.chooseCards
	cls.id = id
	if isinstance(xmlcard.tags.get(GameTag.AURA), str):
		cls.Aura = merge(xmlcard.tags[GameTag.AURA])
	return cls


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
