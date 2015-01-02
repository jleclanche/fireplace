import json
import logging
import uuid
from itertools import chain
from . import cards as CardDB, targeting
from .exceptions import *
from .entity import Entity
from .enums import CardType, GameTag, PlayReq, Race, Zone
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
		self.id = id
		self.uuid = uuid.uuid4()
		self._aura = None
		self._enrage = None
		self.weapon = None
		self.buffs = CardList()
		self.data = data
		self.tags = data.tags.copy()
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
	def entities(self):
		return chain([self], self.slots)

	@property
	def game(self):
		return self.controller.game

	##
	# Tag properties

	type = _TAG(GameTag.CARDTYPE, CardType.INVALID)
	aura = _TAG(GameTag.AURA, False)
	cost = _TAG(GameTag.COST, 0)
	controller = _TAG(GameTag.CONTROLLER, None)
	exhausted = _TAG(GameTag.EXHAUSTED, False)
	overload = _TAG(GameTag.RECALL, 0)
	windfury = _PROPERTY(GameTag.WINDFURY, False)
	hasCombo = _TAG(GameTag.COMBO, False)
	hasDeathrattle = _PROPERTY(GameTag.DEATHRATTLE, False)

	@property
	def zone(self):
		return self.tags.get(GameTag.ZONE)

	@zone.setter
	def zone(self, value):
		self.moveToZone(self.zone, value)
		self.tags[GameTag.ZONE] = value

	@property
	def baseCost(self):
		return self.data.tags.get(GameTag.COST, 0)

	##
	# Properties affected by slots

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
	def targets(self):
		full_board = self.game.board + [self.controller.hero, self.controller.opponent.hero]
		return [card for card in full_board if self.isValidTarget(card)]

	isValidTarget = targeting.isValidTarget

	def hasTarget(self):
		if self.hasCombo and PlayReq.REQ_TARGET_FOR_COMBO in self.data.requirements and self.controller.combo:
			return True
		return PlayReq.REQ_TARGET_TO_PLAY in self.data.requirements or \
			PlayReq.REQ_TARGET_IF_AVAILABLE in self.data.requirements

	@property
	def slots(self):
		return self.buffs

	def action(self, target=None):
		kwargs = {}
		if self.hasTarget():
			assert target
			kwargs["target"] = target
		if self.hasCombo and self.controller.combo:
			logging.info("Activating %r combo targeting %r" % (self, target))
			func = self.data.combo
		else:
			if not hasattr(self.data, "action"):
				return
			logging.info("Activating %r action targeting %r" % (self, target))
			func = self.data.action
		func(self, **kwargs)

	def heal(self, target, amount):
		logging.info("%r heals %r for %i" % (self, target, amount))
		# Note that undamaged targets do not receive heals
		if target.damage:
			self.game.broadcast("HEAL", self, target, amount)

	def hit(self, target, amount):
		logging.info("%r hits %r for %i" % (self, target, amount))
		self.game.broadcast("DAMAGE", self, target, amount)

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
		for buff in self.buffs[:]:
			buff.destroy()
		self.game.broadcast("CARD_DESTROYED", self)

	def moveToZone(self, old, new):
		logging.debug("%r moves from %r to %r" % (self, old, new))
		caches = {
			Zone.HAND: self.controller.hand,
			Zone.DECK: self.controller.deck,
		}
		if caches.get(old) is not None:
			caches[old].remove(self)
		if caches.get(new) is not None:
			caches[new].append(self)

	##
	# Events

	events = [
		"UPDATE",
		"TURN_BEGIN", "TURN_END",
		"OWN_TURN_BEGIN", "OWN_TURN_END",
		"MINION_SUMMON", "OWN_MINION_SUMMON",
		"MINION_DESTROY", "OWN_MINION_DESTROY",
		"CARD_PLAYED", "OWN_CARD_PLAYED", "AFTER_OWN_CARD_PLAYED",
		"BEFORE_ATTACK", "BEFORE_SELF_ATTACK", "SELF_ATTACK",
		"ATTACK",
		"OWN_DAMAGE", "SELF_DAMAGE",
		"HEAL", "OWN_HEAL", "SELF_HEAL"
	]

	def OWN_TURN_BEGIN(self):
		self.exhausted = False

	def discard(self):
		logging.info("Discarding %r" % (self))
		self.zone = Zone.GRAVEYARD

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

	def play(self, target=None):
		"""
		Helper for Player.play(card)
		"""
		assert self.zone != Zone.PLAY
		self.controller.play(self, target)

	def summon(self):
		if self.aura:
			if self.aura == 1:
				logging.warning("Undefined aura for %r", self)
				return
			self._aura = Aura(id=self.data.Aura.id, data=self.data.Aura)
			self._aura.source = self
			self._aura.controller = self.controller
			self._aura.summon()
			logging.info("Aura %r suddenly appears" % (self._aura))

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


