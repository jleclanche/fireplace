import json
import logging
import uuid
from itertools import chain
from . import targeting
from .exceptions import *
from .enums import CardType, GameTag, PlayReq, Zone
from .xmlcard import XMLCard



THE_COIN = "GAME_005"


class Card(object):
	def __new__(cls, id):
		if cls is not Card:
			return super().__new__(cls)
		data = XMLCard.get(id)
		type = {
			CardType.HERO: Hero,
			CardType.MINION: Minion,
			CardType.SPELL: Spell,
			CardType.ENCHANTMENT: Enchantment,
			CardType.WEAPON: Weapon,
			CardType.HERO_POWER: HeroPower,
		}[data.type]
		if type is Spell and data.secret:
			type = Secret
		card = type(id)
		card.data = data
		return card

	def __init__(self, id):
		self.id = id
		self.tags = {}
		self.uuid = uuid.uuid4()
		self.controller = None
		self.zone = Zone.DECK
		self.damageCounter = 0
		self.durabilityCounter = 0
		self.weapon = None
		self.buffs = []
		super().__init__()

	def __str__(self):
		return self.data.name

	def __repr__(self):
		return "<%s (%r)>" % (self.__class__.__name__, self.data.name)

	def __eq__(self, other):
		if isinstance(other, Card):
			return self.id.__eq__(other.id)
		elif isinstance(other, str):
			return self.id.__eq__(other)
		return super().__eq__(other)

	@property
	def game(self):
		return self.controller.game

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
	def cost(self):
		return self.data.cost

	@property
	def type(self):
		return self.data.type

	@property
	def hasDeathrattle(self):
		return hasattr(self.data, "deathrattle") or self.data.hasDeathrattle

	@property
	def targets(self):
		full_board = self.game.board + [self.controller.hero, self.controller.opponent.hero]
		return [card for card in full_board if self.isValidTarget(card)]

	isValidTarget = targeting.isValidTarget

	def hasTarget(self):
		return PlayReq.REQ_TARGET_TO_PLAY in self.data.requirements or \
			PlayReq.REQ_TARGET_IF_AVAILABLE in self.data.requirements

	@property
	def slots(self):
		# TODO enchantments
		ret = []
		if self.weapon:
			assert self.type == CardType.HERO
			ret.append(self.weapon)
		for aura in self.game.auras:
			if aura.isValidTarget(self):
				ret.append(aura)
		ret += self.buffs
		return ret

	def action(self, target=None, combo=None):
		kwargs = {}
		if self.hasTarget():
			kwargs["target"] = target
		if combo and self.data.hasCombo:
			if PlayReq.REQ_TARGET_FOR_COMBO in self.data.requirements:
				kwargs["target"] = target
			kwargs["combo"] = combo
			logging.info("Activating %r combo (%r)" % (self, kwargs))
			self.data.__class__.combo(self, **kwargs)
		else:
			logging.info("%r activates action(%r)" % (self, kwargs))
			self.data.__class__.action(self, **kwargs)

	def destroy(self):
		logging.info("%r dies" % (self))
		self.zone = Zone.GRAVEYARD
		self.onDeath()
		for slot in self.slots:
			slot.onDeath()

	def onDeath(self):
		if self.hasDeathrattle:
			logging.info("Triggering Deathrattle for %r" % (self))
			self.data.__class__.deathrattle(self)

	def discard(self):
		logging.info("Discarding %r" % (self))
		self.zone = Zone.GRAVEYARD
		self.controller.hand.remove(self)

	def isPlayable(self):
		if self.controller.mana < self.cost:
			return False
		if PlayReq.REQ_TARGET_TO_PLAY in self.data.requirements:
			if not self.targets:
				return False
		if len(self.controller.opponent.field) < self.data.minTargets:
			return False
		if len(self.controller.game.board) < self.data.minMinions:
			return False
		if PlayReq.REQ_ENTIRE_ENTOURAGE_NOT_IN_PLAY in self.data.requirements:
			entourage = list(self.data.entourage)
			for minion in self.controller.field:
				if minion.id in entourage:
					entourage.remove(minion.id)
			if not entourage:
				return False
		return True

	def play(self, target=None):
		"""
		Helper for Player.play(card)
		"""
		self.controller.play(self, target)

	def summon(self):
		pass

	def getProperty(self, prop):
		ret = getattr(self.data, prop)
		ret -= getattr(self, prop + "Counter", 0)
		for slot in self.slots:
			ret += slot.getProperty(prop)
		return ret

	def setTag(self, tag, value):
		self.tags[tag] = value

	def unsetTag(self, tag):
		del self.tags[tag]

	def buff(self, card):
		"""
		Helper for Player.summon(buff, minion)
		"""
		return self.controller.summon(card, target=self)


