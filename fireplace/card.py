import json
import logging
import uuid
from itertools import chain
from . import cards as CardDB, targeting
from .exceptions import *
from .entity import Entity
from .enums import CardClass, CardType, GameTag, PlayReq, Race, Rarity, Zone
from .utils import _PROPERTY, _TAG, CardList



THE_COIN = "GAME_005"


def Card(id, data=None):
	if data is None:
		data = getattr(CardDB, id)
	subclass = {
		CardType.HERO: Hero,
		CardType.MINION: Minion,
		CardType.SPELL: Spell,
		CardType.ENCHANTMENT: Enchantment,
		CardType.WEAPON: Weapon,
		CardType.HERO_POWER: HeroPower,
	}[data.tags[GameTag.CARDTYPE]]
	if subclass is Spell and data.tags.get(GameTag.SECRET):
		subclass = Secret
	return subclass(id, data)


class BaseCard(Entity):
	def __init__(self, id, data):
		assert data
		super().__init__()
		self.uuid = uuid.uuid4()
		self._auras = []
		self.data = data
		self.requirements = data.requirements.copy()
		self.tags = data.tags.copy()
		self.id = id
		for event in self.events:
			if hasattr(data, event):
				if event not in self._eventListeners:
					self._eventListeners[event] = []
				# A bit of magic powder to pass the Card object as self to the Card defs
				func = getattr(data, event)
				zone = getattr(func, "zone", Zone.PLAY)
				_func = lambda *args: func(self, *args)
				_func.zone = getattr(func, "zone", Zone.PLAY)
				self._eventListeners[event].append(_func)

	def __str__(self):
		return self.data.tags[GameTag.CARDNAME]

	def __repr__(self):
		return "<%s (%r)>" % (self.__class__.__name__, self.__str__())

	def __eq__(self, other):
		if isinstance(other, BaseCard):
			return self.id.__eq__(other.id)
		elif isinstance(other, str):
			return self.id.__eq__(other)
		return super().__eq__(other)

	@property
	def game(self):
		return self.controller.game

	##
	# Tag properties

	@property
	def maxHealth(self):
		return self.getIntProperty(GameTag.HEALTH)

	@property
	def health(self):
		return max(0, self.maxHealth - self.damage)

	@health.setter
	def health(self, value):
		self.tags[GameTag.HEALTH] = value

	@property
	def extraHealth(self):
		return sum(slot.getIntProperty(GameTag.HEALTH) for slot in self.slots)

	id = _TAG(GameTag.CARD_ID, None)
	cardClass = _TAG(GameTag.CLASS, CardClass.INVALID)
	type = _TAG(GameTag.CARDTYPE, CardType.INVALID)
	aura = _TAG(GameTag.AURA, False)
	controller = _TAG(GameTag.CONTROLLER, None)
	exhausted = _TAG(GameTag.EXHAUSTED, False)
	hasDeathrattle = _PROPERTY(GameTag.DEATHRATTLE, False)

	isValidTarget = targeting.isValidTarget

	@property
	def zone(self):
		return self.tags.get(GameTag.ZONE)

	@zone.setter
	def zone(self, value):
		self._setZone(value)

	def _setZone(self, value):
		old = self.zone
		logging.debug("%r moves from %r to %r" % (self, old, value))
		caches = {
			Zone.HAND: self.controller.hand,
			Zone.DECK: self.controller.deck,
		}
		if caches.get(old) is not None:
			caches[old].remove(self)
		if caches.get(value) is not None:
			caches[value].append(self)
		self.setTag(GameTag.ZONE, value)

	##
	# Properties affected by slots

	@property
	def atk(self):
		ret = self.getIntProperty(GameTag.ATK)
		ret = self.attributeScript("atk", ret)
		return max(0, ret)

	@atk.setter
	def atk(self, value):
		self.tags[GameTag.ATK] = value

	@property
	def deathrattles(self):
		ret = []
		if not self.hasDeathrattle:
			return ret
		if hasattr(self.data, "deathrattle"):
			ret.append(self.data.deathrattle)
		for buff in self.buffs:
			if buff.hasDeathrattle and hasattr(buff.data, "deathrattle"):
				ret.append(buff.data.deathrattle)
		if self.extraDeathrattles:
			ret = ret + ret
		return ret

	def destroy(self):
		logging.info("%r dies" % (self))
		inPlay = self.zone == Zone.PLAY
		self.zone = Zone.GRAVEYARD
		if not inPlay:
			return
		for deathrattle in self.deathrattles:
			logging.info("Triggering Deathrattle for %r" % (self))
			deathrattle(self)
		self.clearBuffs()
		self.game.broadcast("CARD_DESTROYED", self)

	##
	# Events

	events = [
		"UPDATE",
		"TURN_BEGIN", "TURN_END",
		"OWN_TURN_BEGIN", "OWN_TURN_END",
		"MINION_SUMMON", "OWN_MINION_SUMMON",
		"MINION_DESTROY", "OWN_MINION_DESTROY",
		"CARD_PLAYED", "OWN_CARD_PLAYED",
		"AFTER_OWN_CARD_PLAYED", "AFTER_SELF_CARD_PLAYED",
		"BEFORE_ATTACK", "BEFORE_SELF_ATTACK", "SELF_ATTACK",
		"ATTACK",
		"OWN_DAMAGE", "SELF_DAMAGE",
		"HEAL", "OWN_HEAL", "SELF_HEAL",
		"OWN_SECRET_REVEAL",
	]

	def summon(self):
		for aura in self.data.auras:
			aura = Aura(aura)
			aura.source = self
			aura.controller = self.controller
			aura.summon()
			logging.info("Aura %r suddenly appears" % (aura))
			self._auras.append(aura)

	def buff(self, target, buff, **kwargs):
		"""
		Summon \a buff and apply it to \a target
		If keyword arguments are given, attempt to set the given
		values to the buff. Example:
		player.buff(target, health=random.randint(1, 5))
		NOTE: Any Card can buff any other Card. The controller of the
		Card that buffs the target becomes the controller of the buff.
		"""
		ret = self.controller.summon(buff)
		ret.apply(target)
		for k, v in kwargs.items():
			setattr(ret, k, v)
		return ret


