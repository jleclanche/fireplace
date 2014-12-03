import json
import logging
from itertools import chain
from . import targeting
from .exceptions import *
from .entity import Entity
from .enums import CardType, GameTag, PlayReq, Race, Zone
from .utils import _TAG, CardList
from .xmlcard import XMLCard



THE_COIN = "GAME_005"


class Card(Entity):
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
		}[data.getTag(GameTag.CARDTYPE)]
		if type is Spell and data.getTag(GameTag.SECRET):
			type = Secret
		card = type(id)
		# type(id) triggers __init__, so we can't rely on card.data existing
		# so instead we super __init__ here and initialize tags then.
		super(Card, cls).__init__(card)
		card.data = data
		card.tags = data.tags
		return card

	def __init__(self, id):
		self.id = id
		self.aura = None
		self.weapon = None
		self.buffs = []

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
	# Tag properties

	type = _TAG(GameTag.CARDTYPE, CardType.INVALID)
	cost = _TAG(GameTag.COST, 0)
	controller = _TAG(GameTag.CONTROLLER, None)
	exhausted = _TAG(GameTag.EXHAUSTED, False)
	windfury = _TAG(GameTag.WINDFURY, False)
	hasCombo = _TAG(GameTag.COMBO, False)

	@property
	def zone(self):
		return self.tags.get(GameTag.ZONE)

	@zone.setter
	def zone(self, value):
		self.moveToZone(self.zone, value)
		self.tags[GameTag.ZONE] = value

	##
	# Properties affected by slots

	@property
	def health(self):
		return max(0, self.getIntProperty(GameTag.HEALTH) - self.damage)

	@property
	def atk(self):
		return self.getIntProperty(GameTag.ATK)

	@atk.setter
	def atk(self, value):
		self.tags[GameTag.ATK] = value

	@property
	def extraAtk(self):
		return sum(slot.getIntProperty(GameTag.ATK) for slot in self.slots)

	@property
	def extraHealth(self):
		return sum(slot.getIntProperty(GameTag.HEALTH) for slot in self.slots)

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
		ret = []
		if self.weapon:
			assert self.type == CardType.HERO
			ret.append(self.weapon)
		ret += self.buffs
		return ret

	def action(self, target=None, combo=None):
		kwargs = {}
		if self.hasTarget():
			kwargs["target"] = target
		if combo and self.hasCombo:
			if PlayReq.REQ_TARGET_FOR_COMBO in self.data.requirements:
				kwargs["target"] = target
			kwargs["combo"] = combo
			logging.info("Activating %r combo (%r)" % (self, kwargs))
			self.data.__class__.combo(self, **kwargs)
		else:
			logging.info("%r activates action(%r)" % (self, kwargs))
			self.data.__class__.action(self, **kwargs)

	def heal(self, target, amount):
		logging.info("%r heals %r for %i" % (self, target, amount))
		target.onHeal(amount, self)

	def hit(self, target, amount):
		logging.info("%r hits %r for %i" % (self, target, amount))
		target.onDamage(amount, self)

	def destroy(self):
		logging.info("%r dies" % (self))
		self.game.broadcast("onDeath", self)

	def moveToZone(self, old, new):
		logging.debug("%r moves from %r to %r" % (self, old, new))
		if old == Zone.HAND:
			self.controller.hand.remove(self)
		if new == Zone.HAND:
			self.controller.hand.append(self)

	##
	# Events

	def _forwardBroadcast(self, event, *args, **kwargs):
		if hasattr(self.data.__class__, event):
			return getattr(self.data.__class__, event)(self, *args, **kwargs)

	def onDeath(self, card):
		if card is self:
			self.zone = Zone.GRAVEYARD
			if self.hasDeathrattle:
				logging.info("Triggering Deathrattle for %r" % (self))
				self.data.__class__.deathrattle(self)
		self._forwardBroadcast("onDeath", card)

	def onCardPlayed(self, player, card):
		if player is self.controller:
			self.onOwnCardPlayed(card)
		self._forwardBroadcast("onCardPlayed", player, card)

	def onOwnCardPlayed(self, card):
		self._forwardBroadcast("onOwnCardPlayed", card)

	def afterCardPlayed(self, player, card):
		if player is self.controller:
			self.afterOwnCardPlayed(card)
		self._forwardBroadcast("afterCardPlayed", player, card)

	def afterOwnCardPlayed(self, card):
		self._forwardBroadcast("afterOwnCardPlayed", card)

	def onTurnBegin(self, player):
		if player is self.controller:
			self.onOwnTurnBegin()
		self._forwardBroadcast("onTurnBegin", player)

	def onOwnTurnBegin(self):
		self.exhausted = False
		self._forwardBroadcast("onOwnTurnBegin")

	def onTurnEnd(self, player):
		if player is self.controller:
			self.onOwnTurnEnd()
		self._forwardBroadcast("onTurnEnd", player)

	def onOwnTurnEnd(self):
		self._forwardBroadcast("onOwnTurnEnd")

	def setTag(self, *args):
		# Fire an onOwnUpdate every time a tag is set while in play
		super().setTag(*args)
		if self.zone == Zone.PLAY:
			self._forwardBroadcast("onOwnUpdate")

	def discard(self):
		logging.info("Discarding %r" % (self))
		self.zone = Zone.GRAVEYARD

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
		assert self.zone != Zone.PLAY
		self.controller.play(self, target)

	def summon(self):
		pass

	def buff(self, card):
		"""
		Helper for Player.summon(buff, minion)
		"""
		ret = self.controller.summon(card, target=self)
		self._forwardBroadcast("onOwnUpdate")


