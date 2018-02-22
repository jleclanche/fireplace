from itertools import chain
from hearthstone.enums import CardType, PlayReq, PlayState, Race, Rarity, Step, Zone
from . import actions, cards, rules, enums
from .aura import TargetableByAuras
from .entity import BaseEntity, Entity, boolean_property, int_property, slot_property
from .managers import CardManager
from .targeting import is_valid_target, TARGETING_PREREQUISITES
from .utils import CardList
from .exceptions import InvalidAction


THE_COIN = "GAME_005"


def Card(id):
	data = cards.db[id]
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
	if subclass is Spell and data.quest:
		subclass = Quest
	return subclass(data)


class BaseCard(BaseEntity):
	Manager = CardManager
	delayed_destruction = False

	def __init__(self, data):
		self.data = data
		super().__init__()
		self.requirements = data.requirements.copy()
		self.id = data.id
		self.controller = None
		self.choose = None
		self.parent_card = None
		self.aura = False
		self.heropower_damage = 0
		self._zone = Zone.INVALID
		self.tags.update(data.tags)
		self.card_set = data.card_set
		self.secret = data.secret
		self.quest = data.quest

	def __str__(self):
		return self.data.name

	def __hash__(self):
		return self.id.__hash__()

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
		return self._zone

	@zone.setter
	def zone(self, value):
		self._set_zone(value)

	def _set_zone(self, value):
		old = self.zone

		if old == value:
			self.logger.warning("%r attempted a same-zone move in %r", self, old)
			return

		if old:
			self.logger.debug("%r moves from %r to %r", self, old, value)

		caches = {
			Zone.HAND: self.controller.hand,
			Zone.DECK: self.controller.deck,
			Zone.GRAVEYARD: self.controller.graveyard,
			Zone.SETASIDE: self.game.setaside,
		}
		if caches.get(old) is not None:
			caches[old].remove(self)
		if caches.get(value) is not None:
			if hasattr(self, "_summon_index") and self._summon_index is not None:
				caches[value].insert(self._summon_index, self)
			else:
				caches[value].append(self)
		self._zone = value

		if value == Zone.PLAY:
			self.play_counter = self.game.play_counter
			self.game.play_counter += 1

	def buff(self, target, buff, **kwargs):
		"""
		Summon \a buff and apply it to \a target
		If keyword arguments are given, attempt to set the given
		values to the buff. Example:
		player.buff(target, health=random.randint(1, 5))
		NOTE: Any Card can buff any other Card. The controller of the
		Card that buffs the target becomes the controller of the buff.
		"""
		ret = self.controller.card(buff, self)
		ret.source = self
		ret.apply(target)
		for k, v in kwargs.items():
			setattr(ret, k, v)
		return ret

	def is_playable(self) -> bool:
		"""
		Return whether the card can be played.
		Do not confuse with is_summonable()
		"""
		return False

	def play(self, *args):
		raise NotImplementedError


