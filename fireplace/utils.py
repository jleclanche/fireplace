from __future__ import annotations

import os.path
import random
from bisect import bisect
from importlib import import_module
from pkgutil import iter_modules
from typing import List, TypeVar, overload
from xml.etree import ElementTree

from hearthstone.enums import CardClass, CardType

from .logging import log


# Autogenerate the list of cardset modules
_cards_module = os.path.join(os.path.dirname(__file__), "cards")
CARD_SETS = [cs for _, cs, ispkg in iter_modules([_cards_module]) if ispkg]
T = TypeVar("T")


class CardList(list[T]):
	def __contains__(self, x: T) -> bool:
		for item in self:
			if x is item:
				return True
		return False

	@overload
	def __getitem__(self, index: int) -> T:
		pass

	@overload
	def __getitem__(self, index: slice) -> CardList[T]:
		pass

	def __getitem__(self, key):
		ret = super().__getitem__(key)
		if isinstance(key, slice):
			return self.__class__(ret)
		return ret

	def __int__(self) -> int:
		# Used in Kettle to easily serialize CardList to json
		return len(self)

	def contains(self, x: T | str) -> bool:
		"""
		True if list contains any instance of x
		"""
		for item in self:
			if x == item:
				return True
		return False

	def index(self, x: T) -> int:
		for i, item in enumerate(self):
			if x is item:
				return i
		raise ValueError

	def remove(self, x: T):
		for i, item in enumerate(self):
			if x is item:
				del self[i]
				return
		raise ValueError

	def exclude(self, *args, **kwargs):
		if args:
			return self.__class__(e for e in self for arg in args if e is not arg)
		else:
			return self.__class__(e for k, v in kwargs.items() for e in self if getattr(e, k) != v)

	def filter(self, **kwargs):
		def conditional(e, k, v):
			p = getattr(e, k, 0)
			if hasattr(p, "__iter__"):
				return v in p
			return p == v
		return self.__class__(e for k, v in kwargs.items() for e in self if conditional(e, k, v))


def random_draft(card_class: CardClass, exclude=[], include=[]):
	"""
	Return a deck of 30 random cards for the \a card_class
	"""
	from . import cards
	from .deck import Deck

	deck = list(include)
	collection = []
	# hero = card_class.default_hero

	for card in cards.db.keys():
		if card in exclude:
			continue
		cls = cards.db[card]
		if not cls.collectible:
			continue
		if cls.type == CardType.HERO:
			# Heroes are collectible...
			continue
		if cls.card_class and cls.card_class not in [card_class, CardClass.NEUTRAL]:
			# Play with more possibilities
			continue
		collection.append(cls)

	while len(deck) < Deck.MAX_CARDS:
		card = random.choice(collection)
		if deck.count(card.id) < card.max_count_in_deck:
			deck.append(card.id)

	return deck


def random_class():
	return CardClass(random.randint(2, 10))


def entity_to_xml(entity):
	e = ElementTree.Element("Entity")
	for tag, value in entity.tags.items():
		if value and not isinstance(value, str):
			te = ElementTree.Element("Tag")
			te.attrib["enumID"] = str(int(tag))
			te.attrib["value"] = str(int(value))
			e.append(te)
	return e


def game_state_to_xml(game):
	tree = ElementTree.Element("HSGameState")
	tree.append(entity_to_xml(game))
	for player in game.players:
		tree.append(entity_to_xml(player))
	for entity in game:
		if entity.type in (CardType.GAME, CardType.PLAYER):
			# Serialized those above
			continue
		e = entity_to_xml(entity)
		e.attrib["CardID"] = entity.id
		tree.append(e)

	return ElementTree.tostring(tree)


def weighted_card_choice(source, weights: List[int], card_sets: List[str], count: int):
	"""
	Take a list of weights and a list of card pools and produce
	a random weighted sample without replacement.
	len(weights) == len(card_sets) (one weight per card set)
	"""

	chosen_cards = []

	# sum all the weights
	cum_weights = []
	totalweight = 0
	for i, w in enumerate(weights):
		totalweight += w * len(card_sets[i])
		cum_weights.append(totalweight)

	if totalweight == 0:
		return []

	# for each card
	for i in range(count):
		# choose a set according to weighting
		chosen_set = bisect(cum_weights, random.random() * totalweight)

		# choose a random card from that set
		chosen_card_index = random.randint(0, len(card_sets[chosen_set]) - 1)

		chosen_cards.append(card_sets[chosen_set].pop(chosen_card_index))
		totalweight -= weights[chosen_set]
		cum_weights[chosen_set:] = [x - weights[chosen_set] for x in cum_weights[chosen_set:]]

	return [source.controller.card(card, source=source) for card in chosen_cards]


def setup_game():
	from .game import Game
	from .player import Player

	card_class1 = random_class()
	card_class2 = random_class()
	deck1 = random_draft(card_class1)
	deck2 = random_draft(card_class2)
	player1 = Player("Player1", deck1, card_class1.default_hero)
	player2 = Player("Player2", deck2, card_class2.default_hero)

	game = Game(players=(player1, player2))
	game.start()

	return game


def play_turn(game):
	player = game.current_player

	while True:
		while player.choice:
			choice = random.choice(player.choice.cards)
			log.info("Choosing card %r" % (choice))
			player.choice.choose(choice)

		heropower = player.hero.power
		if heropower.is_usable() and random.random() < 0.1:
			choose = None
			target = None
			if heropower.must_choose_one:
				choose = random.choice(heropower.choose_cards)
			if heropower.requires_target():
				target = random.choice(heropower.targets)
			heropower.use(target=target, choose=choose)
			continue

		# eg. Deathstalker Rexxar
		while player.choice:
			choice = random.choice(player.choice.cards)
			log.info("Choosing card %r" % (choice))
			player.choice.choose(choice)

		# iterate over our hand and play whatever is playable
		for card in player.hand:
			if card.is_playable() and random.random() < 0.5:
				target = None
				if card.must_choose_one:
					card = random.choice(card.choose_cards)
					if not card.is_playable():
						continue
				log.info("Playing %r" % card)
				if card.requires_target():
					target = random.choice(card.targets)
				log.info("Target on %r" % target)
				card.play(target=target)

				while player.choice:
					choice = random.choice(player.choice.cards)
					log.info("Choosing card %r" % (choice))
					player.choice.choose(choice)

				continue

		# Randomly attack with whatever can attack
		for character in player.characters:
			if character.can_attack():
				character.attack(random.choice(character.targets))
				# eg. Vicious Fledgling
				while player.choice:
					choice = random.choice(player.choice.cards)
					log.info("Choosing card %r" % (choice))
					player.choice.choose(choice)

		break

	game.end_turn()
	return game


def play_full_game():
	game = setup_game()

	for player in game.players:
		log.info("Can mulligan %r" % (player.choice.cards))
		mull_count = random.randint(0, len(player.choice.cards))
		cards_to_mulligan = random.sample(player.choice.cards, mull_count)
		player.choice.choose(*cards_to_mulligan)

	while True:
		play_turn(game)

	return game