def cardsForHero(hero):
	return ['CS1_042', 'CS2_118', 'CS2_119', 'CS2_120', 'CS2_121', 'CS2_124', 'CS2_125', 'CS2_127', 'CS2_131', 'CS2_142', 'CS2_147', 'CS2_155', 'CS2_162', 'CS2_168', 'CS2_171', 'CS2_172', 'CS2_173', 'CS2_179', 'CS2_182', 'CS2_186', 'CS2_187', 'CS2_189', 'CS2_197', 'CS2_200', 'CS2_201', 'CS2_213', 'EX1_015', 'EX1_506', 'EX1_582']


class Character(Card):
	def __init__(self, id):
		super().__init__(id)

	@property
	def race(self):
		return self.data.race

	@property
	def frozen(self):
		return self.tags.get(GameTag.FROZEN, False)

	@property
	def stealthed(self):
		return self.tags.get(GameTag.STEALTH, False)

	@property
	def windfury(self):
		if self.tags.get(GameTag.WINDFURY, False):
			return True
		return self.getProperty("windfury")

	def canAttack(self):
		numAttacks = self.tags[GameTag.NUM_ATTACKS_THIS_TURN]
		if self.windfury:
			if numAttacks >= 2:
				return False
		elif numAttacks >= 1:
			return False
		if self.atk == 0:
			return False
		if self.summoningSickness and not self.charge:
			return False
		if self.frozen:
			return False
		return True

	def attack(self, target):
		logging.info("%r attacks %r" % (self, target))
		target.damage(self.atk)
		if self.weapon:
			self.weapon.loseDurability()
		if target.atk:
			self.damage(target.atk)
		if self.stealthed:
			self.unstealth()
		self.tags[GameTag.NUM_ATTACKS_THIS_TURN] += 1

	def damage(self, amount):
		self.damageCounter += min(self.health, amount)
		logging.info("%r damaged for %i health (now at %i health)" % (self, amount, self.health))

		# this should happen elsewhere
		if self.health == 0:
			self.destroy()

	def heal(self, amount):
		self.damageCounter -= min(amount, self.damageCounter)
		logging.info("%r healed for %i health (now at %i health)" % (self, amount, self.health))

	def isDamaged(self):
		return bool(self.damageCounter)

	def freeze(self):
		logging.info("%r is now frozen" % (self))
		self.setTag(GameTag.FROZEN, True)

	def unfreeze(self):
		logging.info("%r is no longer frozen" % (self))
		self.unsetTag(GameTag.FROZEN)

	def stealth(self):
		logging.info("%r is now stealthed" % (self))
		self.setTag(GameTag.STEALTH, True)

	def unstealth(self):
		logging.info("%r is no longer stealthed" % (self))
		self.unsetTag(GameTag.STEALTH)


class Hero(Character):
	@property
	def armor(self):
		return self.tags.get(GameTag.ARMOR, 0)

	def gainArmor(self, amount):
		if GameTag.ARMOR not in self.tags:
			self.tags[GameTag.ARMOR] = 0
		self.tags[GameTag.ARMOR] += amount
		logging.info("%r gains %i armor (now at %i)" % (self, amount, self.armor))

	def loseArmor(self, amount):
		self.tags[GameTag.ARMOR] -= amount
		logging.info("%r loses %i armor (now at %i)" % (self, amount, self.armor))

	def damage(self, amount):
		if self.armor:
			newAmount = max(0, amount - self.armor)
			self.loseArmor(min(self.armor, amount))
			amount = newAmount
		super().damage(amount)

	def destroy(self):
		raise GameOver("%s wins!" % (self.controller.opponent))

	def summon(self):
		self.controller.hero = self
		self.controller.summon(self.data.power)