class PlayableCard(BaseCard, Entity, TargetableByAuras):
	windfury = int_property("windfury")
	has_choose_one = boolean_property("has_choose_one")
	playable_zone = Zone.HAND

	def __init__(self, data):
		self.cant_play = False
		self.entourage = CardList(data.entourage)
		self.has_battlecry = False
		self.has_combo = False
		self.lifesteal = False
		self.overload = 0
		self.target = None
		self.rarity = Rarity.INVALID
		self.choose_cards = CardList()
		self.morphed = None
		super().__init__(data)

	@property
	def events(self):
		if self.zone == Zone.HAND:
			return self.data.scripts.Hand.events
		if self.zone == Zone.DECK:
			return self.data.scripts.Deck.events
		if self.zone == Zone.GRAVEYARD and self.tags[enums.DISCARDED] is True:
			return self.data.scripts.Discard.events

		return self.base_events + self._events

	@property
	def cost(self):
		ret = 0
		if self.zone == Zone.HAND:
			mod = self.data.scripts.cost_mod
			if mod is not None:
				r = mod.evaluate(self)
				# evaluate() can return None if it's an Evaluator (Crush)
				if r:
					ret += r
		ret = self._getattr("cost", ret)
		return max(0, ret)

	@property
	def cost_add(self):
		return self.cost+1

	@property
	def cost_dec(self):
		return self.cost-1

	@cost.setter
	def cost(self, value):
		self._cost = value

	@property
	def must_choose_one(self):
		"""
		Returns True if the card has active choices
		"""
		if self.controller.choose_both and self.has_choose_one:
			self.choose_cards = []
		return bool(self.choose_cards)

	@property
	def powered_up(self):
		"""
		Returns True whether the card is "powered up".
		"""
		if not self.data.scripts.powered_up:
			return False
		for script in self.data.scripts.powered_up:
			if not script.check(self):
				return False
		return True

	@property
	def entities(self):
		return chain([self], self.buffs)

	@property
	def zone_position(self):
		"""
		Returns the card's position (1-indexed) in its zone, or 0 if not available.
		"""
		if self.zone == Zone.HAND:
			return self.controller.hand.index(self) + 1
		return 0

	def _set_zone(self, zone):
		old_zone = self.zone
		super()._set_zone(zone)
		if old_zone == Zone.PLAY and zone not in (Zone.GRAVEYARD, Zone.SETASIDE):
			self.clear_buffs()

		if self.zone == Zone.HAND:
			# Create the "Choose One" subcards
			del self.choose_cards[:]
			for id in self.data.choose_cards:
				card = self.controller.card(id, source=self, parent=self)
				self.choose_cards.append(card)

	def destroy(self):
		return self.game.cheat_action(self, [actions.Destroy(self), actions.Deaths()])

	def discard(self):
		self.log("Discarding %r" % self)
		self.tags[enums.DISCARDED] = True
		self.zone = Zone.GRAVEYARD

	def draw(self):
		if len(self.controller.hand) >= self.controller.max_hand_size:
			self.log("%s overdraws and loses %r!", self.controller, self)
			self.discard()
		else:
			self.log("%s draws %r", self.controller, self)
			self.zone = Zone.HAND
			self.controller.cards_drawn_this_turn += 1

			if self.game.step > Step.BEGIN_MULLIGAN:
				# Proc the draw script, but only if we are past mulligan
				actions = self.get_actions("draw")
				self.game.trigger(self, actions, event_args=None)

	def heal(self, target, amount):
		return self.game.cheat_action(self, [actions.Heal(target, amount)])

	def is_playable(self):
		if self.controller.choice:
			return False
		if not self.controller.current_player:
			return False
		zone = self.parent_card.zone if self.parent_card else self.zone
		if zone != self.playable_zone:
			return False
		if not self.controller.can_pay_cost(self):
			return False
		if PlayReq.REQ_TARGET_TO_PLAY in self.requirements:
			if not self.play_targets:
				return False
		if PlayReq.REQ_NUM_MINION_SLOTS in self.requirements:
			if self.requirements[PlayReq.REQ_NUM_MINION_SLOTS] > self.controller.minion_slots:
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
		if PlayReq.REQ_FRIENDLY_MINION_DIED_THIS_GAME in self.requirements:
			if not self.controller.graveyard.filter(type=CardType.MINION):
				return False

		return self.is_summonable()

	def play(self, target=None, index=None, choose=None):
		"""
		Queue a Play action on the card.
		"""
		if choose:
			if self.must_choose_one:
				choose = card = self.choose_cards.filter(id=choose)[0]
				self.log("%r: choosing %r", self, choose)
			else:
				raise InvalidAction("%r cannot be played with choice %r" % (self, choose))
		else:
			if self.must_choose_one:
				raise InvalidAction("%r requires a choice (one of %r)" % (self, self.choose_cards))
			card = self
		if not self.is_playable():
			raise InvalidAction("%r isn't playable." % (self))
		if card.requires_target():
			if not target:
				raise InvalidAction("%r requires a target to play." % (self))
			elif target not in self.play_targets:
				raise InvalidAction("%r is not a valid target for %r." % (target, self))
		elif target:
			self.logger.warning("%r does not require a target, ignoring target %r", self, target)
		if self.controller.all_targets_random:
			target = self.game.cheat_action(self, [actions.Retarget(self, random.choice(self.controller.opponent.characters))])[0][0]
		self.game.play_card(self, target, index, choose)
		return self

	def is_summonable(self) -> bool:
		"""
		Return whether the card can be summoned.
		Do not confuse with is_playable()
		"""
		return True

	def morph(self, into):
		"""
		Morph the card into another card
		"""
		return self.game.cheat_action(self, [actions.Morph(self, into)])

	def shuffle_into_deck(self):
		"""
		Shuffle the card into the controller's deck
		"""
		return self.game.cheat_action(self, [actions.Shuffle(self.controller, self)])

	def battlecry_requires_target(self):
		"""
		True if the play action of the card requires a target
		"""
		if self.has_combo and self.controller.combo:
			if PlayReq.REQ_TARGET_FOR_COMBO in self.requirements:
				return True

		for req in TARGETING_PREREQUISITES:
			if req in self.requirements:
				return True
		return False

	def requires_target(self):
		"""
		True if the card currently requires a target
		"""
		if self.has_combo and PlayReq.REQ_TARGET_FOR_COMBO in self.requirements:
			if self.controller.combo:
				return True
		if PlayReq.REQ_TARGET_IF_AVAILABLE in self.requirements:
			return bool(self.play_targets)
		if PlayReq.REQ_TARGET_IF_AVAILABLE_AND_DRAGON_IN_HAND in self.requirements:
			if self.controller.hand.filter(race=Race.DRAGON):
				return bool(self.play_targets)
		req = self.requirements.get(PlayReq.REQ_TARGET_IF_AVAILABLE_AND_MINIMUM_FRIENDLY_MINIONS)
		if req is not None:
			if len(self.controller.field) >= req:
				return bool(self.play_targets)
		req = self.requirements.get(PlayReq.REQ_TARGET_IF_AVAILABLE_AND_MINIMUM_FRIENDLY_SECRETS)
		if req is not None:
			if len(self.controller.secrets) >= req:
				return bool(self.play_targets)
		return PlayReq.REQ_TARGET_TO_PLAY in self.requirements

	@property
	def play_targets(self):
		return [card for card in self.game.characters if is_valid_target(self, card)]

	@property
	def targets(self):
		return self.play_targets

	def reset(self):
		if self.data:
			self._events = self.data.scripts.events[:]
		else:
			self._events = []
		self.tags.update(self.data.tags)