class Character(BaseCard):
	race = _TAG(GameTag.CARDRACE, Race.INVALID)
	frozen = _TAG(GameTag.FROZEN, False)
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

		self.setTag(GameTag.DAMAGE, amount)

	def OWN_TURN_BEGIN(self):
		self.numAttacks = 0
		super().OWN_TURN_BEGIN()

	def OWN_TURN_END(self):
		if self.frozen and not self.numAttacks:
			self.frozen = False

	def SELF_DAMAGE(self, source, amount):
		self.damage += amount

		# FIXME this should happen in a separate tick
		if not self.health:
			self.destroy()

	def SELF_HEAL(self, source, amount):
		self.damage -= amount

	def silence(self):
		logging.info("%r has been silenced" % (self))
		if self._aura:
			self._aura.destroy()
		for buff in self.buffs[:]:
			buff.destroy()
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


class Hero(Character):
	armor = _TAG(GameTag.ARMOR, 0)

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
	spellPower = _TAG(GameTag.SPELLPOWER, 0)

	charge = _PROPERTY(GameTag.CHARGE, False)
	chromatic = _PROPERTY(GameTag.CANT_BE_TARGETED_BY_ABILITIES, False)
	extraDeathrattles = _PROPERTY(GameTag.EXTRA_DEATHRATTLES, False)
	stealthed = _PROPERTY(GameTag.STEALTH, False)
	taunt = _PROPERTY(GameTag.TAUNT, False)

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
		if self._enrage:
			slots.append(self._enrage)
		return slots

	def bounce(self):
		logging.info("%r is bounced back to %s's hand" % (self, self.controller))
		if len(self.controller.hand) == self.controller.MAX_HAND:
			logging.info("%s's hand is full and bounce fails" % (self.controller))
			self.destroy()
		else:
			self.zone = Zone.HAND

	def hit(self, target, amount):
		super().hit(target, amount)
		if self.stealthed:
			self.stealthed = False

	def moveToZone(self, old, new):
		if old == Zone.PLAY:
			logging.info("%r is removed from the field" % (self))
			self.controller.field.remove(self)
			# Remove any aura the minion gives
			if self._aura:
				self._aura.destroy()
			if self.damage:
				self.damage = 0
		super().moveToZone(old, new)

	def SELF_DAMAGE(self, source, amount):
		if self.divineShield:
			self.divineShield = False
			logging.info("%r's divine shield prevents %i damage. Divine shield fades." % (self, amount))
			return
		if isinstance(source, Minion) and source.poisonous:
			logging.info("%r is destroyed because of %r is poisonous" % (self, source))
			self.destroy()

		if self.enrage and not self._enrage:
			self._enrage = Enrage(id=None, data=self.enrage)
			self._enrage.controller = self.controller
			self._enrage.summon()

		super().SELF_DAMAGE(source, amount)

	def SELF_HEAL(self, source, amount):
		super().SELF_HEAL(source, amount)
		if not self.damage and self._enrage:
			self._enrage.destroy()
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


