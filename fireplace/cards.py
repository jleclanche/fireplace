import json
import logging
import os
import uuid
from lxml.etree import ElementTree
from .exceptions import *
from .targeting import *
from . import carddata


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
	def durability(self):
		return int(self._getXML("/Entity/Tag[@name='Durability']/@value")[0])

	@property
	def atk(self):
		return int((self._getXML("/Entity/Tag[@name='Atk']/@value") or [0])[0])

	@property
	def cost(self):
		return int((self._getXML("/Entity/Tag[@name='Cost']/@value") or [0])[0])

	@property
	def charge(self):
		return bool(int((self._getXML("/Entity/Tag[@name='Charge']/@value") or [0])[0]))

	@property
	def taunt(self):
		return bool(int((self._getXML("/Entity/Tag/[@name='Taunt']/@value") or [0])[0]) or 0)


class _Card(XMLCard):
	STATUS_DECK = 1
	STATUS_HAND = 2
	STATUS_FIELD = 3
	STATUS_GRAVEYARD = 4
	STATUS_DISCARD = 5

	TYPE_HERO = 3
	TYPE_MINION = 4
	TYPE_SPELL = 5
	TYPE_WEAPON = 7
	TYPE_HERO_POWER = "Hero Power"
	TYPE_ENCHANTMENT = "Enchantment"

	def __init__(self, id):
		self.id = id
		self.uuid = uuid.uuid4()
		self.owner = None
		self.status = self.STATUS_DECK
		self.damageCounter = 0
		self.durabilityCounter = 0
		self.summoningSickness = False
		self.weapon = None
		super().__init__(id)

	def __str__(self):
		return self.name

	def __repr__(self):
		return "<%s (%r)>" % (self.__class__.__name__, self.name)

	@property
	def game(self):
		return self.owner.game

	def isPlayable(self):
		if self.owner.mana < self.cost:
			return False
		if len(self.targets) < self.minTargets:
			return False
		if self.type == self.TYPE_MINION:
			if len(self.owner.field) >= self.game.MAX_MINIONS_ON_FIELD:
				return False
		return True

	def getTargets(self, t):
		ret = []
		if t & TARGET_FRIENDLY:
			if t & TARGET_HERO:
				ret.append(self.owner.hero)
			if t & TARGET_MULTIPLE:
				if t & TARGET_MINION:
					ret += self.owner.field

		if t & TARGET_ENEMY:
			if t & TARGET_HERO:
				ret.append(self.owner.opponent.hero)
			if t & TARGET_MULTIPLE:
				if t & TARGET_MINION:
					ret += self.owner.opponent.field

		return ret

	@property
	def targets(self):
		return self.getTargets(self.targeting)

	def hasTarget(self):
		return self.targeting and (not self.targeting & TARGET_MULTIPLE)

	def canAttack(self):
		if self.getProperty("atk") == 0:
			return False
		if self.summoningSickness and not self.charge:
			return False
		return True

	@property
	def slots(self):
		# TODO enchantments
		if self.weapon:
			assert self.type == self.TYPE_HERO
			return [self.weapon]
		return []

	def getProperty(self, prop):
		ret = getattr(self, prop)
		ret -= getattr(self, prop + "Counter", 0)
		for slot in self.slots:
			ret += getattr(slot, prop)
			ret -= getattr(slot, prop + "Counter", 0)
		return ret

	def attack(self, target):
		logging.info("%r attacks %r" % (self, target))
		atk = self.getProperty("atk")
		target.damage(atk)
		if self.weapon:
			self.weapon.loseDurability()
		if target.atk:
			self.damage(target.atk)

	def loseDurability(self, amount=1):
		assert self.type == self.TYPE_WEAPON
		assert self.getProperty("durability")
		# XXX
		self.durabilityCounter += 1
		logging.info("%r loses %i durability (now at %i)" % (self, amount, self.getProperty("durability")))
		if self.getProperty("durability") == 0:
			self.destroy()

	@property
	def currentHealth(self):
		return max(0, self.health - self.damageCounter)

	def heal(self, amount):
		self.damageCounter -= min(amount, self.damageCounter)
		logging.info("%r healed for %i health (now at %i health)" % (self, amount, self.currentHealth))

	def damage(self, amount):
		self.damageCounter += min(self.health, amount)
		logging.info("%r damaged for %i health (now at %i health)" % (self, amount, self.currentHealth))

		# this should happen elsewhere
		if self.currentHealth == 0:
			self.destroy()

	def equip(self, weapon):
		logging.info("%r equips %r" % (self, weapon))
		if self.weapon:
			self.weapon.destroy()
		self.weapon = weapon

	def destroy(self):
		logging.info("%r dies" % (self))
		self.status = self.STATUS_GRAVEYARD
		if self.type == self.TYPE_MINION:
			self.owner.field.remove(self)
		elif self.type == self.TYPE_WEAPON:
			# HACK
			self.owner.hero.weapon = None
		elif self.type == self.TYPE_HERO:
			raise GameOver("%s wins!" % (self.owner.opponent))
		else:
			raise NotImplementedError(self.type)

	def discard(self):
		logging.info("Discarding %r" % (self))
		self.status = self.STATUS_DISCARD
		self.owner.hand.remove(self)

	def play(self, target=None):
		logging.info("%s plays %r" % (self.owner, self))
		assert self.owner, "That minion is not mine!"
		assert self.isPlayable(), "Not enough mana!"
		# remove the card from the hand
		self.owner.hand.remove(self)
		self.owner.usedMana += self.cost
		if self.type == self.TYPE_MINION:
			self.owner.summon(self)
			self.summoningSickness = True
		elif self.type == self.TYPE_SPELL:
			if not hasattr(self, "activate"):
				raise NotImplementedError
		elif self.type == self.TYPE_WEAPON:
			self.owner.hero.equip(self)
		else:
			raise NotImplementedError(self.name, self.type)

		if hasattr(self, "activate"):
			logging.info("Triggering 'activate' for %r" % (self))
			if self.hasTarget():
				self.activate(target=target)
			else:
				self.activate()

		self.status = self.STATUS_FIELD


def Card(id):
	data = getattr(carddata, id, object)
	datadict = {
		"targeting": getattr(data, "targeting", TARGET_NONE),
		"minTargets": getattr(data, "minTargets", 0),
	}
	cardcls = type(id, (_Card, data), datadict)
	return cardcls(id)


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
