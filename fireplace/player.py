import random
from itertools import chain

from hearthstone.enums import CardType, PlayState, Race, Zone

from .actions import Concede, Draw, Fatigue, Give, Hit, Steal, Summon
from .aura import TargetableByAuras
from .card import Card
from .deck import Deck
from .entity import Entity, slot_property
from .managers import PlayerManager
from .utils import CardList


class Player(Entity, TargetableByAuras):
	Manager = PlayerManager
	all_targets_random = slot_property("all_targets_random")
	cant_overload = slot_property("cant_overload")
	choose_both = slot_property("choose_both")
	extra_battlecries = slot_property("extra_battlecries")
	extra_deathrattles = slot_property("extra_deathrattles")
	extra_end_turn_effect = slot_property("extra_end_turn_effect")
	healing_double = slot_property("healing_double", sum)
	hero_power_double = slot_property("hero_power_double", sum)
	healing_as_damage = slot_property("healing_as_damage")
	shadowform = slot_property("shadowform")
	spellpower_double = slot_property("spellpower_double", sum)
	spellpower_adjustment = slot_property("spellpower", sum)
	spells_cost_health = slot_property("spells_cost_health")
	murlocs_cost_health = slot_property("murlocs_cost_health")
	type = CardType.PLAYER

	def __init__(self, name, deck, hero, is_standard=True):
		self.starting_deck = deck
		self.starting_hero = hero
		self.data = None
		self.name = name
		self.hero = None
		self.is_standard = is_standard
		super().__init__()
		self.deck = Deck()
		self.hand = CardList()
		self.discarded = CardList()
		self.field = CardList()
		self.graveyard = CardList()
		self.secrets = CardList()
		self.choice = None
		self.max_hand_size = 10
		self.max_resources = 10
		self.max_deck_size = 60
		self.cant_draw = False
		self.cant_fatigue = False
		self.fatigue_counter = 0
		self.last_card_played = None
		self.cards_drawn_this_turn = 0
		self.overloaded = 0
		self.overload_locked = 0
		self._max_mana = 0
		self._start_hand_size = 3
		self.playstate = PlayState.INVALID
		self.temp_mana = 0
		self.timeout = 75
		self.times_hero_power_used_this_game = 0
		self.used_mana = 0
		self.minions_killed_this_turn = 0
		self.weapon = None
		self.zone = Zone.INVALID
		self.jade_golem = 1
		self.times_totem_summoned_this_game = 0
		self.elemental_played_this_turn = 0
		self.elemental_played_last_turn = 0
		self.cards_played_this_game = CardList()
		self.cthun = None
		self.extra_turns = 0

	def __str__(self):
		return self.name

	def __repr__(self):
		return "%s(name=%r, hero=%r)" % (self.__class__.__name__, self.name, self.hero)

	@property
	def current_player(self):
		return self.game.current_player is self

	@property
	def controller(self):
		return self

	@property
	def mana(self):
		mana = max(0, self.max_mana - self.used_mana - self.overload_locked) + self.temp_mana
		return mana

	@property
	def max_mana(self):
		return self._max_mana

	@max_mana.setter
	def max_mana(self, amount):
		self._max_mana = min(self.max_resources, max(0, amount))
		self.log("%s is now at %i mana crystals", self, self._max_mana)

	@property
	def heropower_damage(self):
		return sum(minion.heropower_damage for minion in self.field)

	@property
	def spellpower(self):
		aura_power = self.controller.spellpower_adjustment
		minion_power = sum(minion.spellpower for minion in self.field)
		return aura_power + minion_power

	@property
	def start_hand_size(self):
		if not self.first_player:
			# Give the second player an extra card
			return self._start_hand_size + 1
		return self._start_hand_size

	@property
	def characters(self):
		return CardList(chain([self.hero] if self.hero else [], self.field))

	@property
	def entities(self):
		for entity in self.field:
			yield from entity.entities
		yield from self.secrets
		yield from self.buffs
		if self.hero:
			yield from self.hero.entities
		yield self

	@property
	def live_entities(self):
		yield from self.field
		if self.hero:
			yield self.hero
		if self.weapon:
			yield self.weapon

	@property
	def actionable_entities(self):
		yield from self.characters
		yield from self.hand
		if self.hero.power:
			yield self.hero.power

	@property
	def minion_slots(self):
		return max(0, self.game.MAX_MINIONS_ON_FIELD - len(self.field))

	def copy_cthun_buff(self, card):
		for buff in self.cthun.buffs:
			buff.source.buff(
				card, buff.id,
				atk=buff.atk,
				max_health=buff.max_health,
				taunt=getattr(buff, "taunt", False))

	def card(self, id, source=None, parent=None, zone=Zone.SETASIDE):
		card = Card(id)
		card.controller = self
		card.zone = zone
		card.play_counter = self.game.play_counter
		self.game.play_counter += 1
		if source is not None:
			card.creator = source
		if parent is not None:
			card.parent_card = parent
		# C'THUN
		if self.cthun and id == self.cthun.id:
			self.copy_cthun_buff(card)
		self.game.manager.new_entity(card)
		return card

	def prepare_for_game(self):
		self.summon(self.starting_hero)
		self.starting_hero = self.hero
		for id in self.starting_deck:
			card = self.card(id, zone=Zone.DECK)
			if self.is_standard and not card.is_standard:
				self.is_standard = False
		self.starting_deck = self.deck[:]
		self.shuffle_deck()
		self.cthun = self.card("OG_280")
		self.playstate = PlayState.PLAYING

		# Draw initial hand (but not any more than what we have in the deck)
		hand_size = min(len(self.deck), self.start_hand_size)
		# Quest cards are automatically included in the player's mulligan as the left-most card
		quests = [card for card in self.deck if card.data.quest]
		starting_hand = quests + random.sample(self.deck, hand_size - len(quests))
		# It's faster to move cards directly to the hand instead of drawing
		for card in starting_hand:
			card.zone = Zone.HAND

	def get_spell_damage(self, amount: int) -> int:
		"""
		Returns the amount of damage \a amount will do, taking
		SPELLPOWER and SPELLPOWER_DOUBLE into account.
		"""
		amount += self.spellpower
		amount <<= self.controller.spellpower_double
		return amount

	def get_heropower_damage(self, amount: int) -> int:
		amount += self.heropower_damage
		amount <<= self.controller.hero_power_double
		return amount

	def discard_hand(self):
		self.log("%r discards their entire hand!", self)
		# iterate the list in reverse so we don't skip over cards in the process
		# yes it's stupid.
		for card in self.hand[::-1]:
			card.discard()

	def can_pay_cost(self, card):
		"""
		Returns whether the player can pay the resource cost of a card.
		"""
		if self.spells_cost_health and card.type == CardType.SPELL:
			return self.hero.health > card.cost
		if self.murlocs_cost_health:
			if card.type == CardType.MINION and card.race == Race.MURLOC:
				return self.hero.health > card.cost
		return self.mana >= card.cost

	def pay_cost(self, source, amount: int) -> int:
		"""
		Make player pay \a amount mana.
		Returns how much mana is spent, after temporary mana adjustments.
		"""
		if self.spells_cost_health and source.type == CardType.SPELL:
			self.log("%s spells cost %i health", self, amount)
			self.game.queue_actions(self, [Hit(self.hero, amount)])
			return amount
		if self.murlocs_cost_health:
			if source.type == CardType.MINION and source.race == Race.MURLOC:
				self.log("%s murlocs cost %i health", self, amount)
				self.game.queue_actions(self, [Hit(self.hero, amount)])
				return amount
		if self.temp_mana:
			# Coin, Innervate etc
			used_temp = min(self.temp_mana, amount)
			amount -= used_temp
			self.temp_mana -= used_temp
		self.log("%s pays %i mana", self, amount)
		self.used_mana += amount
		return amount

	def shuffle_deck(self):
		self.log("%r shuffles their deck", self)
		random.shuffle(self.deck)

	def draw(self, count=1):
		if self.cant_draw:
			self.log("%s tries to draw %i cards, but can't draw", self, count)
			return None

		ret = self.game.cheat_action(self, [Draw(self) * count])[0]
		if count == 1:
			if not ret[0]:  # fatigue
				return None
			return ret[0][0]
		return ret

	def give(self, id):
		cards = self.game.cheat_action(self, [Give(self, id)])[0]
		return cards[0][0]

	def concede(self):
		ret = self.game.cheat_action(self, [Concede(self)])
		return ret

	def fatigue(self):
		return self.game.cheat_action(self, [Fatigue(self)])[0]

	def steal(self, card):
		return self.game.cheat_action(self, [Steal(card)])

	def summon(self, card):
		"""
		Puts \a card in the PLAY zone
		"""
		if isinstance(card, str):
			card = self.card(card, zone=Zone.PLAY)
		self.game.cheat_action(self, [Summon(self, card)])
		return card