class Spell(BaseCard):
	immuneToSpellpower = _TAG(GameTag.ImmuneToSpellpower, False)

	def hit(self, target, amount):
		if not self.immuneToSpellpower:
			amount += self.controller.spellPower
		super().hit(target, amount)


class Secret(BaseCard):
	def isPlayable(self):
		# secrets are all unique
		if self.controller.secrets.contains(self):
			return False
		return super().isPlayable()

	def summon(self):
		super().summon()
		self.zone = Zone.SECRET

	def moveToZone(self, old, new):
		if old == Zone.SECRET:
			self.controller.secrets.remove(self)
		if new == Zone.SECRET:
			self.controller.secrets.append(self)
		super().moveToZone(old, new)

	def reveal(self):
		logging.info("Revealing secret %r" % (self))
		self.game.broadcast("SECRET_REVEAL", self, self.controller)
		self.destroy()


class Enchantment(BaseCard):
	oneTurnEffect = _TAG(GameTag.OneTurnEffect, False)
	owner = _TAG(GameTag.ATTACHED, None)

	def apply(self, target):
		logging.info("Applying %r to %r" % (self, target))
		self.owner = target
		target.buffs.append(self)
		if hasattr(self.data, "apply"):
			self.data.apply(self, target)

	def destroy(self):
		logging.info("Destroying buff %r from %r" % (self, self.owner))
		self.owner.buffs.remove(self)
		if hasattr(self.data, "destroy"):
			self.data.destroy(self)

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

	def __init__(self, id, data):
		super().__init__(id, data)
		self._buffed = CardList()
		self._buffs = CardList()

	@property
	def targets(self):
		return self.controller.getTargets(self.data.targeting)

	def summon(self):
		super().summon()
		self.game.auras.append(self)
		self.zone = Zone.PLAY

	def isValidTarget(self, card):
		if self.source.type == CardType.MINION and self.source.adjacentBuff:
			if card not in self.source.adjacentMinions:
				return False
		if card not in self.targets:
			return False
		if hasattr(self.data, "isValidTarget"):
			return self.data.isValidTarget(self, card)
		return True

	def _buff(self, target):
		if self.id:
			buff = self.buff(target, self.id)
		else:
			virtual = Card(id=None, data=self.data)
			virtual.controller = self.controller
			buff = self.buff(target, virtual)
		self._buffs.append(buff)
		self._buffed.append(target)

	def UPDATE(self):
		for target in self.targets:
			if self.isValidTarget(target):
				if not target in self._buffed:
					self._buff(target)
		for target in self._buffed:
			# Remove auras no longer valid
			if not self.isValidTarget(target):
				for buff in self._buffs:
					if buff in target.buffs:
						buff.destroy()
						self._buffs.remove(buff)
						self._buffed.remove(target)
						break

	def destroy(self):
		logging.info("Removing %r affecting %r" % (self, self._buffed))
		for buff in self._buffs:
			buff.destroy()
		del self._buffed
		self.game.auras.remove(self)


class Enrage(BaseCard):
	"""
	Virtual Card class for Enrage objects.
	Enrage buffs behave like regular cards but do not actually have
	ids or are present in the game files, so hackery.
	"""
	def __str__(self):
		return "Enrage Buff"

	@property
	def slots(self):
		return []

	def destroy(self):
		# Bit hacky. Need a design where we don't duplicate this.
		if self._aura:
			self._aura.destroy()

	def moveToZone(self, old, new):
		pass


class Weapon(BaseCard):
	@property
	def durability(self):
		return self.tags.get(GameTag.DURABILITY, 0)

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


class HeroPower(BaseCard):
	def play(self, target=None):
		logging.info("%s plays hero power %r" % (self.controller, self))
		assert self.isPlayable()
		self.controller.usedMana += self.cost
		self.action(target)
		self.exhausted = True

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