class LiveEntity(PlayableCard, Entity):
	has_deathrattle = boolean_property("has_deathrattle")
	atk = int_property("atk")
	cant_be_damaged = boolean_property("cant_be_damaged")
	immune_while_attacking = slot_property("immune_while_attacking")
	incoming_damage_multiplier = int_property("incoming_damage_multiplier")
	max_health = int_property("max_health")

	def __init__(self, data):
		super().__init__(data)
		self._to_be_destroyed = False
		self.damage = 0
		self.forgetful = False
		self.predamage = 0
		self.turns_in_play = 0
		self.turn_killed = -1

	def _set_zone(self, zone):
		if zone == Zone.GRAVEYARD and self.zone == Zone.PLAY:
			self.turn_killed = self.game.turn
		super()._set_zone(zone)
		# See issue #283 (Malorne, Anub'arak)
		self._to_be_destroyed = False

	@property
	def immune(self):
		if self.immune_while_attacking and self.attacking:
			return True
		return self.cant_be_damaged

	@property
	def damaged(self):
		return bool(self.damage)

	@property
	def deathrattles(self):
		ret = []
		if not self.has_deathrattle:
			return ret
		deathrattle = self.get_actions("deathrattle")
		if deathrattle:
			ret.append(deathrattle)
		for buff in self.buffs:
			for deathrattle in buff.deathrattles:
				ret.append(deathrattle)
		return ret

	@property
	def dead(self):
		return self.zone == Zone.GRAVEYARD or self.to_be_destroyed

	@property
	def delayed_destruction(self):
		return self.zone == Zone.PLAY

	@property
	def to_be_destroyed(self):
		return getattr(self, self.health_attribute) == 0 or self._to_be_destroyed

	@to_be_destroyed.setter
	def to_be_destroyed(self, value):
		self._to_be_destroyed = value

	@property
	def killed_this_turn(self):
		return self.turn_killed == self.game.turn

	def _hit(self, amount):
		self.damage += amount
		return amount

	def hit(self, amount):
		return self.game.cheat_action(self, [actions.Hit(self, amount)])


