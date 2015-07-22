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


class BaseGame(Entity):
	type = CardType.GAME
	MAX_MINIONS_ON_FIELD = 7
	Manager = GameManager

	def __init__(self, players):
		self.data = None
		super().__init__()
		self.players = players
		for player in players:
			player.game = self
		self.step = None
		self.next_step = None
		self.turn = 0
		self.current_player = None
		self.auras = []
		self.graveyard = CardList()
		self.minions_killed_this_turn = CardList()
		self.no_aura_refresh = False

	def __repr__(self):
		return "<%s %s>" % (self.__class__.__name__, self)

	def __str__(self):
		return "%s vs %s" % (self.players)

	def __iter__(self):
		return self.all_entities.__iter__()

	@property
	def game(self):
		return self

	@property
	def board(self):
		return CardList(chain(self.players[0].field, self.players[1].field))

	@property
	def decks(self):
		return CardList(chain(self.players[0].deck, self.players[1].deck))

	@property
	def hands(self):
		return CardList(chain(self.players[0].hand, self.players[1].hand))

	@property
	def characters(self):
		return CardList(chain(self.players[0].characters, self.players[1].characters))

	@property
	def all_entities(self):
		return CardList(chain(self.entities, self.hands, self.decks, self.graveyard))

	@property
	def entities(self):
		return CardList(chain([self], self.players[0].entities, self.players[1].entities))

	@property
	def live_entities(self):
		return CardList(chain(self.players[0].live_entities, self.players[1].live_entities))

	def filter(self, *args, **kwargs):
		return self.all_entities.filter(*args, **kwargs)

	def attack(self, source, target):
		return self.queue_actions(source, [Attack(source, target)])

	def _attack(self):
		"""
		See https://github.com/jleclanche/fireplace/wiki/Combat
		for information on how attacking works
		"""
		attacker = self.proposed_attacker
		defender = self.proposed_defender
		self.proposed_attacker = None
		self.proposed_defender = None
		if attacker.should_exit_combat:
			logging.info("Attack has been interrupted.")
			attacker.should_exit_combat = False
			attacker.attacking = False
			defender.defending = False
			return
		# Save the attacker/defender atk values in case they change during the attack
		# (eg. in case of Enrage)
		def_atk = defender.atk
		attacker.hit(defender, attacker.atk)
		if def_atk:
			defender.hit(attacker, def_atk)
		attacker.attacking = False
		defender.defending = False
		attacker.num_attacks += 1

	def _play(self, card):
		"""
		Plays \a card from a Player's hand
		"""
		player = card.controller
		logging.info("%s plays %r", player, card)
		cost = card.cost
		if player.temp_mana:
			# The coin, Innervate etc
			cost -= player.temp_mana
			player.temp_mana = max(0, player.temp_mana - card.cost)
		player.used_mana += cost
		if card.overload:
			logging.info("%s overloads for %i mana", player, card.overload)
			player.overloaded += card.overload
		player.last_card_played = card
		card.zone = Zone.PLAY

	def card(self, id):
		card = Card(id)
		self.manager.new_entity(card)
		return card

	def check_for_end_game(self):
		"""
		Check if one or more player is currently losing.
		End the game if they are.
		"""
		gameover = False
		for player in self.players:
			if player.playstate == PlayState.LOSING:
				player.playstate = PlayState.LOST
				gameover = True

		if gameover:
			for player in self.players:
				if player.playstate != PlayState.LOST:
					player.playstate = PlayState.WON
			raise GameOver("The game has ended.")

	def process_deaths(self):
		actions = []
		for card in self.live_entities:
			if card.to_be_destroyed:
				actions += self._schedule_death(card)

		self.check_for_end_game()

		if actions:
			self.queue_actions(self, actions)

	def _schedule_death(self, card):
		"""
		Prepare a card for its death. Will run any related Death
		trigger attached to the Game object.
		Returns a list of actions to perform during the death sweep.
		"""
		logging.debug("Scheduling death for %r", card)
		card.ignore_events = True
		card.zone = Zone.GRAVEYARD
		self.graveyard.append(card)
		if card.type == CardType.MINION:
			self.minions_killed_this_turn.append(card)
			card.controller.minions_killed_this_turn += 1
		elif card.type == CardType.HERO:
			card.controller.playstate = PlayState.LOSING

		return [Death(card)]

	def queue_actions(self, source, actions):
		"""
		Queue a list of \a actions for processing from \a source.
		"""
		ret = []
		if not hasattr(actions, "__iter__"):
			actions = (actions, )

		for action in actions:
			if isinstance(action, EventListener):
				logging.debug("Registering %r on %r", action, self)
				source.controller._events.append(action)
			else:
				ret.append(action.trigger(source))
				self.refresh_auras()

		return ret

	def pick_first_player(self):
		"""
		Picks and returns first player, second player
		In the default implementation, the first player is always
		"Player 0". Use CoinRules to decide it randomly.
		"""
		return self.players[0], self.players[1]

	def refresh_auras(self):
		if self.no_aura_refresh:
			return
		for aura in self.auras:
			aura.update()

	def prepare(self):
		self.players[0].opponent = self.players[1]
		self.players[1].opponent = self.players[0]
		for player in self.players:
			self.manager.new_entity(player)
			player.zone = Zone.PLAY
			player.summon(player.original_deck.hero)
			for card in player.original_deck:
				card.controller = player
				card.zone = Zone.DECK
			player.shuffle_deck()
			player.playstate = PlayState.PLAYING
			player.cards_drawn_this_turn = 0

		first, second = self.pick_first_player()
		self.player1 = first
		self.player1.first_player = True
		self.player2 = second
		self.player2.first_player = False
		self.player1.draw(3)
		self.player2.draw(4)
		self.current_player = self.player1

	def start(self):
		logging.info("Starting game: %r" % (self))
		self.prepare()
		self.begin_turn(self.player1)

	def end_turn(self):
		return self.queue_actions(self, [EndTurn(self.current_player)])

	def _end_turn(self):
		logging.info("%s ends turn %i", self.current_player, self.turn)
		self.step, self.next_step = self.next_step, Step.MAIN_CLEANUP

		self.current_player.temp_mana = 0
		for character in self.current_player.characters.filter(frozen=True):
			if not character.num_attacks:
				character.frozen = False
		for buff in self.current_player.entities.filter(one_turn_effect=True):
			logging.info("Ending One-Turn effect: %r", buff)
			buff.destroy()

		self.step, self.next_step = self.next_step, Step.MAIN_NEXT
		self.begin_turn(self.current_player.opponent)

	def begin_turn(self, player):
		return self.queue_actions(self, [BeginTurn(player)])

	def _begin_turn(self, player):
		self.step, self.next_step = self.next_step, Step.MAIN_START_TRIGGERS
		self.step, self.next_step = self.next_step, Step.MAIN_START
		self.turn += 1
		logging.info("%s begins turn %i", player, self.turn)
		self.step, self.next_step = self.next_step, Step.MAIN_ACTION
		self.current_player = player
		self.minions_killed_this_turn = CardList()

		for p in self.players:
			p.cards_drawn_this_turn = 0
			p.current_player = p is player

		player.turn_start = timegm(time.gmtime())
		player.cards_played_this_turn = 0
		player.minions_played_this_turn = 0
		player.minions_killed_this_turn = 0
		player.combo = False
		player.max_mana += 1
		player.used_mana = player.overloaded
		player.overloaded = 0
		for entity in player.entities:
			if entity.type != CardType.PLAYER:
				entity.turns_in_play += 1
				if entity.type == CardType.HERO_POWER:
					entity.exhausted = False
				elif entity.type in (CardType.HERO, CardType.MINION):
					entity.num_attacks = 0

		player.draw()


class CoinRules:
	"""
	Randomly determines the starting player when the Game starts.
	The second player gets "The Coin" (GAME_005).
	"""
	def pick_first_player(self):
		winner = random.choice(self.players)
		logging.info("Tossing the coin... %s wins!", winner)
		return winner, winner.opponent

	def start(self):
		super().start()
		logging.info("%s gets The Coin (%s)", self.player2, THE_COIN)
		self.player2.give(THE_COIN)


class MulliganRules:
	"""
	Performs a Mulligan phase when the Game starts.
	Currently just a dummy phase.
	"""
	def start(self):
		self.next_step = Step.BEGIN_MULLIGAN
		super().start()
		self.begin_mulligan()

	def begin_mulligan(self):
		logging.info("Entering mulligan phase")
		self.step, self.next_step = self.next_step, Step.MAIN_READY


class Game(MulliganRules, CoinRules, BaseGame):
	pass
