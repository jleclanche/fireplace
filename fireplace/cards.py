import json
import os
import uuid


_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir, "data", "basic.json")
f = open(_path, "r")
CARDS = json.load(f)
f.close()

THE_COIN = "GAME_005"


class Card(object):
	STATUS_DECK = 1
	STATUS_HAND = 2
	STATUS_FIELD = 3
	STATUS_GRAVEYARD = 4

	TYPE_MINION = "Minion"
	TYPE_SPELL = "Spell"
	TYPE_WEAPON = "Weapon"
	TYPE_HERO = "Hero"
	TYPE_HERO_POWER = "Hero Power"
	TYPE_ENCHANTMENT = "Enchantment"

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
		self.type = data["type"]
		self.uuid = uuid.uuid4()
		self.owner = None
		self.cost = data.get("cost", 0)
		self.status = self.STATUS_DECK

	def __str__(self):
		return self.name

	def __repr__(self):
		return "<%s %s (%r)>" % (self.__class__.__name__, self.id, self.name)

	def isPlayable(self):
		return self.owner.mana >= self.cost

	def play(self, target=None):
		assert self.owner
		# remove the card from the hand
		self.owner.hand.remove(self)
		self.owner.usedMana += self.cost
		if self.type == self.TYPE_MINION:
			self.owner.field.append(self)
		else:
			raise NotImplementedError

		self.status = self.STATUS_FIELD


def cardsForHero(hero):
	return [card["id"] for card in CARDS if card.get("playerClass") in (None, hero) and card.get("collectible")]