def cardsForHero(hero):
	return ['CS1_042', 'CS2_118', 'CS2_119', 'CS2_120', 'CS2_121', 'CS2_124', 'CS2_125', 'CS2_127', 'CS2_131', 'CS2_142', 'CS2_147', 'CS2_155', 'CS2_162', 'CS2_168', 'CS2_171', 'CS2_172', 'CS2_173', 'CS2_179', 'CS2_182', 'CS2_186', 'CS2_187', 'CS2_189', 'CS2_197', 'CS2_200', 'CS2_201', 'CS2_213', 'EX1_015', 'EX1_506', 'EX1_582']


class Character(Card):
	def __init__(self, id):
		super().__init__(id)

	race = _TAG(GameTag.CARDRACE, Race.INVALID)
	frozen = _TAG(GameTag.FROZEN, False)
	poisonous = _TAG(GameTag.POISONOUS, False)
	stealthed = _TAG(GameTag.STEALTH, False)

	def canAttack(self):
		if self.tags.get(GameTag.CANT_ATTACK, False):
			return False
		numAttacks = self.tags.get(GameTag.NUM_ATTACKS_THIS_TURN, 0)
		if self.windfury:
			if numAttacks >= 2:
				return False
		elif numAttacks >= 1:
			return False
		if self.atk == 0:
			return False
		if self.exhausted and not self.charge:
			return False
		if self.frozen:
			return False
		return True

	def attack(self, target):
		logging.info("%r attacks %r" % (self, target))
		self.hit(target, self.atk)
		if self.weapon:
			self.weapon.loseDurability()
		if target.atk:
			target.hit(self, target.atk)
		if self.stealthed:
			self.stealthed = False
		if GameTag.NUM_ATTACKS_THIS_TURN not in self.tags:
			self.tags[GameTag.NUM_ATTACKS_THIS_TURN] = 0
		self.tags[GameTag.NUM_ATTACKS_THIS_TURN] += 1

	@property
	def damage(self):
		return self.tags.get(GameTag.DAMAGE, 0)

	@damage.setter
	def damage(self, amount):
		amount = max(0, amount)
		if amount < self.damage:
			logging.info("%r healed for %i health (now at %i health)" % (self, self.damage - amount, self.health))
		elif amount == self.damage:
			logging.info("%r receives a no-op health change (now at %i health)" % (self, self.health))
		else:
			logging.info("%r damaged for %i health (now at %i health)" % (self, amount - self.damage, self.health))

		self.setTag(GameTag.DAMAGE, amount)

	def onOwnTurnBegin(self):
		self.setTag(GameTag.NUM_ATTACKS_THIS_TURN, 0)
		super().onOwnTurnBegin()

	def onOwnTurnEnd(self):
		if self.frozen and not self.tags[GameTag.NUM_ATTACKS_THIS_TURN]:
			self.frozen = False
		super().onOwnTurnEnd()

	def onDamage(self, amount, source):
		logging.info("%r onDamage event (amount=%r, source=%r)" % (self, amount, source))
		self.damage += amount

		# FIXME this should happen in a separate tick
		if not self.health:
			self.destroy()

	def onHeal(self, amount, source):
		logging.info("%r onHeal event (amount=%r, source=%r)" % (self, amount, source))
		self.damage -= amount

	def silence(self):
		logging.info("%r has been silenced" % (self))
		if self.aura:
			self.aura.destroy()
		self.buffs = []
		tags = (
			GameTag.CANT_ATTACK,
			GameTag.FROZEN,
			GameTag.POISONOUS,
			GameTag.STEALTH,
			GameTag.WINDFURY,
		)
		for tag in tags:
			if tag in self.tags:
				logging.info("Silencing tag %r on %r" % (tag, self))
				del self.tags[tag]