class PlayableCard(BaseCard):
	freeze = _TAG(GameTag.FREEZE, False)
	hasCombo = _TAG(GameTag.COMBO, False)
	rarity = _TAG(GameTag.RARITY, Rarity.INVALID)
	overload = _TAG(GameTag.RECALL, 0)
	target = _TAG(GameTag.CARD_TARGET, None)
	windfury = _PROPERTY(GameTag.WINDFURY, False)

	def __init__(self, id, data):
		super().__init__(id, data)
		self.buffs = CardList()

	@property
	def baseCost(self):
		return self.data.tags.get(GameTag.COST, 0)

	@property
	def cost(self):
		ret = self.getIntProperty(GameTag.COST)
		ret = self.attributeScript("cost", ret)
		return max(0, ret)

	@cost.setter
	def cost(self, value):
		self.setTag(GameTag.COST, value)

	@property
	def dead(self):
		return self.zone == Zone.GRAVEYARD

	@property
	def hasBattlecry(self):
		return hasattr(self.data, "action")

	@property
	def poweredUp(self):
		"""
		Returns True whether the card is "powered up".
		Currently, this only applies to some cards which require a minion with a
		specific race on the field.
		"""
		for req in self.data.powerUpRequirements:
			for minion in self.controller.field:
				if minion.race == req:
					return True
		return False

	@property
	def entities(self):
		return chain([self], self.slots)

	@property
	def slots(self):
		return self.buffs

	def action(self):
		kwargs = {}
		if self.target:
			kwargs["target"] = self.target
		elif PlayReq.REQ_TARGET_IF_AVAILABLE in self.requirements:
			logging.info("%r has no target, action exits early" % (self))
			return
		if self.hasCombo and self.controller.combo:
			logging.info("Activating %r combo targeting %r" % (self, self.target))
			func = self.data.combo
		elif self.hasBattlecry:
			logging.info("Activating %r action targeting %r" % (self, self.target))
			func = self.data.action
		else:
			return
		func(self, **kwargs)

	def clearBuffs(self):
		if self.buffs:
			logging.info("Clearing buffs from %r" % (self))
			for buff in self.buffs[:]:
				buff.destroy()

	def discard(self):
		logging.info("Discarding %r" % (self))
		self.zone = Zone.GRAVEYARD

	def heal(self, target, amount):
		logging.info("%r heals %r for %i" % (self, target, amount))
		# Note that undamaged targets do not receive heals
		if target.damage:
			self.game.broadcast("HEAL", self, target, amount)

	def hit(self, target, amount):
		if target.immune:
			logging.info("%r is immune to %i damage from %r" % (target, amount, self))
			return
		logging.info("%r hits %r for %i" % (self, target, amount))
		self.game.broadcast("DAMAGE", self, target, amount)

	def isPlayable(self):
		if self.controller.mana < self.cost:
			return False
		if PlayReq.REQ_TARGET_TO_PLAY in self.data.requirements:
			if not self.targets:
				return False
		if len(self.controller.opponent.field) < self.data.requirements.get(PlayReq.REQ_MINIMUM_ENEMY_MINIONS, 0):
			return False
		if len(self.controller.game.board) < self.data.requirements.get(PlayReq.REQ_MINIMUM_TOTAL_MINIONS, 0):
			return False
		if PlayReq.REQ_ENTIRE_ENTOURAGE_NOT_IN_PLAY in self.data.requirements:
			entourage = list(self.data.entourage)
			for minion in self.controller.field:
				if minion.id in entourage:
					entourage.remove(minion.id)
			if not entourage:
				return False
		return True

	def play(self, target=None, choose=None):
		"""
		Helper for Player.play(card)
		"""
		assert self.zone != Zone.PLAY
		self.controller.play(self, target, choose)

	def hasTarget(self):
		if self.hasCombo and PlayReq.REQ_TARGET_FOR_COMBO in self.data.requirements and self.controller.combo:
			return True
		if PlayReq.REQ_TARGET_IF_AVAILABLE in self.data.requirements:
			return bool(self.targets)
		return PlayReq.REQ_TARGET_TO_PLAY in self.data.requirements

	@property
	def targets(self):
		full_board = self.game.board + [self.controller.hero, self.controller.opponent.hero]
		return [card for card in full_board if self.isValidTarget(card)]

	def OWN_TURN_BEGIN(self):
		self.exhausted = False


