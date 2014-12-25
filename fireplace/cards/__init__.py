import os
from ..enums import GameTag
from .game import *
from .classic import *
from .debug import *
from .gvg import *
from .naxxramas import *
from . import cardxml


_PATH = os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir, "data", "TextAsset", "enUS.txt")

tagnames = {
	"Atk": GameTag.ATK,
	"Aura": GameTag.AURA,
	"Charge": GameTag.CHARGE,
	"Chromatic": GameTag.CANT_BE_TARGETED_BY_ABILITIES, # XXX
	"Durability": GameTag.DURABILITY,
	"Deathrattle": GameTag.DEATH_RATTLE,
	"Enrage": GameTag.ENRAGED,
	"ExtraDeathrattles": GameTag.EXTRA_DEATHRATTLES,
	"Health": GameTag.HEALTH,
	"Recall": GameTag.RECALL,
	"Stealth": GameTag.STEALTH,
	"Spellpower": GameTag.SPELLPOWER,
	"Taunt": GameTag.TAUNT,
	"Windfury": GameTag.WINDFURY,
	"OneTurnEffect": GameTag.OneTurnEffect,
	"cantAttack": GameTag.CANT_ATTACK, # XXX
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
		cls = type(id, (carddef, ), {})
	cls.tags = xmlcard.tags
	if carddef:
		if hasattr(carddef, "Enrage"):
			# Initialize the Enrage virtual card too
			carddef.Enrage.tags = {}
			_initTags(carddef.Enrage, carddef.Enrage)
		_initTags(carddef, cls)
	cls.requirements = xmlcard.requirements
	cls.entourage = xmlcard.entourage
	cls.id = id
	return cls


# Here we import every card from every set and load the cardxml database.
# For every card, we will "merge" the class with its Python definition if
# it exists.
# This code is only ran once, at initial import.

if "cardlist" not in globals():
	with open(_PATH, "r") as f:
		db = cardxml.load(_PATH)
		cardlist = []
		for id in db:
			globals()[id] = merge(id)
			cardlist.append(id)
