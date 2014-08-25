import json
import os
import uuid


_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir, "data", "basic.json")
f = open(_path, "r")
CARDS = json.load(f)
f.close()

THE_COIN = "GAME_005"


class Card(object):
	@classmethod
	def byId(cls, id):
		for card in CARDS:
			if card["id"] == id:
				return cls(card)
		raise ValueError("Could not find a card with id %r" % (id))

	def __init__(self, data):
		self._data = data
		self.name = data["name"]
		self.id = data["id"]
		self.uuid = uuid.uuid4()

	def __str__(self):
		return self.name

	def __repr__(self):
		return "<%s %s (%r)>" % (self.__class__.__name__, self.id, self.name)


def cardsForHero(hero):
	return [card["id"] for card in CARDS if card.get("playerClass") in (None, hero) and card.get("collectible")]