class Hero(Character):
	armor = _TAG(GameTag.ARMOR, 0)

	def onDamage(self, amount, source):
		if self.armor:
			newAmount = max(0, amount - self.armor)
			self.armor -= min(self.armor, amount)
			amount = newAmount
		super().onDamage(amount, source)

	def destroy(self):
		raise GameOver("%s wins!" % (self.controller.opponent))

	def summon(self):
		self.controller.hero = self
		self.controller.summon(self.data.power)

	@property
	def windfury(self):
		ret = self.tags.get(GameTag.WINDFURY, False)
		if not ret and self.weapon:
			# Heroes can inherit Windfury from weapons
			return self.weapon.windfury

	@windfury.setter
	def windfury(self, value):
		self.tags[GameTag.WINDFURY] = value


class Minion(Character):
	taunt = _TAG(GameTag.TAUNT, False)
	divineShield = _TAG(GameTag.DIVINE_SHIELD, False)
	adjacentBuff = _TAG(GameTag.ADJACENT_BUFF, False)
	hasAura = _TAG(GameTag.AURA, False)

	@property
	def charge(self):
		if self.tags.get(GameTag.CHARGE, False):
			return True
		return any(slot.getBoolProperty(GameTag.CHARGE) for slot in self.slots)

	@property
	def adjacentMinions(self):
		assert self.zone is Zone.PLAY, self.zone
		index = self.controller.field.index(self)
		left = self.controller.field[:index]
		right = self.controller.field[index+1:]
		return (left and left[-1] or None, right and right[0] or None)

	def bounce(self):
		logging.info("%r is bounced back to %s's hand" % (self, self.controller))
		if not self.controller.addToHand(self):
			logging.info("%s's hand is full and bounce fails" % (self.controller))
			self.destroy()
		else:
			self.zone = Zone.HAND

	def moveToZone(self, old, new):
		if old == Zone.PLAY:
			logging.info("%r is removed from the field" % (self))
			self.controller.field.remove(self)
			# Remove any aura the minion gives
			if self.aura:
				self.aura.destroy()
			if self.damage:
				self.damage = 0
		super().moveToZone(old, new)

	def onDamage(self, amount, source):
		if self.divineShield:
			self.divineShield = False
			logging.info("%r's divine shield prevents %i damage. Divine shield fades." % (self, amount))
			return
		super().onDamage(amount, source)
		if isinstance(source, Minion) and source.poisonous:
			logging.info("%r is destroyed because of %r is poisonous" % (self, source))
			self.destroy()

	def isPlayable(self):
		playable = super().isPlayable()
		if len(self.controller.field) >= self.game.MAX_MINIONS_ON_FIELD:
			return False
		return playable

	def summon(self):
		if len(self.controller.field) >= self.game.MAX_MINIONS_ON_FIELD:
			return
		self.controller.field.append(self)
		self.exhausted = True
		if self.data.cantAttack:
			self.setTag(GameTag.CANT_ATTACK, True)
		if self.hasAura:
			self.aura = Aura(self.data.aura)
			self.aura.source = self
			self.aura.controller = self.controller
			self.aura.summon()
			logging.info("Aura %r suddenly appears" % (self.aura))


