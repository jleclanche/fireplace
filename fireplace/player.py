import logging
import random
from itertools import chain
from .actions import Draw, Give, Summon
from .deck import Deck
from .entity import Entity
from .enums import CardType, PlayState, Zone
from .entity import slot_property
from .managers import PlayerManager
from .targeting import *
from .utils import CardList


class Player(Entity):
	Manager = PlayerManager
	extra_deathrattles = slot_property("extra_deathrattles")
	hero_power_double = slot_property("hero_power_double", sum)
	healing_double = slot_property("healing_double", sum)
	outgoing_healing_adjustment = slot_property("outgoing_healing_adjustment")
	spellpower_double = slot_property("spellpower_double", sum)
	type = CardType.PLAYER

	def __init__(self, name):
		self.data = None
		super().__init__()
		self.name = name
		self.deck = Deck()
		self.hand = CardList()
		self.field = CardList()
		self.secrets = CardList()
		self.buffs = []
		self.max_hand_size = 10
		self.max_resources = 10
		self.current_player = False
		self.fatigue_counter = 0
		self.hero = None
		self.last_card_played = None
		self.overloaded = 0
		self.max_mana = 0
		self.playstate = PlayState.INVALID
		self.temp_mana = 0
		self.timeout = 75
		self.times_hero_power_used_this_game = 0
		self.minions_killed_this_turn = 0
		self.weapon = None
		self.zone = Zone.INVALID

	def __str__(self):
		return self.name

	def __repr__(self):
		return "%s(name=%r, hero=%r)" % (self.__class__.__name__, self.name, self.hero)

	@property
	def controller(self):
		return self

	@property
	def slots(self):
		return self.buffs

	@property
	def mana(self):
		mana = max(0, self.max_mana - self.used_mana) + self.temp_mana
		return mana

	@property
	def spellpower(self):
		return sum(minion.spellpower for minion in self.field)

	@property
	def characters(self):
		return CardList(chain([self.hero] if self.hero else [], self.field))

	@property
	def entities(self):
		ret = []
		for entity in self.field:
			ret += entity.entities
		# Secrets are only active on the opponent's turn
		if not self.current_player:
			for entity in self.secrets:
				ret += entity.entities
		return CardList(chain(list(self.hero.entities) if self.hero else [], ret, [self]))

	@property
	def live_entities(self):
		ret = self.field[:]
		if self.hero:
			ret.append(self.hero)
		if self.weapon:
			ret.append(self.weapon)
		return ret

	def get_spell_damage(self, amount: int) -> int:
		"""
		Returns the amount of damage \a amount will do, taking
		SPELLPOWER and SPELLPOWER_DOUBLE into account.
		"""
		amount += self.spellpower
		amount *= (self.controller.spellpower_double + 1)
		return amount

	def give(self, id):
		cards = self.game.queue_actions(self, [Give(self, id)])[0]
		return cards[0][0]

	def prepare_deck(self, cards, hero):
		self.original_deck = Deck.from_list(cards)
		self.original_deck.hero = hero

	def discard_hand(self):
		logging.info("%r discards his entire hand!" % (self))
		# iterate the list in reverse so we don't skip over cards in the process
		# yes it's stupid.
		for card in self.hand[::-1]:
			card.discard()

	def draw(self, count=1):
		ret = self.game.queue_actions(self, [Draw(self) * count])[0]
		if count == 1:
			if not ret[0]:  # fatigue
				return None
			return ret[0][0]
		return ret

	def mill(self, count=1):
		if count == 1:
			if not self.deck:
				return
			else:
				card = self.deck[-1]
			logging.info("%s mills %r" % (self, card))
			card.destroy()
			return card
		else:
			ret = []
			while count:
				ret.append(self.mill())
				count -= 1
			return ret

	def fatigue(self):
		self.fatigue_counter += 1
		logging.info("%s takes %i fatigue damage" % (self, self.fatigue_counter))
		self.hero.hit(self.hero, self.fatigue_counter)

	@property
	def max_mana(self):
		return self._max_mana

	@max_mana.setter
	def max_mana(self, amount):
		self._max_mana = min(self.max_resources, max(0, amount))
		logging.info("%s is now at %i mana crystals", self, self._max_mana)

	def take_control(self, card):
		logging.info("%s takes control of %r", self, card)
		zone = card.zone
		card.zone = Zone.SETASIDE
		card.controller = self
		card.zone = zone

	def shuffle_deck(self):
		logging.info("%r shuffles their deck", self)
		random.shuffle(self.deck)

	def summon(self, card):
		"""
		Puts \a card in the PLAY zone
		"""
		if isinstance(card, str):
			card = self.game.card(card)
			card.controller = self
		self.game.queue_actions(self, [Summon(self, card)])
		return card
