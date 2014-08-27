import inspect
import json
import logging
import os
import uuid
from lxml.etree import ElementTree


_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir, "data", "TextAsset")

THE_COIN = "GAME_005"

class XMLCard(object):
	def __init__(self, id):
		self.file = os.path.join(_path, "%s.xml" % (id))
		self.xml = ElementTree().parse(self.file)

	def _getXML(self, xpath):
		return self.xml.xpath(xpath)

	@property
	def name(self):
		return self._getXML("/Entity/Tag[@name='CardName']/enUS/text()")[0]

	@property
	def type(self):
		return int(self._getXML("/Entity/Tag[@name='CardType']/@value")[0])

	@property
	def health(self):
		return int(self._getXML("/Entity/Tag[@name='Health']/@value")[0])

	@property
	def cost(self):
		return int((self._getXML("/Entity/Tag[@name='Cost']/@value") or [0])[0])

	@property
	def charge(self):
		return bool(int((self._getXML("/Entity/Tag/[@name='Charge']/@value") or [0])[0]) or 0)

	@property
	def taunt(self):
		return bool(int((self._getXML("/Entity/Tag/[@name='Taunt']/@value") or [0])[0]) or 0)


class Card(XMLCard):
	STATUS_DECK = 1
	STATUS_HAND = 2
	STATUS_FIELD = 3
	STATUS_GRAVEYARD = 4

	TYPE_MINION = 4
	TYPE_SPELL = 5
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
			datacls = object
		new_class = type(id, (cls, datacls), {})
		return new_class(id)

	def __init__(self, id):
		self.id = id
		self.uuid = uuid.uuid4()
		self.owner = None
		self.status = self.STATUS_DECK
		super().__init__(id)

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
			self.owner.summon(self)
		elif self.type == self.TYPE_SPELL:
			if not hasattr(self, "activate"):
				raise NotImplementedError
		else:
			raise NotImplementedError(self.name, self.type)

		if hasattr(self, "activate"):
			logging.info("Triggering 'activate' for %r" % (self))
			if self.hasTarget():
				self.activate(target=target)
			else:
				self.activate()

		self.status = self.STATUS_FIELD


def cardsForHero(hero):
	return ['CS1_042', 'CS2_118', 'CS2_119', 'CS2_120', 'CS2_121', 'CS2_124', 'CS2_125', 'CS2_127', 'CS2_131', 'CS2_142', 'CS2_147', 'CS2_155', 'CS2_162', 'CS2_168', 'CS2_171', 'CS2_172', 'CS2_173', 'CS2_179', 'CS2_182', 'CS2_186', 'CS2_187', 'CS2_189', 'CS2_197', 'CS2_200', 'CS2_201', 'CS2_213', 'EX1_015', 'EX1_506', 'EX1_582']


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
