import logging
from itertools import chain
from . import cards as CardDB, targeting
from .actions import Damage, Deaths, Destroy, Heal, Morph, Play
from .entity import Entity, boolean_property, int_property
from .enums import AuraType, CardType, PlayReq, Race, Zone
from .managers import *
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
	has_deathrattle = boolean_property("has_deathrattle")
	atk = int_property("atk")
	max_health = int_property("max_health")
	cost = int_property("cost")

	def __init__(self, id, data):
		self.data = data
		super().__init__()
		self._auras = []
		self.requirements = data.requirements.copy()
		self.entourage = CardList(self.data.entourage)
		self.id = id
		self.controller = None
		self.aura = False
		self.silenced = False
		self.secret = data.secret
		self.spellpower = 0
		self.turns_in_play = 0
		self.tags.update(data.tags)

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
		self._set_zone(value)

	def _set_zone(self, value):
		old = self.zone
		assert old != value
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
		else:
			for aura in self._auras:
				aura.destroy()

	def summon(self):
		logging.info("Summoning %r", self)
		self.zone = Zone.PLAY

	def buff(self, target, buff, **kwargs):
		"""
		Summon \a buff and apply it to \a target
		If keyword arguments are given, attempt to set the given
		values to the buff. Example:
		player.buff(target, health=random.randint(1, 5))
		NOTE: Any Card can buff any other Card. The controller of the
		Card that buffs the target becomes the controller of the buff.
		"""
		ret = self.game.card(buff)
		ret.controller = self.controller
		ret.zone = Zone.SETASIDE
		ret.creator = self
		ret.apply(target)
		for k, v in kwargs.items():
			setattr(ret, k, v)
		return ret


class PlayableCard(BaseCard):
	Manager = PlayableCardManager
	windfury = boolean_property("windfury")

	def __init__(self, id, data):
		self.buffs = CardList()
		self.has_battlecry = False
		self.has_combo = False
		self.overload = 0
		self.target = None
		super().__init__(id, data)

	@property
	def dead(self):
		return self.zone == Zone.GRAVEYARD or self.to_be_destroyed

	@property
	def deathrattles(self):
		ret = []
		if not self.has_deathrattle:
			return ret
		if hasattr(self.data.scripts, "deathrattle"):
			ret.append(self.data.scripts.deathrattle)
		for buff in self.buffs:
			if buff.has_deathrattle and hasattr(buff.data.scripts, "deathrattle"):
				ret.append(buff.data.scripts.deathrattle)
		return ret

	@property
	def powered_up(self):
		"""
		Returns True whether the card is "powered up".
		Currently, this only applies to some cards which require a minion with a
		specific race on the field.
		"""
		for req in self.data.powerup_requirements:
			for minion in self.controller.field:
				if minion.race == req:
					return True
		return False

	@property
	def to_be_destroyed(self):
		return self.health == 0 or getattr(self, "_to_be_destroyed", False)

	@to_be_destroyed.setter
	def to_be_destroyed(self, value):
		self._to_be_destroyed = value

	@property
	def entities(self):
		return chain([self], self.buffs)

	@property
	def slots(self):
		return self.buffs

	def _set_zone(self, zone):
		super()._set_zone(zone)
		if zone == Zone.HAND:
			self.clear_buffs()

	def summon(self):
		super().summon()
		if self.controller.last_card_played is self:
			self.action()

	def action(self):
		kwargs = {}
		if self.target:
			kwargs["target"] = self.target
		elif PlayReq.REQ_TARGET_IF_AVAILABLE in self.requirements:
			logging.info("%r has no target, action exits early" % (self))
			return

		if self.has_combo and self.controller.combo:
			logging.info("Activating %r combo targeting %r" % (self, self.target))
			actions = self.data.scripts.combo
		elif hasattr(self.data.scripts, "action"):
			logging.info("Activating %r action targeting %r" % (self, self.target))
			actions = self.data.scripts.action
		elif self.choose:
			logging.info("Activating %r Choose One: %r", self, self.chosen)
			actions = self.chosen.data.scripts.action
		else:
			return

		if callable(actions):
			actions = actions(self, **kwargs)

		if actions:
			self.game.queue_actions(self, actions)
			# Hard-process deaths after a battlecry.
			# cf. test_knife_juggler()
			self.game.process_deaths()

	def clear_buffs(self):
		if self.buffs:
			logging.info("Clearing buffs from %r" % (self))
			for buff in self.buffs[:]:
				buff.destroy()

	def destroy(self):
		return self.game.queue_actions(self, [Destroy(self), Deaths()])

	def _destroy(self):
		"""
		Destroy a card.
		If the card is in PLAY, it is instead scheduled to be destroyed, and it will
		be moved to the GRAVEYARD on the next Death event.
		"""
		if self.zone == Zone.PLAY:
			logging.info("Marking %r for imminent death", self)
			self.to_be_destroyed = True
		else:
			self.zone = Zone.GRAVEYARD

	def discard(self):
		logging.info("Discarding %r" % (self))
		self.zone = Zone.GRAVEYARD

	def draw(self):
		if len(self.controller.hand) >= self.controller.max_hand_size:
			logging.info("%s overdraws and loses %r!", self.controller, self)
			self.destroy()
		else:
			logging.info("%s draws %r", self.controller, self)
			self.zone = Zone.HAND
			self.controller.cards_drawn_this_turn += 1

	def heal(self, target, amount):
		return self.game.queue_actions(self, [Heal(target, amount)])

	def hit(self, target, amount):
		if getattr(target, "immune", False):
			logging.info("%r is immune to %i damage from %r" % (target, amount, self))
			return
		return self.game.queue_actions(self, [Damage(target, amount)])

	def is_playable(self):
		if not self.controller.current_player:
			return False
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
			if not [id for id in self.entourage if not self.controller.field.contains(id)]:
				return False
		if PlayReq.REQ_WEAPON_EQUIPPED in self.requirements:
			if not self.controller.weapon:
				return False
		return True

	def play(self, target=None, choose=None):
		"""
		Queue a Play action on the card.
		"""
		assert self.is_playable()
		assert self.zone == Zone.HAND
		self.game.queue_actions(self.controller, [Play(self, target, choose)])
		return self

	def has_target(self):
		if self.has_combo and PlayReq.REQ_TARGET_FOR_COMBO in self.requirements and self.controller.combo:
			return True
		if PlayReq.REQ_TARGET_IF_AVAILABLE in self.requirements:
			return bool(self.targets)
		return PlayReq.REQ_TARGET_TO_PLAY in self.requirements

	@property
	def targets(self):
		full_board = self.game.board + [self.controller.hero, self.controller.opponent.hero]
		return [card for card in full_board if targeting.is_valid_target(self, card)]