class Character(PlayableCard):
	race = _TAG(GameTag.CARDRACE, Race.INVALID)
	frozen = _TAG(GameTag.FROZEN, False)
	immune = _PROPERTY(GameTag.CANT_BE_DAMAGED, False)
	minHealth = _PROPERTY(GameTag.HEALTH_MINIMUM, 0)
	numAttacks = _TAG(GameTag.NUM_ATTACKS_THIS_TURN, 0)
	poisonous = _TAG(GameTag.POISONOUS, False)
	attacking = _TAG(GameTag.ATTACKING, False)
	defending = _TAG(GameTag.DEFENDING, False)
	shouldExitCombat = _TAG(GameTag.SHOULDEXITCOMBAT, False)

	def canAttack(self):
		if self.tags.get(GameTag.CANT_ATTACK, False):
			return False
		if self.windfury:
			if self.numAttacks >= 2:
				return False
		elif self.numAttacks >= 1:
			return False
		if self.atk == 0:
			return False
		if self.exhausted and not self.charge:
			return False
		if self.frozen:
			return False
		return True

	def attack(self, target):
		assert target.zone == Zone.PLAY
		assert self.controller.currentPlayer
		self.game.attack(self, target)

	def destroy(self):
		if self.attacking:
			self.shouldExitCombat = True
		super().destroy()

	@property
	def damage(self):
		return self.tags.get(GameTag.DAMAGE, 0)

	@damage.setter
	def damage(self, amount):
		amount = max(0, amount)
		if amount < self.damage:
			logging.info("%r healed for %i health" % (self, self.damage - amount))
		elif amount == self.damage:
			logging.info("%r receives a no-op health change" % (self))
		else:
			logging.info("%r damaged for %i health" % (self, amount - self.damage))

		if self.minHealth:
			logging.info("%r has HEALTH_MINIMUM of %i", self, self.minHealth)
			amount = min(amount, self.maxHealth - self.minHealth)

		self.setTag(GameTag.DAMAGE, amount)

	@property
	def extraAtk(self):
		return sum(slot.getIntProperty(GameTag.ATK) for slot in self.slots)

	def OWN_TURN_BEGIN(self):
		self.numAttacks = 0
		super().OWN_TURN_BEGIN()

	def OWN_TURN_END(self):
		if self.frozen and not self.numAttacks:
			self.frozen = False

	def SELF_DAMAGE(self, source, amount):
		self.damage += amount

		if source.freeze:
			logging.info("%r is frozen by %r" % (self, source))
			self.frozen = True

		# FIXME this should happen in a separate tick
		if not self.health:
			self.destroy()

	def SELF_HEAL(self, source, amount):
		self.damage -= amount

	def silence(self):
		logging.info("%r has been silenced" % (self))
		for aura in self._auras:
			aura.destroy()
		self.clearBuffs()
		tags = (
			GameTag.CANT_ATTACK,
			GameTag.DIVINE_SHIELD,
			GameTag.FROZEN,
			GameTag.POISONOUS,
			GameTag.STEALTH,
			GameTag.TAUNT,
			GameTag.WINDFURY,
		)
		for tag in tags:
			if tag in self.tags:
				logging.info("Silencing tag %r on %r" % (tag, self))
				del self.tags[tag]

		# Wipe the event listeners and keep only those of the card itself
		self._registerEvents()
		self.silenced = True