class Minion(Character):
	def __init__(self, id):
		super().__init__(id)
		self.summoningSickness = False

	@property
	def charge(self):
		for slot in self.slots:
			if slot.charge:
				return True
		return self.data.charge

	@property
	def adjacentMinions(self):
		assert self.zone is Zone.PLAY, self.zone
		index = self.controller.field.index(self)
		left = self.controller.field[:index]
		right = self.controller.field[index+1:]
		return (left and left[-1] or None, right and right[0] or None)

	def bounce(self):
		logging.info("%r is bounced back to %s's hand" % (self, self.controller))
		self.removeFromField()
		self.controller.addToHand(self)

	def removeFromField(self):
		logging.info("%r is removed from the field" % (self))
		self.controller.field.remove(self)
		# Remove any aura the minion gives
		if self.data.hasAura:
			logging.info("Aura %r fades" % (self.aura))
			self.game.auras.remove(self.aura)

	def damage(self, amount):
		if self.shield:
			self.shield = False
			logging.info("%r's divine shield prevents %i damage. Divine shield fades." % (self, amount))
			return
		super().damage(amount)

	def destroy(self):
		self.removeFromField()
		super().destroy()

	def isPlayable(self):
		playable = super().isPlayable()
		if len(self.controller.field) >= self.game.MAX_MINIONS_ON_FIELD:
			return False
		return playable

	def summon(self):
		if len(self.controller.field) >= self.game.MAX_MINIONS_ON_FIELD:
			return
		self.controller.field.append(self)
		self.summoningSickness = True
		if self.data.stealth:
			self.stealth()
		if self.data.windfury:
			self.setTag(GameTag.WINDFURY, True)
		if self.data.hasAura:
			self.aura = Card(self.data.aura)
			self.aura.controller = self.controller
			self.aura.zone = Zone.PLAY
			self.aura.source = self
			logging.info("Aura %r suddenly appears" % (self.aura))
			self.game.auras.append(self.aura)
		self.shield = self.data.divineShield


class Spell(Card):
	pass


class Secret(Card):
	def isPlayable(self):
		# secrets are all unique
		if self.controller.secrets.contains(self):
			return False
		return super().isPlayable()

	def summon(self):
		self.controller.secrets.append(self)
		self.zone = Zone.SECRET

	def destroy(self):
		self.controller.secrets.remove(self)
		super().destroy()


class Enchantment(Card):
	@property
	def targets(self):
		return self.controller.getTargets(self.data.targeting)

	def isValidTarget(self, card):
		if self.source.data.adjacentBuff:
			adj = self.source.adjacentMinions
			if card is not adj[0] and card is not adj[1]:
				return False
		if card not in self.targets:
			return False
		if hasattr(self.data.__class__, "isValidTarget"):
			return self.data.__class__.isValidTarget(self, card)
		return True

	def summon(self, target):
		self.owner = target
		target.buffs.append(self)

	def destroy(self):
		if self in self.game.auras:
			self.game.auras.remove(self)
		else:
			self.owner.buffs.remove(self)
		super().destroy()


class Weapon(Card):
	@property
	def durability(self):
		return self.getProperty("durability")

	def loseDurability(self, amount=1):
		assert self.type == CardType.WEAPON
		assert self.durability
		# XXX
		self.durabilityCounter += 1
		logging.info("%r loses %i durability (now at %i)" % (self, amount, self.durability))
		if self.durability == 0:
			self.destroy()

	def destroy(self):
		# HACK
		self.controller.hero.weapon = None
		super().destroy()

	def summon(self):
		if self.controller.hero.weapon:
			self.controller.hero.weapon.destroy()
		self.controller.hero.weapon = self


class HeroPower(Card):
	def play(self, target=None):
		logging.info("%s plays hero power %r" % (self.controller, self))
		self.controller.availableMana -= self.cost
		self.action(target)

	def summon(self):
		self.controller.hero.power = self