class Character(PlayableCard):
	Manager = CharacterManager
	min_health = boolean_property("min_health")
	immune = boolean_property("immune")

	def __init__(self, *args):
		self.attacking = False
		self.frozen = False
		self.cant_attack = False
		self.cant_be_targeted_by_abilities = False
		self.cant_be_targeted_by_hero_powers = False
		self.num_attacks = 0
		self.race = Race.INVALID
		self.should_exit_combat = False
		super().__init__(*args)

	@property
	def attackable(self):
		return not self.immune

	@property
	def attack_targets(self):
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

	def can_attack(self):
		if not self.zone == Zone.PLAY:
			return False
		if self.cant_attack:
			return False
		if not self.controller.current_player:
			return False
		if not self.atk:
			return False
		if self.exhausted:
			return False
		if self.frozen:
			return False
		if not self.targets:
			return False
		return True

	@property
	def max_attacks(self):
		if self.windfury:
			return 2
		return 1

	@property
	def exhausted(self):
		if self.num_attacks >= self.max_attacks:
			return True
		return False

	def _set_zone(self, zone):
		if self.attacking:
			self.should_exit_combat = True
		super()._set_zone(zone)

	def attack(self, target):
		assert target.zone == Zone.PLAY
		assert self.controller.current_player
		self.game.attack(self, target)

	def _destroy(self):
		if self.attacking:
			self.should_exit_combat = True
		super()._destroy()

	@property
	def damaged(self):
		return bool(self.damage)

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

		if self.min_health:
			logging.info("%r has HEALTH_MINIMUM of %i", self, self.min_health)
			amount = min(amount, self.max_health - self.min_health)

		self._damage = amount

	@property
	def health(self):
		return max(0, self.max_health - self.damage)

	def _hit(self, source, amount):
		self.damage += amount
		return amount

	@property
	def targets(self):
		if self.zone == Zone.PLAY:
			return self.attack_targets
		return super().targets


class Hero(Character):
	def __init__(self, id, data):
		self.armor = 0
		self.power = None
		super().__init__(id, data)

	@property
	def slots(self):
		ret = super().slots[:]
		if self.controller.weapon and not self.controller.weapon.exhausted:
			ret.append(self.controller.weapon)
		return ret

	@property
	def entities(self):
		ret = [self]
		if self.power:
			ret.append(self.power)
		if self.controller.weapon:
			ret.append(self.controller.weapon)
		return chain(ret, self.buffs)

	def _hit(self, source, amount):
		if self.armor:
			new_amount = max(0, amount - self.armor)
			self.armor -= min(self.armor, amount)
			amount = new_amount
		return super()._hit(source, amount)

	def attack(self, target):
		ret = super().attack(target)
		if self.controller.weapon:
			logging.info("%r loses 1 durability", self.controller.weapon)
			self.controller.weapon.damage += 1

		return ret

	def summon(self):
		super().summon()
		self.controller.hero = self
		if self.data.hero_power:
			self.controller.summon(self.data.hero_power)


