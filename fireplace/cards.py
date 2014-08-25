import json
import os


_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir, "data", "basic.json")
f = open(_path, "r")
CARDS = json.load(f)
f.close()

THE_COIN = "GAME_005"

class Card(object):
	def __init__(self, json):
		self.json = json

	def __str__(self):
		return self.json["name"]

	def __repr__(self):
		return "<%s %s (%r)>" % (self.__class__.__name__, self.json["id"], self.json["name"])

def cardsForHero(hero):
	return [Card(card) for card in CARDS if card.get("playerClass") == hero or "playerClass" not in card]