class Hero(Character):
	armor = _TAG(GameTag.ARMOR, 0)

	def __init__(self, id, data):
		super().__init__(id, data)
		self.weapon = None

	@property
	def slots(self):
		ret = super().slots[:]
		if self.weapon:
			ret.append(self.weapon)
		return ret

	@property
	def entities(self):
		return chain([self, self.power], self.slots)

	def SELF_DAMAGE(self, source, amount):
		if self.armor:
			newAmount = max(0, amount - self.armor)
			self.armor -= min(self.armor, amount)
			amount = newAmount
		super().SELF_DAMAGE(source, amount)

	def destroy(self):
		raise GameOver("%s wins!" % (self.controller.opponent))

	def summon(self):
		super().summon()
		self.controller.hero = self
		self.controller.summon(self.data.power)


class Minion(Character):
	divineShield = _TAG(GameTag.DIVINE_SHIELD, False)
	adjacentBuff = _TAG(GameTag.ADJACENT_BUFF, False)
	enrage = _TAG(GameTag.ENRAGED, False)
	silenced = _TAG(GameTag.SILENCED, False)
	spellPower = _TAG(GameTag.SPELLPOWER, 0)

	chromatic = _PROPERTY(GameTag.CANT_BE_TARGETED_BY_ABILITIES, False)
	extraDeathrattles = _PROPERTY(GameTag.EXTRA_DEATHRATTLES, False)
	stealthed = _PROPERTY(GameTag.STEALTH, False)
	taunt = _PROPERTY(GameTag.TAUNT, False)

	def __init__(self, id, data):
		super().__init__(id, data)
		self._enrage = None

	@property
	def charge(self):
		ret = self.getBoolProperty(GameTag.CHARGE)
		return ret or self.attributeScript("charge", ret)

	@charge.setter
	def charge(self, value):
		self.setTag(GameTag.CHARGE, value)

	@property
	def adjacentMinions(self):
		assert self.zone is Zone.PLAY, self.zone
		ret = CardList()
		index = self.controller.field.index(self)
		left = self.controller.field[:index]
		right = self.controller.field[index+1:]
		if left:
			ret.append(left[-1])
		if right:
			ret.append(right[0])
		return ret

	@property
	def slots(self):
		slots = super().slots[:]
		if self.enraged:
			slots.append(self._enrage)
		return slots

	def attributeScript(self, attr, value):
		if self.silenced:
			return value
		return super().attributeScript(attr, value)

	@property
	def enraged(self):
		return self.enrage and self.damage

	def _setZone(self, value):
		if self.zone == Zone.PLAY:
			logging.info("%r is removed from the field" % (self))
			self.controller.field.remove(self)
			# Remove any aura the minion gives
			for aura in self._auras:
				aura.destroy()
			if self.damage:
				self.damage = 0
		super()._setZone(value)

	def bounce(self):
		logging.info("%r is bounced back to %s's hand" % (self, self.controller))
		if len(self.controller.hand) == self.controller.maxHandSize:
			logging.info("%s's hand is full and bounce fails" % (self.controller))
			self.destroy()
		else:
			if self.attacking:
				self.shouldExitCombat = True
			self.zone = Zone.HAND

	def hit(self, target, amount):
		super().hit(target, amount)
		if self.stealthed:
			self.stealthed = False

	def morph(self, id):
		into = Card(id)
		into.controller = self.controller
		for buff in self.buffs:
			# TODO: buff.setAside() instead
			buff.destroy()
		self.tags = into.tags.copy()

	def SELF_DAMAGE(self, source, amount):
		if self.divineShield:
			self.divineShield = False
			logging.info("%r's divine shield prevents %i damage. Divine shield fades." % (self, amount))
			return
		if isinstance(source, Minion) and source.poisonous:
			logging.info("%r is destroyed because of %r is poisonous" % (self, source))
			self.destroy()

		if self.enrage and not self._enrage:
			self._enrage = Enrage(self.data.enrageTags)
			self._enrage.controller = self.controller

		super().SELF_DAMAGE(source, amount)

	def SELF_HEAL(self, source, amount):
		super().SELF_HEAL(source, amount)
		if self._enrage and not self.enraged:
			self._enrage = None

	def isPlayable(self):
		playable = super().isPlayable()
		if len(self.controller.field) >= self.game.MAX_MINIONS_ON_FIELD:
			return False
		return playable

	def summon(self):
		super().summon()
		if len(self.controller.field) >= self.game.MAX_MINIONS_ON_FIELD:
			return
		self.controller.field.append(self)
		self.game.broadcast("MINION_SUMMON", self.controller, self)
		self.exhausted = True