class Character(LiveEntity):
	health_attribute = "health"
	cant_attack = boolean_property("cant_attack")
	cant_be_targeted_by_opponents = boolean_property("cant_be_targeted_by_opponents")
	cant_be_targeted_by_abilities = boolean_property("cant_be_targeted_by_abilities")
	cant_be_targeted_by_hero_powers = boolean_property("cant_be_targeted_by_hero_powers")
	heavily_armored = boolean_property("heavily_armored")
	min_health = boolean_property("min_health")
	taunt = boolean_property("taunt")

	def __init__(self, data):
		self.frozen = False
		self.attack_target = None
		self.cannot_attack_heroes = False
		self.num_attacks = 0
		self.race = Race.INVALID
		super().__init__(data)

	@property
	def events(self):
		ret = super().events
		if self.heavily_armored:
			ret += rules.HEAVILY_ARMORED
		return ret

	@property
	def attackable(self):
		return not self.immune

	@property
	def attacking(self):
		return self.attack_target is not None

	@property
	def attack_targets(self):
		if self.cannot_attack_heroes:
			targets = self.controller.opponent.field
		else:
			targets = self.controller.opponent.characters

		taunts = targets.filter(taunt=True).filter(attackable=True)
		return (taunts or targets).filter(attackable=True)

	def can_attack(self, target=None):
		if self.controller.choice:
			return False
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
		if not self.attack_targets:
			return False
		if target is not None and target not in self.attack_targets:
			return False

		return True

	@property
	def max_attacks(self):
		return self.windfury + 1

	@property
	def exhausted(self):
		if self.num_attacks >= self.max_attacks:
			return True
		return False

	@property
	def should_exit_combat(self):
		if self.attacking:
			if self.dead or self.zone != Zone.PLAY:
				return True
		return False

	def attack(self, target):
		if not self.can_attack(target):
			raise InvalidAction("%r can't attack %r." % (self, target))
		if self.controller.all_targets_random:
			target = self.game.cheat_action(self, [actions.Retarget(self, random.choice(self.controller.opponent.characters))])[0][0]
		self.game.attack(self, target)

	@property
	def health(self):
		return max(0, self.max_health - self.damage)

	@property
	def targets(self):
		if self.zone == Zone.PLAY:
			return self.attack_targets
		return super().targets

	def set_current_health(self, amount):
		return self.game.cheat_action(self, [actions.SetCurrentHealth(self, amount)])


class Hero(Character):
	def __init__(self, data):
		self.armor = 0
		self.power = None
		super().__init__(data)

	@property
	def entities(self):
		yield self
		if self.power:
			yield self.power
			if self.power.buffs:
				yield from self.power.buffs
		if self.controller.weapon:
			yield self.controller.weapon
		yield from self.buffs

	@property
	def windfury(self):
		ret = super().windfury
		if self.controller.weapon:
			# NOTE: As of 9786, Windfury is retained even when the weapon is exhausted.
			return self.controller.weapon.windfury or ret
		return ret

	def _getattr(self, attr, i):
		ret = super()._getattr(attr, i)
		if attr == "atk":
			if self.controller.weapon and not self.controller.weapon.exhausted:
				ret += self.controller.weapon.atk
		return ret

	def _set_zone(self, value):
		if value == Zone.PLAY:
			self.controller.hero = self
			if self.data.hero_power:
				self.controller.summon(self.data.hero_power)
		elif value == Zone.GRAVEYARD:
			if self.power:
				self.power.zone = Zone.GRAVEYARD
			if self.controller.hero is self:
				self.controller.playstate = PlayState.LOSING
		super()._set_zone(value)

	def _hit(self, amount):
		amount = super()._hit(amount)
		if self.armor:
			reduced_damage = min(amount, self.armor)
			self.log("%r loses %r armor instead of damage", self, reduced_damage)
			self.damage -= reduced_damage
			self.armor -= reduced_damage
		return amount


