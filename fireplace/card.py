import json
import logging
from itertools import chain
from . import cards as CardDB, targeting
from .exceptions import *
from .entity import Entity, booleanProperty, intProperty
from .enums import AuraType, CardClass, CardType, PlayReq, Race, Rarity, Zone
from .managers import (CardManager, PlayableCardManager, CharacterManager,
	MinionManager, SpellManager, WeaponManager, EnchantmentManager)
from .utils import CardList


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
	}[data.type]
	if subclass is Spell and data.secret:
		subclass = Secret
	return subclass(id, data)


class BaseCard(Entity):
	Manager = CardManager
	hasDeathrattle = booleanProperty("hasDeathrattle")
	atk = intProperty("atk")
	maxHealth = intProperty("maxHealth")
	cost = intProperty("cost")

	def __init__(self, id, data):
		assert data
		super().__init__()
		self._auras = []
		self.data = data
		self.requirements = data.requirements.copy()
		self.id = id
		self.controller = None
		self.aura = False
		self.silenced = False
		self.secret = data.secret
		self.spellpower = 0
		self.tags.update(data.tags)

		for event in self.events:
			if hasattr(data.scripts, event):
				if event not in self._eventListeners:
					self._eventListeners[event] = []
				# A bit of magic powder to pass the Card object as self to the Card defs
				func = getattr(data.scripts, event)
				zone = getattr(func, "zone", Zone.PLAY)
				_func = lambda *args: func(self, *args)
				_func.zone = getattr(func, "zone", Zone.PLAY)
				self._eventListeners[event].append(_func)

	def __str__(self):
		return self.name

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

	@property
	def zone(self):
		return getattr(self, "_zone", Zone.INVALID)

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
		self._zone = value

		if value == Zone.PLAY:
			for aura in self.data.auras:
				aura = Aura(aura, source=self)
				aura.summon()
				self._auras.append(aura)

	def destroy(self):
		logging.info("%r dies" % (self))
		inPlay = self.zone == Zone.PLAY
		self.zone = Zone.GRAVEYARD
		if not inPlay:
			return
		self.game.broadcast("CARD_DESTROYED", self)

	def summon(self):
		logging.info("Summoning %r", self)
		self.zone = Zone.PLAY

	##
	# Events

	events = [
		"TURN_BEGIN", "TURN_END",
		"OWN_TURN_BEGIN", "OWN_TURN_END",
		"SELF_CARD_DESTROYED",
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
	Manager = PlayableCardManager
	windfury = booleanProperty("windfury")

	def __init__(self, id, data):
		self.buffs = CardList()
		self.exhausted = False
		self.freeze = False
		self.hasBattlecry = False
		self.hasCombo = False
		self.overload = 0
		self.target = None
		super().__init__(id, data)

	@property
	def dead(self):
		return self.zone == Zone.GRAVEYARD or self.toBeDestroyed

	@property
	def deathrattles(self):
		ret = []
		if not self.hasDeathrattle:
			return ret
		if hasattr(self.data.scripts, "deathrattle"):
			ret.append(self.data.scripts.deathrattle)
		for buff in self.buffs:
			if buff.hasDeathrattle and hasattr(buff.data.scripts, "deathrattle"):
				ret.append(buff.data.scripts.deathrattle)
		return ret

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
			func = self.data.scripts.combo
		elif hasattr(self.data.scripts, "action"):
			logging.info("Activating %r action targeting %r" % (self, self.target))
			func = self.data.scripts.action
		else:
			return
		func(self, **kwargs)

	def clearBuffs(self):
		if self.buffs:
			logging.info("Clearing buffs from %r" % (self))
			for buff in self.buffs[:]:
				buff.destroy()
				if buff.creator:
					# Clean up the buff from its source auras
					buff.creator._buffs.remove(buff)

	def discard(self):
		logging.info("Discarding %r" % (self))
		self.zone = Zone.GRAVEYARD

	def heal(self, target, amount):
		logging.info("%r heals %r for %i" % (self, target, amount))
		if self.controller.outgoingHealingAdjustment:
			# "healing as damage" (hack-ish)
			return self.hit(target, amount)
		elif target.damage:
			# Note that undamaged targets do not receive heals
			self.game.broadcast("HEAL", self, target, amount)

	def hit(self, target, amount):
		if getattr(target, "immune", False):
			logging.info("%r is immune to %i damage from %r" % (target, amount, self))
			return
		logging.info("%r hits %r for %i" % (self, target, amount))
		self.game.broadcast("DAMAGE", self, target, amount)

	def isPlayable(self):
		if self.controller.mana < self.cost:
			return False
		if PlayReq.REQ_TARGET_TO_PLAY in self.requirements:
			if not self.targets:
				return False
		if len(self.controller.opponent.field) < self.requirements.get(PlayReq.REQ_MINIMUM_ENEMY_MINIONS, 0):
			return False
		if len(self.controller.game.board) < self.requirements.get(PlayReq.REQ_MINIMUM_TOTAL_MINIONS, 0):
			return False
		if PlayReq.REQ_ENTIRE_ENTOURAGE_NOT_IN_PLAY in self.requirements:
			entourage = list(self.data.entourage)
			for minion in self.controller.field:
				if minion.id in entourage:
					entourage.remove(minion.id)
			if not entourage:
				return False
		if PlayReq.REQ_WEAPON_EQUIPPED in self.requirements:
			if not self.controller.weapon:
				return False
		return True

	def play(self, target=None, choose=None):
		"""
		Helper for Player.play(card)
		"""
		assert self.zone != Zone.PLAY
		self.controller.play(self, target, choose)

	def hasTarget(self):
		if self.hasCombo and PlayReq.REQ_TARGET_FOR_COMBO in self.requirements and self.controller.combo:
			return True
		if PlayReq.REQ_TARGET_IF_AVAILABLE in self.requirements:
			return bool(self.targets)
		return PlayReq.REQ_TARGET_TO_PLAY in self.requirements

	@property
	def targets(self):
		full_board = self.game.board + [self.controller.hero, self.controller.opponent.hero]
		return [card for card in full_board if targeting.isValidTarget(self, card)]

	def SELF_CARD_DESTROYED(self):
		for deathrattle in self.deathrattles:
			logging.info("Triggering Deathrattle for %r" % (self))
			deathrattle(self)
			if self.controller.extraDeathrattles:
				logging.info("Triggering Deathrattle for %r again", self)
				deathrattle(self)
		self.clearBuffs()

	def OWN_TURN_BEGIN(self):
		self.exhausted = False


class Character(PlayableCard):
	Manager = CharacterManager
	minHealth = booleanProperty("minHealth")
	immune = booleanProperty("immune")

	silenceableAttributes = (
		"aura", "cantAttack", "cantBeTargetedByAbilities", "cantBeTargetedByHeroPowers",
		"charge", "divineShield", "enrage", "frozen", "poisonous", "stealthed", "taunt",
		"windfury",
	)

	def __init__(self, *args):
		self.attacking = False
		self.frozen = False
		self.cantAttack = False
		self.cantBeTargetedByAbilities = False
		self.cantBeTargetedByHeroPowers = False
		self.race = Race.INVALID
		self.shouldExitCombat = False
		super().__init__(*args)

	@property
	def attackable(self):
		return not self.immune

	@property
	def attackTargets(self):
		targets = [self.controller.opponent.hero] + self.controller.opponent.field
		taunts = []
		for target in self.controller.opponent.field:
			if target.taunt:
				taunts.append(target)
		ret = []
		for target in (taunts if taunts else self.controller.opponent.field):
			if target.attackable:
				ret.append(target)
		if not taunts and self.controller.opponent.hero.attackable:
			ret.append(self.controller.opponent.hero)
		return ret

	def canAttack(self):
		if self.cantAttack:
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

	def summon(self):
		super().summon()
		self.numAttacks = 0

	@property
	def damage(self):
		return getattr(self, "_damage", 0)

	@damage.setter
	def damage(self, amount):
		amount = max(0, amount)
		dmg = self.damage
		if amount < dmg:
			logging.info("%r healed for %i health" % (self, dmg - amount))
		elif amount == dmg:
			logging.info("%r receives a no-op health change" % (self))
		else:
			logging.info("%r damaged for %i health" % (self, amount - dmg))

		if self.minHealth:
			logging.info("%r has HEALTH_MINIMUM of %i", self, self.minHealth)
			amount = min(amount, self.maxHealth - self.minHealth)

		self._damage = amount

	@property
	def health(self):
		return max(0, self.maxHealth - self.damage)

	@property
	def targets(self):
		if self.zone == Zone.PLAY:
			return self.attackTargets
		return super().targets

	@property
	def toBeDestroyed(self):
		return self.health == 0

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

	def SELF_HEAL(self, source, amount):
		self.damage -= amount

	def silence(self):
		logging.info("%r has been silenced" % (self))
		for aura in self._auras:
			aura.destroy()
		self.clearBuffs()

		for attr in self.silenceableAttributes:
			if getattr(self, attr):
				setattr(self, attr, False)

		# Wipe the event listeners and keep only those of the card itself
		self._registerEvents()
		self.silenced = True


class Hero(Character):
	def __init__(self, id, data):
		self.armor = 0
		super().__init__(id, data)

	@property
	def slots(self):
		ret = super().slots[:]
		if self.controller.weapon and not self.controller.weapon.exhausted:
			ret.append(self.controller.weapon)
		return ret

	@property
	def entities(self):
		ret = [self, self.power]
		if self.controller.weapon:
			ret.append(self.controller.weapon)
		return chain(ret, self.buffs)

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
		self.controller.summon(self.data.heroPower)


class Minion(Character):
	Manager = MinionManager
	charge = booleanProperty("charge")
	stealthed = booleanProperty("stealthed")
	taunt = booleanProperty("taunt")

	def __init__(self, id, data):
		self._enrage = None
		self.adjacentBuff = False
		self.divineShield = False
		self.enrage = False
		self.poisonous = False
		super().__init__(id, data)

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
	def attackable(self):
		if self.stealthed:
			return False
		return super().attackable

	@property
	def slots(self):
		slots = super().slots[:]
		if self.enraged:
			slots.append(self._enrage)
		return slots

	@property
	def enraged(self):
		return self.enrage and self.damage

	def _setZone(self, value):
		if value == Zone.PLAY:
			self.controller.field.append(self)

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
		into = self.game.card(id)
		logging.info("Morphing %r into %r", self, into)
		for buff in self.buffs:
			# TODO: buff.setAside() instead
			buff.destroy()
		self.zone = Zone.REMOVEDFROMGAME
		into.controller = self.controller
		into.zone = Zone.PLAY
		into.linkedCard = self
		return into

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
		if len(self.controller.field) >= self.game.MAX_MINIONS_ON_FIELD:
			return
		super().summon()
		self.game.broadcast("MINION_SUMMON", self.controller, self)
		self.exhausted = True


class Spell(PlayableCard):
	Manager = SpellManager

	def __init__(self, *args):
		self.immuneToSpellpower = False
		super().__init__(*args)

	def hit(self, target, amount):
		if not self.immuneToSpellpower:
			amount += self.controller.spellpower
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
	Manager = EnchantmentManager

	def __init__(self, *args):
		self.creator = None
		self.oneTurnEffect = False
		super().__init__(*args)

	@property
	def slots(self):
		return []

	def apply(self, target):
		logging.info("Applying %r to %r" % (self, target))
		self.owner = target
		if hasattr(self.data.scripts, "apply"):
			self.data.scripts.apply(self, target)
		if hasattr(self.data.scripts, "maxHealth"):
			logging.info("%r removes all damage from %r", self, target)
			target.damage = 0
		target.buffs.append(self)

	def destroy(self):
		logging.info("Destroying buff %r from %r" % (self, self.owner))
		self.owner.buffs.remove(self)
		if hasattr(self.data.scripts, "destroy"):
			self.data.scripts.destroy(self)
		for aura in self._auras:
			aura.destroy()

	def TURN_END(self, *args):
		if self.oneTurnEffect:
			logging.info("Ending One-Turn effect: %r" % (self))
			self.destroy()


class Aura(object):
	"""
	A virtual Card class which is only for the source of the Enchantment buff on
	targets affected by an aura. It is only internal.
	"""

	def __init__(self, obj, source):
		self.id = obj["id"]
		self.source = source
		self.controller = source.controller
		self.requirements = obj["requirements"].copy()
		self._buffed = CardList()
		self._buffs = CardList()
		self._auraType = obj["type"]

	@property
	def game(self):
		return self.source.game

	def isValidTarget(self, target):
		if self._auraType == AuraType.PLAYER_AURA:
			return target == self.controller
		return targeting.isValidTarget(self.source, target, requirements=self.requirements)

	@property
	def targets(self):
		if self._auraType == AuraType.PLAYER_AURA:
			return [self.controller]
		elif self._auraType == AuraType.HAND_AURA:
			return self.controller.hand + self.controller.opponent.hand
		if self.source.type == CardType.MINION and self.source.adjacentBuff:
			return self.source.adjacentMinions
		# XXX The targets are right but we need to get them a cleaner way.
		ret = self.game.player1.field + self.game.player2.field
		if self.controller.weapon:
			ret.append(self.controller.weapon)
		return ret

	def summon(self):
		logging.info("Summoning Aura %r", self)
		self.game.auras.append(self)

	def _buff(self, target):
		buff = self.source.buff(target, self.id)
		buff.creator = self
		self._buffs.append(buff)
		self._buffed.append(target)

	def _entityBuff(self, target):
		"Returns the buff created by this aura on \a target"
		for buff in target.buffs:
			if buff.creator is self:
				return buff

	def update(self):
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
		del self._buffs
		del self._buffed
		self.game.auras.remove(self)


class Enrage(object):
	"""
	Enrage class for Minion.enrageTags
	Enrage buffs are just a collection of tags for the enraged Minion's slots.
	"""

	_eventListeners = {}

	def __init__(self, tags):
		MinionManager(self).update(tags)

	def _getattr(self, attr, i):
		return i + getattr(self, attr, 0)


class Weapon(PlayableCard):
	Manager = WeaponManager

	def __init__(self, *args):
		super().__init__(*args)
		self.damage = 0

	@property
	def durability(self):
		ret = getattr(self, "_durability", 0)
		for slot in self.slots:
			ret += getattr(slot, "durability", 0)
		return max(0, ret - self.damage)

	@durability.setter
	def durability(self, value):
		self._durability = value

	@property
	def toBeDestroyed(self):
		return self.durability == 0

	def destroy(self):
		self.controller.weapon = None
		super().destroy()

	def loseDurability(self, count=1):
		logging.info("%r loses %r durability", self, count)
		self.damage += count

	def summon(self):
		super().summon()
		if self.controller.weapon:
			self.controller.weapon.destroy()
		self.controller.weapon = self

	def SELF_ATTACK(self, target):
		self.loseDurability()

	def OWN_TURN_END(self):
		self.exhausted = True


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
		self.controller.timesHeroPowerUsedThisGame += 1

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