class Spell(PlayableCard):
	immuneToSpellpower = _TAG(GameTag.ImmuneToSpellpower, False)

	def hit(self, target, amount):
		if not self.immuneToSpellpower:
			amount += self.controller.spellPower
		super().hit(target, amount)


class Secret(Spell):
	def _setZone(self, value):
		if self.zone == Zone.SECRET:
			self.controller.secrets.remove(self)
		if value == Zone.SECRET:
			self.controller.secrets.append(self)
		super()._setZone(value)

	def isPlayable(self):
		# secrets are all unique
		if self.controller.secrets.contains(self):
			return False
		return super().isPlayable()

	def summon(self):
		super().summon()
		self.zone = Zone.SECRET

	def reveal(self):
		logging.info("Revealing secret %r" % (self))
		self.game.broadcast("SECRET_REVEAL", self, self.controller)
		self.destroy()


class Enchantment(BaseCard):
	oneTurnEffect = _TAG(GameTag.OneTurnEffect, False)
	owner = _TAG(GameTag.ATTACHED, None)
	creator = _TAG(GameTag.CREATOR, None)

	@property
	def slots(self):
		return []

	def apply(self, target):
		logging.info("Applying %r to %r" % (self, target))
		self.owner = target
		target.buffs.append(self)
		if target.type == CardType.WEAPON:
			# HACK
			# We don't want to have a full-fledged damage system for durability.
			# However, we want to be able to specify durability in buffs.
			# This should be done elsewhere, preferably in the Weapon class.
			durability = self.tags.get(GameTag.DURABILITY, 0)
			if durability:
				target.durability += durability
		if hasattr(self.data, "apply"):
			self.data.apply(self, target)

	def destroy(self):
		logging.info("Destroying buff %r from %r" % (self, self.owner))
		self.owner.buffs.remove(self)
		if hasattr(self.data, "destroy"):
			self.data.destroy(self)
		for aura in self._auras:
			aura.destroy()

	def setAtk(self, value):
		"Helper to set a character's atk to \a value through an Enchantment"
		logging.info("Setting %r's Atk to %i through %r" % (self.owner, value, self))
		for buff in self.owner.buffs:
			# Nullify all OneTurnEffect atk buffs.
			# This is needed because of things like Abusive Seargent + Humility
			# which results in negative atk otherwise.
			# @mischanix thinks this is handled through an internal "attack value
			# this turn" tag. Who's right? Find out in Season 2.
			if buff.oneTurnEffect and buff.atk:
				buff.atk = 0
		self.atk = -self.owner.atk + value

	def setHealth(self, value):
		"Helper to set a character's health to \a value through an Enchantment"
		assert self.owner.health
		logging.info("Setting %r's Health to %i through %r" % (self.owner, value, self))
		self.owner.damage = 0
		self.health = -self.owner.health + value

	def TURN_END(self, *args):
		if self.oneTurnEffect:
			logging.info("Ending One-Turn effect: %r" % (self))
			self.destroy()