class Minion(Character):
	Manager = MinionManager
	charge = boolean_property("charge")
	stealthed = boolean_property("stealthed")
	taunt = boolean_property("taunt")

	silenceable_attributes = (
		"aura", "cant_attack", "cant_be_targeted_by_abilities",
		"cant_be_targeted_by_hero_powers", "charge", "divine_shield", "enrage",
		"frozen", "poisonous", "stealthed", "taunt", "windfury",
	)

	def __init__(self, id, data):
		self._enrage = None
		self.adjacent_buff = False
		self.divine_shield = False
		self.enrage = False
		self.poisonous = False
		super().__init__(id, data)

	@property
	def adjacent_minions(self):
		assert self.zone is Zone.PLAY, self.zone
		ret = CardList()
		index = self.controller.field.index(self)
		left = self.controller.field[:index]
		right = self.controller.field[index + 1:]
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
	def asleep(self):
		return not self.turns_in_play and not self.charge

	@property
	def exhausted(self):
		if self.asleep:
			return True
		return super().exhausted

	@property
	def slots(self):
		slots = super().slots[:]
		if self.enraged:
			if not self._enrage:
				self._enrage = Enrage(self.data.enrage_tags)
			slots.append(self._enrage)
		return slots

	@property
	def enraged(self):
		return self.enrage and self.damage

	def _set_zone(self, value):
		if value == Zone.PLAY:
			self.controller.field.append(self)

		if self.zone == Zone.PLAY:
			logging.info("%r is removed from the field" % (self))
			self.controller.field.remove(self)
			if self.damage:
				self.damage = 0

		super()._set_zone(value)

	def bounce(self):
		logging.info("%r is bounced back to %s's hand" % (self, self.controller))
		if len(self.controller.hand) == self.controller.max_hand_size:
			logging.info("%s's hand is full and bounce fails" % (self.controller))
			self.destroy()
		else:
			self.zone = Zone.HAND

	def hit(self, target, amount):
		super().hit(target, amount)
		if self.stealthed:
			self.stealthed = False

	def _hit(self, source, amount):
		if self.divine_shield:
			self.divine_shield = False
			logging.info("%r's divine shield prevents %i damage. Divine shield fades.", self, amount)
			return

		if getattr(source, "poisonous", False):
			logging.info("%r is destroyed because of %r is poisonous", self, source)
			self.destroy()

		return super()._hit(source, amount)

	def morph(self, into):
		return self.game.queue_actions(self, [Morph(self, into)])

	def is_playable(self):
		playable = super().is_playable()
		if len(self.controller.field) >= self.game.MAX_MINIONS_ON_FIELD:
			return False
		return playable

	def silence(self):
		logging.info("%r has been silenced" % (self))
		for aura in self._auras:
			aura.destroy()
		self.clear_buffs()

		for attr in self.silenceable_attributes:
			if getattr(self, attr):
				setattr(self, attr, False)

		# Wipe the event listeners
		self._events = []
		self.silenced = True

	def summon(self):
		if len(self.controller.field) >= self.game.MAX_MINIONS_ON_FIELD:
			return
		super().summon()


class Spell(PlayableCard):
	Manager = SpellManager

	def __init__(self, *args):
		self.immune_to_spellpower = False
		super().__init__(*args)

	def hit(self, target, amount):
		if not self.immune_to_spellpower:
			amount = self.controller.get_spell_damage(amount)
		super().hit(target, amount)


class Secret(Spell):
	def _set_zone(self, value):
		if self.zone == Zone.SECRET:
			self.controller.secrets.remove(self)
		if value == Zone.SECRET:
			self.controller.secrets.append(self)
		super()._set_zone(value)

	def is_playable(self):
		# secrets are all unique
		if self.controller.secrets.contains(self):
			return False
		return super().is_playable()

	def summon(self):
		super().summon()
		self.zone = Zone.SECRET

	def reveal(self):
		return self.game.queue_actions(self, [Reveal(self)])


