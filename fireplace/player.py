import logging
from itertools import chain
from .card import Card
from .entity import Entity
from .enums import CardType, GameTag, Zone
from .targeting import *
from .utils import CardList, _TAG


class Player(Entity):
	maxHandSize = _TAG(GameTag.MAXHANDSIZE, 10)
	maxResources = _TAG(GameTag.MAXRESOURCES, 10)

	def __init__(self, name, deck):
		self.name = name
		self.deck = deck
		for card in self.deck:
			card.controller = self
		self.deck.hero.controller = self
		self.hand = CardList()
		self.field = CardList()
		self.secrets = CardList()
		self.fatigueCounter = 0
		# set to False after the player has finished his mulligan
		self.canMulligan = True
		super().__init__()

	def __str__(self):
		return self.name

	def __repr__(self):
		return "%s(name=%r, deck=%r)" % (self.__class__.__name__, self.name, self.deck)

	@property
	def mana(self):
		mana = max(0, self.maxMana - self.usedMana) + self.tempMana
		return mana

	@property
	def spellPower(self):
		return sum(minion.spellPower for minion in self.field)

	@property
	def entities(self):
		ret = []
		for entity in self.field:
			ret += entity.entities
		# Secrets are only active on the opponent's turn
		if not self.currentPlayer:
			for entity in self.secrets:
				ret += entity.entities
		# Note: Board receives TURN_BEGIN before player
		return chain(list(self.hero.entities), ret, [self])

	@property
	def opponent(self):
		# Hacky.
		return [p for p in self.game.players if p != self][0]

	# for debugging
	def give(self, id):
		card = Card(id)
		logging.debug("Giving %r to %s" % (card, self))
		card.controller = self
		card.zone = Zone.HAND
		return card

	def getTargets(self, t):
		ret = []
		if t & TARGET_FRIENDLY:
			if t & TARGET_HAND:
				ret += self.hand
			if t & TARGET_HERO:
				ret.append(self.hero)
			if t & TARGET_WEAPON:
				if self.hero.weapon:
					ret.append(self.hero.weapon)
			if t & TARGET_MINION:
				if t & TARGET_MULTIPLE:
					ret += self.field
		if t & TARGET_ENEMY:
			if t & TARGET_HAND:
				ret += self.opponent.hand
			if t & TARGET_HERO:
				ret.append(self.opponent.hero)
			if t & TARGET_WEAPON:
				if self.opponent.hero.weapon:
					ret.append(self.opponent.hero.weapon)
			if t & TARGET_MINION:
				if t & TARGET_MULTIPLE:
					ret += self.opponent.field
		return ret

	def getById(self, id):
		"Helper to get a card from the hand by its id"
		for card in self.hand:
			if card.id == id:
				return card
		raise ValueError

	def discardHand(self):
		logging.info("%r discards his entire hand!" % (self))
		# iterate the list in reverse so we don't skip over cards in the process
		# yes it's stupid.
		for card in self.hand[::-1]:
			card.discard()

	def draw(self, count=1):
		if count == 1:
			if not self.deck:
				card = None
			else:
				card = self.deck[-1]
			self.game.broadcast("DRAW", self, card)
			logging.info("%s draws %r" % (self, card))
			return card
		else:
			ret = []
			while count:
				ret.append(self.draw())
				count -= 1
			return ret

	def mill(self, count=1):
		if count == 1:
			if not self.deck:
				return
			else:
				card = self.deck[-1]
			self.game.broadcast("MILL", self, card)
			logging.info("%s mills %r" % (self, card))
			return card
		else:
			ret = []
			while count:
				ret.append(self.mill())
				count -= 1
			return ret

	def fatigue(self):
		self.fatigueCounter += 1
		logging.info("%s takes %i fatigue damage" % (self, self.fatigueCounter))
		self.hero.hit(self.hero, self.fatigueCounter)

	currentPlayer = _TAG(GameTag.CURRENT_PLAYER, False)
	combo = _TAG(GameTag.COMBO_ACTIVE, False)
	overloaded = _TAG(GameTag.RECALL_OWED, 0)
	tempMana = _TAG(GameTag.TEMP_RESOURCES, 0)
	usedMana = _TAG(GameTag.RESOURCES_USED, 0)
	cardsPlayedThisTurn = _TAG(GameTag.NUM_CARDS_PLAYED_THIS_TURN, 0)
	lastCardPlayed = _TAG(GameTag.LAST_CARD_PLAYED, None)
	minionsPlayedThisTurn = _TAG(GameTag.NUM_MINIONS_PLAYED_THIS_TURN, 0)
	minionsKilledThisTurn = _TAG(GameTag.NUM_MINIONS_PLAYER_KILLED_THIS_TURN, 0)

	@property
	def maxMana(self):
		return self.tags.get(GameTag.RESOURCES, 0)

	@maxMana.setter
	def maxMana(self, amount):
		self.tags[GameTag.RESOURCES] = min(self.maxResources, max(0, amount))
		logging.info("%s is now at %i mana crystals" % (self, amount))

	def takeControl(self, minion):
		logging.info("%s takes control of %r" % (self, minion))
		self.opponent.field.remove(minion)
		self.field.append(minion)
		minion.controller = self

	def summon(self, card):
		"""
		Puts \a card in the PLAY zone
		"""
		if isinstance(card, str):
			card = Card(card)
			card.controller = self
		logging.debug("%s summons %r" % (self, card))
		card.zone = Zone.PLAY
		card.summon()
		return card

	def play(self, card, target=None, choose=None):
		"""
		Plays \a card from the player's hand
		"""
		logging.info("%s plays %r from their hand" % (self, card))
		assert card.controller
		self.game.broadcast("CARD_PLAYED", self, card)
		if card.hasTarget():
			assert target
			card.target = target
		cost = card.cost
		if self.tempMana:
			# The coin, Innervate etc
			cost -= self.tempMana
			self.tempMana = max(0, self.tempMana - card.cost)
		self.usedMana += cost
		self.summon(card)
		# Card must already be on the field for action()
		if choose:
			# Choose One cards replace the action on the played card
			assert choose in card.data.chooseCards
			chosen = Card(choose)
			chosen.controller = self
			logging.info("Choose One from %r: %r", card, chosen)
			card.action = chosen.action
			if chosen.hasTarget():
				chosen.target = target
			chosen.action()
			if chosen.target:
				chosen.target = None
		else:
			card.action()
		if not self.combo:
			self.combo = True
		self.game.broadcast("AFTER_CARD_PLAYED", self, card)
		if card.target:
			card.target = None
		self.lastCardPlayed = card

	##
	# Events

	events = [
		"BEFORE_OWN_ATTACK", "OWN_ATTACK",
		"OWN_TURN_BEGIN", "TURN_END",
		"OWN_DRAW",
		"OWN_DAMAGE", "OWN_HEAL",
		"OWN_CARD_PLAYED", "CARD_PLAYED",
		"AFTER_CARD_PLAYED", "AFTER_OWN_CARD_PLAYED",
		"OWN_MINION_DESTROY",
		"MINION_SUMMON",
	]

	def broadcast(self, event, *args):
		# Broadcast things to the hand if requested
		for entity in self.hand:
			for f in entity._eventListeners.get(event, []):
				if getattr(f, "zone", Zone.PLAY) == Zone.HAND:
					f(*args)
		super().broadcast(event, *args)

	def BEFORE_OWN_ATTACK(self, source, target):
		source.broadcast("BEFORE_SELF_ATTACK", target)

	def OWN_ATTACK(self, source, target):
		source.broadcast("SELF_ATTACK", target)

	def OWN_TURN_BEGIN(self):
		self.combo = False
		self.cardsPlayedThisTurn = 0
		self.minionsPlayedThisTurn = 0
		self.maxMana += 1
		self.usedMana = self.overloaded
		if self.overloaded:
			self.overloaded = 0
		self.draw()

	def TURN_END(self, *args):
		if self.tempMana:
			self.tempMana = 0

	def OWN_DRAW(self, card):
		if not card:
			self.fatigue()
			return

		if len(self.hand) > self.maxHandSize:
			logging.info("%s overdraws and loses %r!" % (self, card))
			card.destroy()
		else:
			card.zone = Zone.HAND

	def OWN_CARD_PLAYED(self, card):
		if card.overload:
			logging.info("%s is overloaded for %i mana" % (self, self.overloaded))
			self.overloaded += card.overload

	def OWN_DAMAGE(self, source, target, amount):
		target.broadcast("SELF_DAMAGE", source, amount)

	def OWN_HEAL(self, source, target, amount):
		target.broadcast("SELF_HEAL", source, amount)

	def CARD_PLAYED(self, player, card):
		if player is self:
			card.controller.broadcast("OWN_CARD_PLAYED", card)
		card.broadcast("SELF_CARD_PLAYED")

	def AFTER_CARD_PLAYED(self, player, card):
		if player is self:
			card.controller.broadcast("AFTER_OWN_CARD_PLAYED", card)
		card.broadcast("AFTER_SELF_CARD_PLAYED")

	def AFTER_OWN_CARD_PLAYED(self, card):
		self.cardsPlayedThisTurn += 1
		if card.type == CardType.MINION:
			self.minionsPlayedThisTurn += 1

	def MINION_SUMMON(self, player, minion):
		if player is self:
			minion.controller.broadcast("OWN_MINION_SUMMON", minion)