class Spell(Card):
	pass


class Secret(Card):
	def isPlayable(self):
		# secrets are all unique
		if self.controller.secrets.contains(self):
			return False
		return super().isPlayable()

	def summon(self):
		self.zone = Zone.SECRET

	def moveToZone(self, old, new):
		if old == Zone.SECRET:
			self.controller.secrets.remove(self)
		if new == Zone.SECRET:
			self.controller.secrets.append(self)
		super().moveToZone(old, new)


class Enchantment(Card):
	def summon(self, target):
		self.owner = target
		target.buffs.append(self)

	def destroy(self):
		self.owner.buffs.remove(self)
		super().destroy()

	def onDeath(self, card):
		if card is self.owner:
			# If we have a deathrattle, it means the deathrattle is on the owner.
			if self.hasDeathrattle:
				logging.info("Triggering Enchantment Deathrattle for %r" % (self))
				self.data.__class__.deathrattle(self)

	def onTurnEnd(self, player):
		if self.data.oneTurnEffect:
			logging.info("Ending One-Turn effect: %r" % (self))
			self.destroy()
		super().onTurnEnd(player)


class Aura(Card):
	"""
	A virtual Card class which is only for the source of the Enchantment buff on
	targets affected by an aura. It is only internal.
	"""

	def __init__(self, id):
		super().__init__(id)
		self._buffed = CardList()
		self._buffs = []
		self.data = XMLCard.get(id)
		self.tags = self.data.tags

	@property
	def targets(self):
		return self.controller.getTargets(self.data.targeting)

	def summon(self):
		self.game.auras.append(self)
		self.zone = Zone.PLAY

	def isValidTarget(self, card):
		if self.source.adjacentBuff:
			adj = self.source.adjacentMinions
			if card is not adj[0] and card is not adj[1]:
				return False
		if card not in self.targets:
			return False
		if hasattr(self.data.__class__, "isValidTarget"):
			return self.data.__class__.isValidTarget(self, card)
		return True

	def onUpdate(self):
		for target in self.targets:
			if self.isValidTarget(target):
				if not target in self._buffed:
					self._buffs.append(target.buff(self.id))
					self._buffed.append(target)

	def destroy(self):
		for buff in self._buffs:
			buff.destroy()
		self.update()
		del self._buffed
		self.game.auras.remove(self)


class Weapon(Card):
	@property
	def durability(self):
		return self.tags[GameTag.DURABILITY]

	def gainDurability(self, amount=1):
		self.tags[GameTag.DURABILITY] += 1
		logging.info("%r gains %i durability (now at %i)" % (self, amount, self.durability))

	def loseDurability(self, amount=1):
		assert self.durability
		self.tags[GameTag.DURABILITY] -= 1
		logging.info("%r loses %i durability (now at %i)" % (self, amount, self.durability))
		if self.durability == 0:
			self.destroy()

	def destroy(self):
		self.controller.hero.weapon = None
		super().destroy()

	def summon(self):
		if self.controller.hero.weapon:
			self.controller.hero.weapon.destroy()
		self.controller.hero.weapon = self


class HeroPower(Card):
	def play(self, target=None):
		logging.info("%s plays hero power %r" % (self.controller, self))
		assert not self.exhausted
		self.controller.usedMana += self.cost
		self.action(target)
		self.exhausted = True

	def isPlayable(self):
		playable = super().isPlayable()
		if self.exhausted:
			return False
		return playable

	def summon(self):
		self.controller.hero.power = self
