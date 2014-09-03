import json
import logging
import uuid
from .exceptions import *
from .targeting import *
from .xmlcard import XMLCard



THE_COIN = "GAME_005"


class Card(object):
	STATUS_DECK = 1
	STATUS_HAND = 2
	STATUS_FIELD = 3
	STATUS_GRAVEYARD = 4
	STATUS_DISCARD = 5

	TYPE_HERO = 3
	TYPE_MINION = 4
	TYPE_SPELL = 5
	TYPE_ENCHANTMENT = 6
	TYPE_WEAPON = 7
	TYPE_HERO_POWER = 10

	def __init__(self, id):
		self.id = id
		self.data = XMLCard.get(id)
		self.uuid = uuid.uuid4()
		self.owner = None
		self.status = self.STATUS_DECK
		self.damageCounter = 0
		self.durabilityCounter = 0
		self.summoningSickness = False
		self.weapon = None
		self.armor = 0
		super().__init__()
		self.shield = self.data.divineShield
		if not hasattr(self.data, "targeting"):
			self.data.targeting = TARGET_NONE
		if not hasattr(self.data, "minTargets"):
			self.data.minTargets = 0

	def __str__(self):
		return self.data.name

	def __repr__(self):
		return "<%s (%r)>" % (self.__class__.__name__, self.data.name)

	@property
	def game(self):
		return self.owner.game

	##
	# Properties affected by slots

	@property
	def health(self):
		damage  = self.damageCounter
		health = self.getProperty("health")
		return max(0, health - damage)

	@property
	def atk(self):
		return self.getProperty("atk")

	@property
	def durability(self):
		return self.getProperty("durability")

	@property
	def targets(self):
		return self.getTargets(self.data.targeting)

	@property
	def cost(self):
		return self.data.cost

	@property
	def type(self):
		return self.data.type

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

	def hasTarget(self):
		return self.data.targeting and (not self.data.targeting & TARGET_MULTIPLE)

	def isValidTarget(self, card):
		if card not in self.targets:
			return False
		return self.data.__class__.isValidTarget(self, card)

	@property
	def slots(self):
		# TODO enchantments
		ret = []
		if self.weapon:
			assert self.type == self.TYPE_HERO
			ret.append(self.weapon)
		for aura in self.game.auras:
			if aura.isValidTarget(self):
				ret.append(aura)
		return ret

	def canAttack(self):
		if self.atk == 0:
			return False
		if self.summoningSickness and not self.charge:
			return False
		return True

	def attack(self, target):
		logging.info("%r attacks %r" % (self, target))
		target.damage(self.atk)
		if self.weapon:
			self.weapon.loseDurability()
		if target.atk:
			self.damage(target.atk)

	def loseDurability(self, amount=1):
		assert self.type == self.TYPE_WEAPON
		assert self.durability
		# XXX
		self.durabilityCounter += 1
		logging.info("%r loses %i durability (now at %i)" % (self, amount, self.durability))
		if self.durability == 0:
			self.destroy()

	def gainArmor(self, amount):
		assert self.type == self.TYPE_HERO
		self.armor += amount
		logging.info("%r gains %i armor (now at %i)" % (self, amount, self.armor))

	def damage(self, amount):
		if self.shield:
			assert self.type is self.TYPE_MINION
			self.shield = False
			logging.info("%r's divine shield prevents %i damage. Divine shield fades." % (self, amount))
			return
		if self.armor:
			newAmount = max(0, amount - self.armor)
			self.armor -= min(self.armor, amount)
			logging.info("%r reduces damage taken by %i through armor. %i armor remaining" % (self, amount - newAmount, self.armor))
			amount = newAmount

		self.damageCounter += min(self.health, amount)
		logging.info("%r damaged for %i health (now at %i health)" % (self, amount, self.health))

		# this should happen elsewhere
		if self.health == 0:
			self.destroy()

	def heal(self, amount):
		self.damageCounter -= min(amount, self.damageCounter)
		logging.info("%r healed for %i health (now at %i health)" % (self, amount, self.health))

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
			# Remove any aura the minion gives
			if self.data.hasAura:
				logging.info("Aura %r fades" % (self.aura))
				self.game.auras.remove(self.aura)
		elif self.type == self.TYPE_WEAPON:
			# HACK
			self.owner.hero.weapon = None
		elif self.type == self.TYPE_HERO:
			raise GameOver("%s wins!" % (self.owner.opponent))
		elif self.type == self.TYPE_ENCHANTMENT:
			self.owner.slots.remove(self)
		else:
			raise NotImplementedError(self.type)

		if self.data.hasDeathrattle:
			logging.info("Triggering Deathrattle for %r" % (self))
			self.data.__class__.deathrattle(self)

	def discard(self):
		logging.info("Discarding %r" % (self))
		self.status = self.STATUS_DISCARD
		self.owner.hand.remove(self)

	def isPlayable(self):
		if self.owner.mana < self.cost:
			return False
		if len(self.targets) < self.data.minTargets:
			return False
		if self.type == self.TYPE_MINION:
			if len(self.owner.field) >= self.game.MAX_MINIONS_ON_FIELD:
				return False
		return True

	def play(self, target=None):
		logging.info("%s plays %r" % (self.owner, self))
		assert self.owner, "That minion is not mine!"
		assert self.isPlayable(), "Not enough mana!"
		self.owner.availableMana -= self.cost
		self.status = self.STATUS_FIELD

		if self.type is self.TYPE_MINION:
			self.owner.summon(self)
			self.summoningSickness = True
			if self.data.hasAura:
				self.aura = Card(self.data.aura)
				self.aura.owner = self.owner
				self.aura.source = self
				logging.info("Aura %r suddenly appears" % (self.aura))
				self.game.auras.append(self.aura)
		elif self.type in (self.TYPE_SPELL, self.TYPE_HERO_POWER):
			if not hasattr(self.data, "activate"):
				raise NotImplementedError(self)
		elif self.type == self.TYPE_WEAPON:
			self.owner.hero.equip(self)
		elif self.type == self.TYPE_HERO:
			self.owner.hero = self
			self.power = Card(self.data.power)
			self.power.owner = self.owner
			assert self.power.type is self.TYPE_HERO_POWER, self.power.type
		else:
			raise NotImplementedError(self.name, self.type)

		# Card must already be on the field for activate
		if self.type not in (self.TYPE_HERO, self.TYPE_HERO_POWER):
			self.owner.hand.remove(self)

		if hasattr(self.data, "activate"):
			logging.info("Triggering 'activate' for %r" % (self))
			activate = self.data.__class__.activate
			if self.hasTarget():
				activate(self, target=target)
			else:
				activate(self)

	def getProperty(self, prop):
		ret = getattr(self.data, prop)
		ret -= getattr(self, prop + "Counter", 0)
		for slot in self.slots:
			ret += slot.getProperty(prop)
		return ret

	def buff(self, card):
		if isinstance(card, str):
			from .cards import Card
			card = Card(card)
		card.owner = self
		logging.debug("%r receives buff: %r" % (self, card))
		assert card.type == card.TYPE_ENCHANTMENT, card.type
		self.buffs.append(card)



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
