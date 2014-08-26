import json
import logging
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

		from . import carddata
		if hasattr(carddata, self.id):
			self.script = getattr(carddata, self.id)(self)
		else:
			self.script = None
			logging.warning("Unimplemented card: %r" % (self))

	def __str__(self):
		return self.name

	def __repr__(self):
		return "<%s %s (%r)>" % (self.__class__.__name__, self.id, self.name)

	def isPlayable(self):
		return self.owner.mana >= self.cost

	def play(self, target=None):
		logging.info("%s plays %r" % (self.owner, self))
		assert self.owner, "That minion is not mine!"
		assert self.isPlayable(), "Not enough mana!"
		# remove the card from the hand
		self.owner.hand.remove(self)
		self.owner.usedMana += self.cost
		if self.type == self.TYPE_MINION:
			self.owner.field.append(self)
		elif self.type == self.TYPE_SPELL:
			if not hasattr(self.script, "activate"):
				raise NotImplementedError
			self.script.activate()
		else:
			raise NotImplementedError

		if not self.script:
			raise NotImplementedError("Unimplemented card: %r" % (self))
		if hasattr(self.script, "battlecry"):
			logging.info("Triggering battlecry for %r" % (self))
			self.script.battlecry()

		self.status = self.STATUS_FIELD


def cardsForHero(hero):
	"Returns playable (collectible) cards for hero \a hero"
	return [card["id"] for card in CARDS if card.get("playerClass") in (None, hero) and card.get("collectible")]


class BaseCard(object):
	def __init__(self, card):
		self._card = card

	def __getattr__(self, attr):
		# XXX hacky, should merge with Card
		if attr == "_card":
			return super().__getattr__(attr)
		return getattr(self._card, attr)


class Minion(BaseCard):
	pass


class Spell(BaseCard):
	pass


class Weapon(BaseCard):
	pass


class Hero(BaseCard):
	pass


class HeroPower(BaseCard):
	pass
