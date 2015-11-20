import logging


class CardList(list):
	def __contains__(self, x):
		for item in self:
			if x is item:
				return True
		return False

	def __getitem__(self, key):
		ret = super().__getitem__(key)
		if isinstance(key, slice):
			return self.__class__(ret)
		return ret

	def __int__(self):
		# Used in Kettle to easily serialize CardList to json
		return len(self)

	def contains(self, x):
		"True if list contains any instance of x"
		for item in self:
			if x == item:
				return True
		return False

	def index(self, x):
		for i, item in enumerate(self):
			if x is item:
				return i
		raise ValueError

	def remove(self, x):
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
		return self.__class__(e for k, v in kwargs.items() for e in self if getattr(e, k, 0) == v)


def random_draft(hero, exclude=[]):
	"""
	Return a deck of 30 random cards from the \a hero's collection
	"""
	import random
	from . import cards
	from .deck import Deck
	from hearthstone.enums import CardType, Rarity

	deck = []
	collection = []
	hero = getattr(cards, hero)

	for card in cards.db.keys():
		if card in exclude:
			continue
		cls = getattr(cards, card)
		if not cls.collectible:
			continue
		if cls.type == CardType.HERO:
			# Heroes are collectible...
			continue
		if cls.card_class and cls.card_class != hero.card_class:
			continue
		collection.append(cls)

	while len(deck) < Deck.MAX_CARDS:
		card = random.choice(collection)
		if card.rarity == Rarity.LEGENDARY and card.id in deck:
			continue
		elif deck.count(card.id) < Deck.MAX_UNIQUE_CARDS:
			deck.append(card.id)

	return deck

def pretty_format_game(game):
	"""
	Returns a detailed string representation of the board state from a game.
	"""
	return (pretty_format_player(game.player1)
		 + "\n\n" + pretty_format_player(game.player2))

def pretty_format_player(player):
	hero = player.hero
	power = hero.power
	weapon = player.weapon
	# This is a bit messy, consider using named parameters in the format string
	return "%s%s - %s (%d / %d%s) (Mana %d / %d) %s%s\nHand: %s\nField: %s" % (
		player.name,
		"*" if player.current_player else "",
		hero.name,
		hero.atk, hero.health,
		" + %d" % hero.armor if hero.armor > 0 else "",
		player.mana, player.max_mana,
		("(%s - %d)" % (power.name, power.cost)
			if power.is_usable()
			else "(%s)" % _strike(power.name)),
		" (%s)" % (pretty_format_weapon(weapon)) if weapon else "",
		pretty_format_hand(player.hand),
		pretty_format_field(player.field))

def pretty_format_weapon(weapon):
	return "%s (%d / %d)" % (
		weapon.name,
		weapon.atk,
		weapon.durability)

def pretty_format_hand(hand):
	return ", ".join([pretty_format_card(card) for card in hand])

def pretty_format_card(card):
	return "%s (%d)" % (card.name, card.cost)

def pretty_format_field(field):
	return ", ".join([pretty_format_minion(minion) for minion in field])

def pretty_format_minion(minion):
	# TODO(liujimj): Add more tags for can_attack, etc.
	return "%s%s (%d)%s (%d / %d%s)" % (
		minion.name,
		"*" if minion.can_attack else "",
		minion.cost,
		" (S)" if minion.silenced else "",
		minion.atk, minion.health,
		"D" if minion.damaged else "")

def _strike(text):
	return '\u0336'.join(text) + '\u0336'

def get_logger(name, level=logging.DEBUG):
	logger = logging.getLogger(name)
	logger.setLevel(level)

	if not logger.handlers:
		ch = logging.StreamHandler()
		ch.setLevel(level)

		formatter = logging.Formatter(
			"[%(name)s.%(module)s]: %(message)s",
			datefmt="%H:%M:%S"
		)
		ch.setFormatter(formatter)

		logger.addHandler(ch)

	return logger


fireplace_logger = get_logger("fireplace")