class Aura(BaseCard):
	"""
	A virtual Card class which is only for the source of the Enchantment buff on
	targets affected by an aura. It is only internal.
	"""

	def __init__(self, obj):
		id = obj["id"]
		super().__init__(id, getattr(CardDB, id))
		self.requirements = obj["requirements"].copy()
		self._buffed = CardList()
		self._buffs = CardList()
		self._zone = obj["zone"]

	def isValidTarget(self, target):
		return self.source.isValidTarget(target, requirements=self.requirements)

	@property
	def targets(self):
		if self.source.type == CardType.MINION and self.source.adjacentBuff:
			return self.source.adjacentMinions
		if self.zone == Zone.HAND:
			return self.controller.hand + self.controller.opponent.hand
		# XXX The targets are right but we need to get them a cleaner way.
		ret = self.game.player1.field + self.game.player2.field
		if self.controller.hero.weapon:
			ret.append(self.controller.hero.weapon)
		return ret

	def summon(self):
		super().summon()
		self.game.auras.append(self)
		self.zone = self._zone

	def _buff(self, target):
		if self.id:
			buff = self.buff(target, self.id)
		else:
			virtual = Card(id=None, data=self.data)
			virtual.controller = self.controller
			buff = self.buff(target, virtual)
		buff.creator = self
		self._buffs.append(buff)
		self._buffed.append(target)

	def _entityBuff(self, target):
		"Returns the buff created by this aura on \a target"
		for buff in target.buffs:
			if buff.creator is self:
				return buff

	def UPDATE(self):
		for target in self.targets:
			if target.type == CardType.ENCHANTMENT:
				# HACKY: self.targets currently relies on hero entities
				# This includes enchantments so we need to filter them out.
				continue
			if self.isValidTarget(target):
				if not self._entityBuff(target):
					self._buff(target)
		# Make sure to copy the list as it can change during iteration
		for target in self._buffed[:]:
			# Remove auras no longer valid
			if not self.isValidTarget(target):
				buff = self._entityBuff(target)
				if buff:
					buff.destroy()
					self._buffs.remove(buff)
				self._buffed.remove(target)

	def destroy(self):
		logging.info("Removing %r affecting %r" % (self, self._buffed))
		for buff in self._buffs:
			buff.destroy()
		del self._buffed
		self.game.auras.remove(self)


class Enrage(Entity):
	"""
	Virtual Card class for Enrage objects.
	Enrage buffs are just a collection of tags for the enraged Minion's slots.
	"""

	type = None
	events = []
	slots = []

	def __init__(self, tags):
		super().__init__()
		self.tags = tags.copy()

	def __str__(self):
		return "Enrage Buff"


class Weapon(PlayableCard):
	durability = _TAG(GameTag.DURABILITY, 0)

	@durability.setter
	def durability(self, value):
		self.setTag(GameTag.DURABILITY, value)
		if self.durability == 0:
			self.destroy()

	def destroy(self):
		self.controller.hero.weapon = None
		super().destroy()

	def summon(self):
		super().summon()
		if self.controller.hero.weapon:
			self.controller.hero.weapon.destroy()
		self.controller.hero.weapon = self

	def SELF_ATTACK(self, target):
		self.durability -= 1


class HeroPower(PlayableCard):
	def play(self, target=None):
		logging.info("%s plays hero power %r" % (self.controller, self))
		assert self.isPlayable()
		if self.hasTarget():
			assert target
			self.target = target
		self.controller.usedMana += self.cost
		self.action()
		self.exhausted = True
		if self.target:
			self.target = None

	def isPlayable(self):
		playable = super().isPlayable()
		if self.exhausted:
			return False
		return playable

	def summon(self):
		super().summon()
		if hasattr(self.controller.hero, "power"):
			self.controller.hero.power.destroy()
		self.controller.hero.power = self
