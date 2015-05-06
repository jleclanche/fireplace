import logging
import random
import time
from calendar import timegm
from itertools import chain
from .actions import Attack, BeginTurn, Death, Deaths, EndTurn, EventListener
from .card import Card, THE_COIN
from .entity import Entity
from .enums import CardType, PlayState, Step, Zone
from .managers import GameManager
from .utils import CardList


class GameOver(Exception):
	pass


class Game(Entity):
	type = CardType.GAME
	MAX_MINIONS_ON_FIELD = 8
	Manager = GameManager

	def __init__(self, players):
		self.data = None
		super().__init__()
		self.players = players
		for player in players:
			player.game = self
		self.step = Step.BEGIN_FIRST
		self.turn = 0
		self.currentPlayer = None
		self.auras = []
		self._actionQueue = []

	def __repr__(self):
		return "<%s %s>" % (self.__class__.__name__, self)

	def __str__(self):
		return "%s vs %s" % (self.players)

	def __iter__(self):
		return self.allEntities.__iter__()

	@property
	def board(self):
		return CardList(chain(self.player1.field, self.player2.field))

	@property
	def decks(self):
		return CardList(chain(self.player1.deck, self.player2.deck))

	@property
	def hands(self):
	    return CardList(chain(self.player1.hand, self.player2.hand))

	@property
	def characters(self):
		return CardList(chain(self.player1.characters, self.player2.characters))

	@property
	def allEntities(self):
		return CardList(chain(self.entities, self.hands, self.decks))

	@property
	def entities(self):
		return CardList(chain([self], self.player1.entities, self.player2.entities))

	@property
	def liveEntities(self):
		return CardList(chain(self.player1.liveEntities, self.player2.liveEntities))

	def filter(self, *args, **kwargs):
		return self.allEntities.filter(*args, **kwargs)

	def attack(self, source, target):
		return self.queueActions(source, [Attack(source, target)])

	def _attack(self):
		"""
		See https://github.com/jleclanche/fireplace/wiki/Combat
		for information on how attacking works
		"""
		attacker = self.proposedAttacker
		defender = self.proposedDefender
		self.proposedAttacker = None
		self.proposedDefender = None
		if attacker.shouldExitCombat:
			logging.info("Attack has been interrupted.")
			attacker.shouldExitCombat = False
			attacker.attacking = False
			defender.defending = False
			return
		# Save the attacker/defender atk values in case they change during the attack
		# (eg. in case of Enrage)
		attAtk = attacker.atk
		defAtk = defender.atk
		attacker.hit(defender, attAtk)
		if defAtk:
			defender.hit(attacker, defAtk)
		if attacker.type == CardType.HERO and attacker.controller.weapon:
			attacker.controller.weapon.loseDurability()
		attacker.attacking = False
		defender.defending = False
		attacker.numAttacks += 1

	def card(self, id):
		card = Card(id)
		self.manager.new_entity(card)
		return card

	def end(self, *losers):
		"""
		End the game.
		\a *losers: Players that lost the game.
		"""
		for player in self.players:
			if player in losers:
				player.playstate = PlayState.LOST
			else:
				player.playstate = PlayState.WON
		raise GameOver("The game has ended.")

	def processDeaths(self):
		return self.queueActions(self, [Deaths()])

	def _processDeaths(self):
		actions = []
		losers = []
		for card in self.liveEntities:
			if card.toBeDestroyed:
				actions.append(Death(card))
				if card.type == CardType.MINION:
					self.minionsKilledThisTurn += 1
					card.controller.minionsKilledThisTurn += 1
				elif card.type == CardType.HERO:
					card.controller.playstate = PlayState.LOSING
					losers.append(card.controller)

		if losers:
			self.end(*losers)
			return

		if actions:
			self.queueActions(self, actions)

	def queueActions(self, source, actions):
		"""
		Queue a list of \a actions for processing from \a source.
		"""
		ret = []
		for action in actions:
			if isinstance(action, EventListener):
				logging.debug("Registering %r on %r", action, self)
				source.controller._events.append(action)
			else:
				self._actionQueue.append(action)
				ret.append(action.trigger(source, self))
				self.refreshAuras()
				self._actionQueue.pop()
		if not self._actionQueue:
			self._processDeaths()

		return ret

	def tossCoin(self):
		outcome = random.randint(0, 1)
		# player who wins the outcome is the index
		winner = self.players[outcome]
		loser = winner.opponent
		logging.info("Tossing the coin... %s wins!" % (winner))
		return winner, loser

	def refreshAuras(self):
		for aura in self.auras:
			aura.update()

	def start(self):
		logging.info("Starting game: %r" % (self))
		self.player1, self.player2 = self.tossCoin()
		self.manager.new_entity(self.player1)
		self.manager.new_entity(self.player2)
		self.currentPlayer = self.player1
		# XXX: Mulligan events should handle the following, but unimplemented for now
		self.player1.cardsDrawnThisTurn = 0
		self.player2.cardsDrawnThisTurn = 0
		for player in self.players:
			player.zone = Zone.PLAY
			player.summon(player.originalDeck.hero)
			for card in player.originalDeck:
				card.controller = player
				card.zone = Zone.DECK
			player.shuffleDeck()
			player.playstate = PlayState.PLAYING

		self.player1.draw(3)
		self.player2.draw(4)
		self.beginMulligan()
		self.player1.firstPlayer = True
		self.player2.firstPlayer = False

	def beginMulligan(self):
		logging.info("Entering mulligan phase")
		self.step = Step.BEGIN_MULLIGAN
		self.nextStep = Step.MAIN_READY
		logging.info("%s gets The Coin (%s)" % (self.player2, THE_COIN))
		self.player2.give(THE_COIN)
		self.beginTurn(self.player1)

	def endTurn(self):
		return self.queueActions(self, [EndTurn(self.currentPlayer)])

	def _endTurn(self):
		logging.info("%s ends turn %i", self.currentPlayer, self.turn)
		self.step, self.nextStep = self.nextStep, Step.MAIN_CLEANUP

		self.currentPlayer.tempMana = 0
		for character in self.currentPlayer.characters.filter(frozen=True):
			if not character.numAttacks:
				character.frozen = False
		for buff in self.currentPlayer.entities.filter(oneTurnEffect=True):
			logging.info("Ending One-Turn effect: %r", buff)
			buff.destroy()

		self.step, self.nextStep = self.nextStep, Step.MAIN_NEXT
		self.beginTurn(self.currentPlayer.opponent)

	def beginTurn(self, player):
		return self.queueActions(self, [BeginTurn(player)])

	def _beginTurn(self, player):
		self.step, self.nextStep = self.nextStep, Step.MAIN_START_TRIGGERS
		self.step, self.nextStep = self.nextStep, Step.MAIN_START
		self.turn += 1
		logging.info("%s begins turn %i", player, self.turn)
		self.step, self.nextStep = self.nextStep, Step.MAIN_ACTION
		self.currentPlayer = player
		self.minionsKilledThisTurn = 0

		for p in self.players:
			p.cardsDrawnThisTurn = 0
			p.currentPlayer = p is player

		player.turnStart = timegm(time.gmtime())
		player.cardsPlayedThisTurn = 0
		player.minionsPlayedThisTurn = 0
		player.minionsKilledThisTurn = 0
		player.combo = False
		player.maxMana += 1
		player.usedMana = player.overloaded
		player.overloaded = 0
		for entity in player.entities:
			if entity.type != CardType.PLAYER:
				entity.turnsInPlay += 1
				if entity.type == CardType.HERO_POWER:
					entity.exhausted = False
				elif entity.type in (CardType.HERO, CardType.MINION):
					entity.numAttacks = 0

		player.draw()