class Enchantment(BaseCard):
	Manager = EnchantmentManager
	slots = []

	def __init__(self, *args):
		self.aura_source = None
		self.one_turn_effect = False
		super().__init__(*args)

	def _set_zone(self, zone):
		if zone == Zone.PLAY:
			self.owner.buffs.append(self)
		elif zone == Zone.GRAVEYARD:
			self.owner.buffs.remove(self)
		super()._set_zone(zone)

	def apply(self, target):
		logging.info("Applying %r to %r" % (self, target))
		self.owner = target
		if hasattr(self.data.scripts, "apply"):
			self.data.scripts.apply(self, target)
		if hasattr(self.data.scripts, "max_health"):
			logging.info("%r removes all damage from %r", self, target)
			target.damage = 0
		self.zone = Zone.PLAY

	def destroy(self):
		logging.info("Destroying buff %r from %r" % (self, self.owner))
		if hasattr(self.data.scripts, "destroy"):
			self.data.scripts.destroy(self)
		self.zone = Zone.GRAVEYARD
		if self.aura_source:
			# Clean up the buff from its source auras
			self.aura_source._buffs.remove(self)
	_destroy = destroy


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

	def __repr__(self):
		return "<Aura (%r)>" % (self.id)

	@property
	def game(self):
		return self.source.game

	def is_valid_target(self, target):
		if self._auraType == AuraType.PLAYER_AURA:
			return target == self.controller
		elif self._auraType == AuraType.HAND_AURA:
			if target.zone != Zone.HAND:
				return False
		return targeting.is_valid_target(self.source, target, requirements=self.requirements)

	@property
	def targets(self):
		if self._auraType == AuraType.PLAYER_AURA:
			return [self.controller]
		elif self._auraType == AuraType.HAND_AURA:
			return self.controller.hand + self.controller.opponent.hand
		if self.source.type == CardType.MINION and self.source.adjacent_buff:
			return self.source.adjacent_minions
		# XXX The targets are right but we need to get them a cleaner way.
		ret = self.game.player1.field + self.game.player2.field
		if self.controller.weapon:
			ret.append(self.controller.weapon)
		return ret

	def summon(self):
		logging.info("Summoning Aura %r", self)
		self.game.auras.append(self)
		self.game.refresh_auras()

	def _buff(self, target):
		buff = self.source.buff(target, self.id)
		buff.aura_source = self
		self._buffs.append(buff)
		self._buffed.append(target)

	def _entity_buff(self, target):
		"Returns the buff created by this aura on \a target"
		for buff in target.buffs:
			if buff.aura_source is self:
				return buff

	def update(self):
		for target in self.targets:
			if target.type == CardType.ENCHANTMENT:
				# HACKY: self.targets currently relies on hero entities
				# This includes enchantments so we need to filter them out.
				continue
			if self.is_valid_target(target):
				if not self._entity_buff(target):
					self._buff(target)
		# Make sure to copy the list as it can change during iteration
		for target in self._buffed[:]:
			# Remove auras no longer valid
			if not self.is_valid_target(target):
				buff = self._entity_buff(target)
				if buff:
					buff.destroy()
				self._buffed.remove(target)

	def destroy(self):
		logging.info("Removing %r affecting %r" % (self, self._buffed))
		self.game.auras.remove(self)
		for buff in self._buffs[:]:
			buff.destroy()
		del self._buffs
		del self._buffed
		self.source._auras.remove(self)


class Enrage(object):
	"""
	Enrage class for Minion.enrage_tags
	Enrage buffs are just a collection of tags for the enraged Minion's slots.
	"""

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
	def exhausted(self):
		return not self.controller.current_player

	@exhausted.setter
	def exhausted(self, value):
		pass

	@property
	def to_be_destroyed(self):
		return self.durability == 0 or getattr(self, "_to_be_destroyed", False)

	@to_be_destroyed.setter
	def to_be_destroyed(self, value):
		self._to_be_destroyed = value

	def _set_zone(self, zone):
		if self.zone == Zone.PLAY:
			self.controller.weapon = None
		super()._set_zone(zone)

	def summon(self):
		super().summon()
		if self.controller.weapon:
			self.controller.weapon.destroy()
		self.controller.weapon = self


class HeroPower(PlayableCard):
	Manager = HeroPowerManager

	def activate(self):
		actions = self.data.scripts.activate
		if callable(actions):
			kwargs = {}
			if self.target:
				kwargs["target"] = self.target
			actions = actions(self, **kwargs)

		if actions:
			return self.game.queue_actions(self, actions)

	def hit(self, target, amount):
		amount *= (self.controller.hero_power_double + 1)
		super().hit(target, amount)

	def is_playable(self):
		return False

	def play(self, target=None):
		raise NotImplementedError

	def use(self, target=None):
		assert self.is_usable()
		logging.info("%s uses hero power %r on %r", self.controller, self, target)

		if self.has_target():
			assert target
			self.target = target

		ret = self.activate()

		self.exhausted = True
		self.controller.times_hero_power_used_this_game += 1
		self.controller.used_mana += self.cost
		self.target = None

		return ret

	def is_usable(self):
		if self.exhausted:
			return False
		return super().is_playable()

	def summon(self):
		super().summon()
		if self.controller.hero.power:
			self.controller.hero.power.destroy()
		self.controller.hero.power = self
		self.exhausted = False