class Minion(Character):
	charge = boolean_property("charge")
	has_inspire = boolean_property("has_inspire")
	spellpower = int_property("spellpower")
	stealthed = boolean_property("stealthed")

	silenceable_attributes = (
		"always_wins_brawls", "aura", "cant_attack", "cant_be_targeted_by_abilities",
		"cant_be_targeted_by_hero_powers", "charge", "divine_shield", "enrage",
		"forgetful", "frozen", "has_deathrattle", "has_inspire", "poisonous", "lifesteal",
		"stealthed", "taunt", "windfury", "cannot_attack_heroes",
	)

	def __init__(self, data):
		self.always_wins_brawls = False
		self.divine_shield = False
		self.enrage = False
		self.poisonous = False
		self.silenced = False
		self._summon_index = None
		super().__init__(data)

	@property
	def ignore_scripts(self):
		return self.silenced

	@property
	def adjacent_minions(self):
		assert self.zone is Zone.PLAY, self.zone
		ret = CardList()
		index = self.zone_position - 1
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
		return self.zone == Zone.PLAY and not self.turns_in_play and not self.charge

	@property
	def exhausted(self):
		if self.asleep:
			return True
		return super().exhausted

	@property
	def enraged(self):
		return self.enrage and self.damage

	@property
	def update_scripts(self):
		yield from super().update_scripts
		if self.enraged:
			yield from self.data.scripts.enrage

	@property
	def zone_position(self):
		if self.zone == Zone.PLAY:
			return self.controller.field.index(self) + 1
		return super().zone_position

	def _set_zone(self, value):
		if value == Zone.PLAY:
			if self._summon_index is not None:
				self.controller.field.insert(self._summon_index, self)
			else:
				self.controller.field.append(self)
		elif value == Zone.GRAVEYARD and self.zone == Zone.PLAY:
			self.controller.minions_killed_this_turn += 1

		if self.zone == Zone.PLAY:
			self.log("%r is removed from the field", self)
			self.controller.field.remove(self)
			if self.damage:
				self.damage = 0

		super()._set_zone(value)

	def _hit(self, amount):
		if self.divine_shield:
			self.divine_shield = False
			self.log("%r's divine shield prevents %i damage.", self, amount)
			return 0

		amount = super()._hit(amount)

		if self.health < self.min_health:
			self.log("%r has HEALTH_MINIMUM of %i", self, self.min_health)
			self.damage = self.max_health - self.min_health

		return amount

	def bounce(self):
		return self.game.cheat_action(self, [actions.Bounce(self)])

	def is_summonable(self):
		summonable = super().is_summonable()
		if len(self.controller.field) >= self.game.MAX_MINIONS_ON_FIELD:
			return False
		return summonable

	def silence(self):
		return self.game.cheat_action(self, [actions.Silence(self)])

	def reset(self):
		for attr in self.silenceable_attributes:
			setattr(self, attr, None)
		self.silenced = False
		self.clear_buffs()
		super().reset()



class Spell(PlayableCard):
	def __init__(self, data):
		self.immune_to_spellpower = False
		self.receives_double_spelldamage_bonus = False
		super().__init__(data)

	def get_damage(self, amount, target):
		amount = super().get_damage(amount, target)
		if not self.immune_to_spellpower:
			amount = self.controller.get_spell_damage(amount)
		if self.receives_double_spelldamage_bonus:
			amount *= 2
		return amount



class Secret(Spell):
	@property
	def events(self):
		ret = super().events
		if self.zone == Zone.SECRET and not self.exhausted:
			ret += self.data.scripts.secret
		return ret

	@property
	def exhausted(self):
		return self.zone == Zone.SECRET and self.controller.current_player

	@property
	def zone_position(self):
		if self.zone == Zone.SECRET:
			return self.controller.secrets.index(self) + 1
		return super().zone_position

	def _set_zone(self, value):
		if value == Zone.PLAY:
			# Move secrets to the SECRET Zone when played
			value = Zone.SECRET
		if self.zone == Zone.SECRET:
			self.controller.secrets.remove(self)
		if value == Zone.SECRET:
			self.controller.secrets.append(self)
		super()._set_zone(value)

	def is_summonable(self):
		# secrets are all unique
		if self.controller.secrets.contains(self):
			return False
		return super().is_summonable()


class Quest(Spell):
	def __init__(self, data):
		self.quest_progress_total = data.quest_progress_total
		self.quest_progress = 0
		self.quest_map = {}
		super().__init__(data)


	@property
	def events(self):
		ret = super().events
		if self.zone == Zone.SECRET:
			ret += self.data.scripts.secret
		return ret

	@property
	def zone_position(self):
		if self.zone == Zone.SECRET:
			return self.controller.secrets.index(self) + 1
		return super().zone_position

	def _set_zone(self, value):
		if value == Zone.PLAY:
			# Move secrets to the SECRET Zone when played
			value = Zone.SECRET
		if self.zone == Zone.SECRET:
			self.controller.secrets.remove(self)
		if value == Zone.SECRET:
			self.controller.secrets.insert(0, self)
		super()._set_zone(value)

	def is_summonable(self):
		# secrets are all unique
		for i in self.controller.secrets:
			if i.quest:
				return False
		return super().is_summonable()



