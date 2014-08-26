import inspect
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
		from . import carddata
		if hasattr(carddata, id):
			datacls = getattr(carddata, id)
		else:
			# temporary until most cards are done
			datacls = object
		for data in CARDS:
			if data["id"] == id:
				if datacls is object:
					logging.warning("Unimplemented card: %r (%s)" % (id, data["name"]))
				new_class = type(id, (cls, datacls), {})
				return new_class(data)
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
		return "<%s (%r)>" % (self.__class__.__name__, self.name)

	def isPlayable(self):
		return self.owner.mana >= self.cost

	def hasTarget(self):
		return "target" in inspect.getargspec(self.activate).args

	def damage(self, amount):
		self.health -= amount
		logging.info("%r damaged for %i health (now at %i health)" % (self, amount, self.health))

		# this should happen elsewhere
		if self.health == 0:
			self.destroy()

	def destroy(self):
		logging.info("%r dies" % (self))
		self.status = self.STATUS_GRAVEYARD
		self.owner.field.remove(self)

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
			if not hasattr(self, "activate"):
				raise NotImplementedError
		else:
			raise NotImplementedError

		if hasattr(self, "activate"):
			logging.info("Triggering 'activate' for %r" % (self))
			if self.hasTarget():
				self.activate(target=target)
			else:
				self.activate()

		self.status = self.STATUS_FIELD


def cardsForHero(hero):
	"Returns playable (collectible) cards for hero \a hero"
	return [card["id"] for card in CARDS if card.get("playerClass") in (None, hero) and card.get("collectible")]


class BaseCard(object):
	pass


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