class Enchantment(BaseCard):
	atk = int_property("atk")
	cost = int_property("cost")
	has_deathrattle = boolean_property("has_deathrattle")
	incoming_damage_multiplier = int_property("incoming_damage_multiplier")
	max_health = int_property("max_health")
	spellpower = int_property("spellpower")
	additional_activations = int_property("additional_activations")

	buffs = []
	slots = []

	def __init__(self, data):
		self.one_turn_effect = False
		self.additional_deathrattles = []
		super().__init__(data)

	@property
	def deathrattles(self):
		if not self.has_deathrattle:
			return []
		ret = self.additional_deathrattles[:]
		deathrattle = self.get_actions("deathrattle")
		if deathrattle:
			ret.append(deathrattle)
		if not ret:
			raise NotImplementedError("Missing deathrattle script for %r" % (self))
		return ret

	def _getattr(self, attr, i):
		i += getattr(self, "_" + attr, 0)
		return getattr(self.data.scripts, attr, lambda s, x: x)(self, i)

	def _set_zone(self, zone):
		if zone == Zone.PLAY:
			self.owner.buffs.append(self)
		elif zone == Zone.REMOVEDFROMGAME:
			if self.zone == zone:
				# Can happen if a Destroy is queued after a bounce, for example
				self.logger.warning("Trying to remove %r which is already gone", self)
				return
			self.owner.buffs.remove(self)
			if self in self.game.active_aura_buffs:
				self.game.active_aura_buffs.remove(self)
		super()._set_zone(zone)

	def apply(self, target):
		self.log("Applying %r to %r", self, target)
		self.owner = target
		if hasattr(self.data.scripts, "apply"):
			self.data.scripts.apply(self, target)
		if hasattr(self.data.scripts, "max_health"):
			self.log("%r removes all damage from %r", self, target)
			target.damage = 0
		if hasattr(self.data.scripts, "hand"):
			target.data.scripts.Hand.events.append(self.data.scripts.hand)
		self.zone = Zone.PLAY

	def remove(self):
		self.zone = Zone.REMOVEDFROMGAME


class Weapon(rules.WeaponRules, LiveEntity):
	health_attribute = "durability"

	def __init__(self, *args):
		super().__init__(*args)
		self.damage = 0

	@property
	def durability(self):
		return max(0, self.max_durability - self.damage)

	@property
	def max_durability(self):
		ret = self._max_durability
		ret += self._getattr("max_health", 0)
		return max(0, ret)

	@max_durability.setter
	def max_durability(self, value):
		self._max_durability = value

	@property
	def exhausted(self):
		return self.zone == Zone.PLAY and not self.controller.current_player

	def _set_zone(self, zone):
		if zone == Zone.PLAY:
			if self.controller.weapon:
				self.log("Destroying old weapon %r", self.controller.weapon)
				self.game.trigger(self, [actions.Destroy(self.controller.weapon)], event_args=None)
			self.controller.weapon = self
		elif self.zone == Zone.PLAY:
			self.controller.weapon = None
		super()._set_zone(zone)


class HeroPower(PlayableCard):
	additional_activations = int_property("additional_activations")
	playable_zone = Zone.PLAY

	def __init__(self, data):
		super().__init__(data)
		self.activations_this_turn = 0

	@property
	def exhausted(self):
		if self.additional_activations == -1:
			return False
		return self.activations_this_turn >= 1 + self.additional_activations

	def _set_zone(self, value):
		if value == Zone.PLAY:
			if self.controller.hero.power:
				self.controller.hero.power.destroy()
			self.controller.hero.power = self
		super()._set_zone(value)

	def activate(self):
		return self.game.queue_actions(self.controller, [actions.Activate(self, self.target)])

	def get_damage(self, amount, target):
		amount = super().get_damage(amount, target)
		amount += self.controller.heropower_damage
		amount <<= self.controller.hero_power_double
		return amount

	def use(self, target=None):
		if not self.is_usable():
			raise InvalidAction("%r can't be used." % (self))

		self.log("%s uses hero power %r on %r", self.controller, self, target)

		if self.requires_target():
			if not target:
				raise InvalidAction("%r requires a target." % (self))
			self.target = target
		elif target:
			self.logger.warning("%r does not require a target, ignoring target %r", self, target)

		ret = self.activate()

		self.controller.times_hero_power_used_this_game += 1
		self.target = None

		return ret

	def is_usable(self):
		if self.exhausted:
			return False
		return super().is_playable()
