from collections import OrderedDict
from inspect import isclass
from hearthstone.enums import BlockType, CardType, CardClass, Mulligan, PlayState, Step, Zone, PlayReq, Race
from .dsl import LazyNum, LazyValue, Selector, RandomSelector
from .entity import Entity
from .logging import log
from .exceptions import InvalidAction
from .utils import random_class
from . import enums
import random


def _eval_card(source, card):
	"""
	Return a Card instance from \a card
	The card argument can be:
	- A Card instance (nothing is done)
	- The string ID of the card (the card is created)
	- A LazyValue (the card is dynamically created)
	"""
	if isinstance(card, LazyValue):
		card = card.evaluate(source)

	if isinstance(card, Action):
		card = card.trigger(source)[0]

	if not isinstance(card, list):
		cards = [card]
	else:
		cards = card

	ret = []
	for card in cards:
		if isinstance(card, str):
			ret.append(source.controller.card(card, source))
		else:
			ret.append(card)

	return ret


class EventListener:
	ON = 1
	AFTER = 2

	def __init__(self, trigger, actions, at):
		self.trigger = trigger
		self.actions = actions
		self.at = at
		self.once = False

	def __repr__(self):
		return "<EventListener %r>" % (self.trigger)


class ActionMeta(type):
	def __new__(metacls, name, bases, namespace):
		cls = type.__new__(metacls, name, bases, dict(namespace))
		argslist = []
		for k, v in namespace.items():
			if not isinstance(v, ActionArg):
				continue
			v._setup(len(argslist), k, cls)
			argslist.append(v)
		cls.ARGS = tuple(argslist)
		return cls

	@classmethod
	def __prepare__(metacls, name, bases):
		return OrderedDict()


class ActionArg(LazyValue):
	def _setup(self, index, name, owner):
		self.index = index
		self.name = name
		self.owner = owner

	def __repr__(self):
		return "<%s.%s>" % (self.owner.__name__, self.name)

	def evaluate(self, source):
		# This is used when an event listener triggers and the callback
		# Action has arguments of the type Action.FOO
		# XXX we rely on source.event_args to be set, but it's very racey.
		# If multiple events happen on an entity at once, stuff will go wrong.
		assert source.event_args
		return source.event_args[self.index]


class CardArg(ActionArg):
	# Type hint
	pass


class IntArg(ActionArg, LazyNum):
	def evaluate(self, source):
		ret = super().evaluate(source)
		return self.num(ret)


class Action(metaclass=ActionMeta):
	def __init__(self, *args, **kwargs):
		self._args = args
		self._kwargs = kwargs
		self.callback = ()
		self.times = 1
		self.event_queue = []

	def __repr__(self):
		args = ["%s=%r" % (k, v) for k, v in zip(self.ARGS, self._args)]
		return "<Action: %s(%s)>" % (self.__class__.__name__, ", ".join(args))

	def after(self, *actions):
		return EventListener(self, actions, EventListener.AFTER)

	def on(self, *actions):
		return EventListener(self, actions, EventListener.ON)

	def then(self, *args):
		"""
		Create a callback containing an action queue, called upon the
		action's trigger with the action's arguments available.
		"""
		ret = self.__class__(*self._args, **self._kwargs)
		ret.callback = args
		ret.times = self.times
		return ret

	def _broadcast(self, entity, source, at, *args):
		for event in entity.events:
			if event.at != at:
				continue
			if isinstance(event.trigger, self.__class__) and event.trigger.matches(entity, args):
				log.info("%r triggers off %r from %r", entity, self, source)
				entity.trigger_event(source, event, args)

	def broadcast(self, source, at, *args):
		for entity in source.game.entities:
			self._broadcast(entity, source, at, *args)

		for entity in source.game.hands:
			self._broadcast(entity, source, at, *args)

		for entity in source.game.decks:
			self._broadcast(entity, source, at, *args)

		for entity in source.game.graveyard:
			if entity.tags[enums.DISCARDED]:
				self._broadcast(entity, source, at, *args)

	def queue_broadcast(self, obj, args):
		self.event_queue.append((obj, args))

	def resolve_broadcasts(self):
		for obj, args in self.event_queue:
			obj.broadcast(*args)
		self.event_queue = []

	def get_args(self, source):
		return self._args

	def matches(self, source, args):
		for arg, match in zip(args, self._args):
			if match is None:
				# Allow matching Action(None, None, z) to Action(x, y, z)
				continue
			if arg is None:
				# We got an arg of None and a match not None. Bad.
				return False
			if callable(match):
				res = match(arg)
				if not res:
					return False
			else:
				# this stuff is stupidslow
				res = match.eval([arg], source)
				if not res or res[0] is not arg:
					return False
		return True


class GameAction(Action):
	def trigger(self, source):
		args = self.get_args(source)
		self.do(source, *args)


class Attack(GameAction):
	"""
	Make \a ATTACKER attack \a DEFENDER
	"""
	ATTACKER = ActionArg()
	DEFENDER = ActionArg()

	def get_args(self, source):
		ret = super().get_args(source)
		return ret

	def do(self, source, attacker, defender):
		log.info("%r attacks %r", attacker, defender)
		attacker.attack_target = defender
		defender.defending = True
		source.game.proposed_attacker = attacker
		source.game.proposed_defender = defender
		source.game.manager.step(Step.MAIN_COMBAT, Step.MAIN_ACTION)
		source.game.refresh_auras()  # XXX Needed for Gorehowl
		self.broadcast(source, EventListener.ON, attacker, defender)

		defender = source.game.proposed_defender
		source.game.proposed_attacker = None
		source.game.proposed_defender = None
		if attacker.should_exit_combat:
			log.info("Attack has been interrupted.")
			attacker.attack_target = None
			defender.defending = False
			return

		assert attacker is not defender, "Why are you hitting yourself %r?" % (attacker)

		# Save the attacker/defender atk values in case they change during the attack
		# (eg. in case of Enrage)
		def_atk = defender.atk
		source.game.queue_actions(attacker, [Hit(defender, attacker.atk)])
		if def_atk:
			source.game.queue_actions(defender, [Hit(attacker, def_atk)])

		self.broadcast(source, EventListener.AFTER, attacker, defender)

		attacker.attack_target = None
		defender.defending = False
		attacker.num_attacks += 1


class BeginTurn(GameAction):
	"""
	Make \a player begin the turn
	"""
	PLAYER = ActionArg()

	def do(self, source, player):
		source.manager.step(source.next_step, Step.MAIN_READY)
		source.turn += 1
		source.log("%s begins turn %i", player, source.turn)
		source.current_player = player
		source.manager.step(source.next_step, Step.MAIN_START_TRIGGERS)
		source.manager.step(source.next_step, source.next_step)
		self.broadcast(source, EventListener.ON, player)
		source._begin_turn(player)


class Concede(GameAction):
	"""
	Make \a player concede
	"""
	PLAYER = ActionArg()

	def do(self, source, player):
		player.playstate = PlayState.CONCEDED
		source.game.check_for_end_game()


class Disconnect(GameAction):
	"""
	Make \a player disconnect
	"""
	PLAYER = ActionArg()

	def do(self, source, player):
		player.playstate = PlayState.DISCONNECTED


class Deaths(GameAction):
	"""
	Process all deaths in the PLAY Zone.
	"""
	def do(self, source, *args):
		source.game.process_deaths()


class Death(GameAction):
	"""
	Move target to the GRAVEYARD Zone.
	"""
	ENTITY = ActionArg()

	def do(self, source, target):
		log.info("Processing Death for %r", target)
		self.broadcast(source, EventListener.ON, target)
		if target.deathrattles:
			source.game.queue_actions(source, [Deathrattle(target)])
		target.reset()


class EndTurn(GameAction):
	"""
	End the current turn
	"""
	PLAYER = ActionArg()

	def do(self, source, player):
		if player.choice:
			raise InvalidAction("%r cannot end turn with the open choice %r." % (player, player.choice))
		self.broadcast(source, EventListener.ON, player)
		source.game._end_turn()


class Joust(GameAction):
	"""
	Perform a joust between \a challenger and \a defender.
	Note that this does not evaluate the results of the joust. For that,
	see dsl.evaluators.JoustEvaluator.
	"""
	CHALLENGER = ActionArg()
	DEFENDER = ActionArg()

	def get_args(self, source):
		challenger = self._args[0].eval(source.game, source)
		defender = self._args[1].eval(source.game, source)
		return challenger and challenger[0], defender and defender[0]

	def do(self, source, challenger, defender):
		log.info("Jousting %r vs %r", challenger, defender)
		source.game.joust(source, challenger, defender, self.callback)


class GenericChoice(GameAction):
	PLAYER = ActionArg()
	CARDS = ActionArg()

	def get_args(self, source):
		player = self._args[0]
		if isinstance(player, Selector):
			player = player.eval(source.game.players, source)
			assert len(player) == 1
			player = player[0]
		cards = self._args[1]
		if isinstance(cards, Selector):
			cards = cards.eval(source.game, source)
		elif isinstance(cards, LazyValue):
			cards = cards.evaluate(source)

		for card in cards:
			card.zone = Zone.SETASIDE

		return player, cards

	def do(self, source, player, cards):
		player.choice = self
		self.source = source
		self.player = player
		self.cards = cards
		self.min_count = 1
		self.max_count = 1

	def choose(self, card):
		if card not in self.cards:
			raise InvalidAction("%r is not a valid choice (one of %r)" % (card, self.cards))
		for _card in self.cards:
			if _card is card:
				if card.type == CardType.HERO_POWER:
					_card.zone = Zone.PLAY
				elif self.source.id in ["UNG_088", "UNG_211"]:
					self.player.game.cheat_action(self.source, [CastSpell(card)])
				elif len(self.player.hand) < self.player.max_hand_size:
					_card.zone = Zone.HAND
				else:
					_card.discard()
			else:
				_card.discard()
		self.player.choice = None


class MulliganChoice(GameAction):
	PLAYER = ActionArg()

	def __init__(self, *args, callback):
		super().__init__(*args)
		self.callback = callback

	def do(self, source, player):
		player.mulligan_state = Mulligan.INPUT
		player.choice = self
		# NOTE: Ideally, we give The Coin when the Mulligan is over.
		# Unfortunately, that's not compatible with Blizzard's way.
		self.cards = player.hand.exclude(id="GAME_005")
		self.source = source
		self.player = player
		self.min_count = 0
		# but weirdly, the game server includes the coin in the mulligan count
		self.max_count = len(player.hand)

	def choose(self, *cards):
		self.player.draw(len(cards))
		for card in cards:
			assert card in self.cards
			card.zone = Zone.DECK
		self.player.choice = None
		self.player.shuffle_deck()
		self.player.mulligan_state = Mulligan.DONE

		if self.player.opponent.mulligan_state == Mulligan.DONE:
			self.callback()


class Play(GameAction):
	"""
	Make the source player play \a card, on \a target or None.
	Choose play action from \a choose or None.
	"""
	PLAYER = ActionArg()
	CARD = CardArg()
	TARGET = ActionArg()
	INDEX = IntArg()
	CHOOSE = ActionArg()

	def _broadcast(self, entity, source, at, *args):
		# Prevent cards from triggering off their own play
		if entity is args[1]:
			return
		return super()._broadcast(entity, source, at, *args)

	def do(self, source, card, target, index, choose):
		player = source
		log.info("%s plays %r (target=%r, index=%r)", player, card, target, index)

		player.pay_cost(card, card.cost)

		card.target = target
		card._summon_index = index

		battlecry_card = choose or card
		# We check whether the battlecry will trigger, before the card.zone changes
		if battlecry_card.battlecry_requires_target() and not target:
			log.info("%r requires a target for its battlecry. Will not trigger.")
			trigger_battlecry = False
		else:
			trigger_battlecry = True

		card.zone = Zone.PLAY

		# NOTE: A Play is not a summon! But it sure looks like one.
		# We need to fake a Summon broadcast.
		summon_action = Summon(player, card)

		if card.type in (CardType.MINION, CardType.WEAPON):
			self.queue_broadcast(summon_action, (player, EventListener.ON, player, card))
		self.broadcast(player, EventListener.ON, player, card, target)
		self.resolve_broadcasts()

		# "Can't Play" (aka Counter) means triggers don't happen either
		if not card.cant_play:
			if trigger_battlecry:
				source.game.queue_actions(card, [Battlecry(battlecry_card, card.target)])

			# If the play action transforms the card (eg. Druid of the Claw), we
			# have to broadcast the morph result as minion instead.
			played_card = card.morphed or card
			if played_card.type in (CardType.MINION, CardType.WEAPON):
				summon_action.broadcast(player, EventListener.AFTER, player, played_card)
			elif played_card.type == CardType.SPELL:
				player.spells_played_this_game += 1
				from .card import Secret
				if isinstance(played_card, Secret):
					player.secrets_played_this_game += 1
			self.broadcast(player, EventListener.AFTER, player, played_card, target)

		player.combo = True
		player.last_card_played = card
		player.cards_played_this_turn += 1
		if card.type == CardType.MINION:
			player.minions_played_this_turn += 1
			if card.race == Race.TOTEM:
				player.totems_played_this_game += 1
				
		card.target = None
		card.choose = None


class Activate(GameAction):
	PLAYER = ActionArg()
	CARD = CardArg()
	TARGET = ActionArg()

	def get_args(self, source):
		return (source, ) + super().get_args(source)

	def do(self, source, player, heropower, target=None):
		player.pay_cost(heropower, heropower.cost)
		self.broadcast(source, EventListener.ON, player, heropower, target)

		actions = heropower.get_actions("activate")
		source.game.action_start(BlockType.PLAY, heropower, 0, target)
		source.game.main_power(heropower, actions, target)
		source.game.action_end(BlockType.PLAY, heropower)

		for minion in player.field.filter(has_inspire=True):
			actions = minion.get_actions("inspire")
			if actions is None:
				raise NotImplementedError("Missing inspire script for %r" % (minion))
			source.game.trigger(minion, actions, event_args=None)

		heropower.activations_this_turn += 1


class Overload(GameAction):
	PLAYER = ActionArg()
	AMOUNT = IntArg()

	def do(self, source, player, amount):
		if player.cant_overload:
			log.info("%r cannot overload %s", source, player)
			return
		log.info("%r overloads %s for %i", source, player, amount)
		self.broadcast(source, EventListener.ON, player, amount)
		player.overloaded += amount


class TargetedAction(Action):
	TARGET = ActionArg()

	def __init__(self, *args, **kwargs):
		self.source = kwargs.pop("source", None)
		super().__init__(*args, **kwargs)
		self.trigger_index = 0

	def __repr__(self):
		args = ["%s=%r" % (k, v) for k, v in zip(self.ARGS[1:], self._args[1:])]
		return "<TargetedAction: %s(%s)>" % (self.__class__.__name__, ", ".join(args))

	def __mul__(self, value):
		self.times = value
		return self

	def eval(self, selector, source):
		if isinstance(selector, Entity):
			return [selector]
		else:
			return selector.eval(source.game, source)

	def get_target_args(self, source, target):
		ret = []
		for k, v in zip(self.ARGS[1:], self._args[1:]):
			if isinstance(v, Selector):
				# evaluate Selector arguments
				v = v.eval(source.game, source)
			elif isinstance(v, LazyValue):
				v = v.evaluate(source)
			elif isinstance(k, CardArg):
				v = _eval_card(source, v)
			ret.append(v)
		return ret

	def get_targets(self, source, t):
		if isinstance(t, Entity):
			ret = t
		elif isinstance(t, LazyValue):
			ret = t.evaluate(source)
		else:
			ret = t.eval(source.game, source)
		if not ret:
			return []
		if not hasattr(ret, "__iter__"):
			# Bit of a hack to ensure we always get a list back
			ret = [ret]
		return ret

	def trigger(self, source):
		ret = []

		if self.source is not None:
			source = self.source.eval(source.game, source)
			assert len(source) == 1
			source = source[0]

		times = self.times
		if isinstance(times, LazyValue):
			times = times.evaluate(source)
		elif isinstance(times, Action):
			times = times.trigger(source)[0]

		for i in range(times):
			self.trigger_index = i
			args = self.get_args(source)
			targets = self.get_targets(source, args[0])
			args = args[1:]
			log.info("%r triggering %r targeting %r", source, self, targets)
			for target in targets:
				target_args = self.get_target_args(source, target)
				ret.append(self.do(source, target, *target_args))

				for action in self.callback:
					log.info("%r queues up callback %r", self, action)
					ret += source.game.queue_actions(source, [action], event_args=[target] + target_args)

		self.resolve_broadcasts()

		return ret


class Buff(TargetedAction):
	"""
	Buff character targets with Enchantment \a id
	NOTE: Any Card can buff any other Card. The controller of the
	Card that buffs the target becomes the controller of the buff.
	"""
	TARGET = ActionArg()
	BUFF = ActionArg()

	def get_target_args(self, source, target):
		buff = self._args[1]
		buff = source.controller.card(buff)
		buff.source = source
		return [buff]

	def do(self, source, target, buff):
		kwargs = self._kwargs.copy()
		for k, v in kwargs.items():
			if isinstance(v, LazyValue):
				v = v.evaluate(source)
			setattr(buff, k, v)
		return buff.apply(target)


class Bounce(TargetedAction):
	"""
	Bounce minion targets on the field back into the hand.
	"""
	def do(self, source, target):
		if len(target.controller.hand) >= target.controller.max_hand_size:
			log.info("%r is bounced to a full hand and gets destroyed", target)
			return source.game.queue_actions(source, [Destroy(target)])
		else:
			log.info("%r is bounced back to %s's hand", target, target.controller)
			target.reset()
			target.zone = Zone.HAND


class CopyDeathrattles(TargetedAction):
	"""
	Copy the deathrattles from a card onto the target
	"""
	TARGET = ActionArg()
	DEATHRATTLES = ActionArg()

	def do(self, source, target, entities):
		for entity in entities:
			for deathrattle in entity.deathrattles:
				target.additional_deathrattles.append(deathrattle)


class Counter(TargetedAction):
	"""
	Counter a card, making it unplayable.
	"""
	def do(self, source, target):
		target.cant_play = True


class Predamage(TargetedAction):
	"""
	Predamage target by \a amount.
	"""
	TARGET = ActionArg()
	AMOUNT = IntArg()

	def do(self, source, target, amount):
		for i in range(target.incoming_damage_multiplier):
			amount *= 2
		target.predamage = amount
		if amount:
			self.broadcast(source, EventListener.ON, target, amount)
			return source.game.trigger_actions(source, [Damage(target)])[0][0]
		return 0


class Damage(TargetedAction):
	"""
	Damage target by \a amount.
	"""
	TARGET = ActionArg()
	AMOUNT = IntArg()

	def get_target_args(self, source, target):
		return [target.predamage]

	def do(self, source, target, amount):
		amount = target._hit(target.predamage)
		target.predamage = 0
		if source.type == CardType.MINION and source.stealthed:
			# TODO this should be an event listener of sorts
			source.stealthed = False
		if amount:
			self.broadcast(source, EventListener.ON, target, amount, source)
		return amount


class Deathrattle(TargetedAction):
	"""
	Trigger deathrattles on card targets.
	"""
	def do(self, source, target):
		for deathrattle in target.deathrattles:
			if callable(deathrattle):
				actions = deathrattle(target)
			else:
				actions = deathrattle
			source.game.queue_actions(target, actions)

			if target.controller.extra_deathrattles:
				log.info("Triggering deathrattles for %r again", target)
				source.game.queue_actions(target, actions)


class Battlecry(TargetedAction):
	"""
	Trigger Battlecry on card targets
	"""
	CARD = CardArg()
	TARGET = ActionArg()

	def get_target_args(self, source, target):
		arg = self._args[1]
		if isinstance(arg, Selector):
			arg = arg.eval(source.game, source)
			assert len(arg) == 1
			arg = arg[0]
		return [arg]

	def do(self, source, card, target):
		player = card.controller

		if card.has_combo and player.combo:
			log.info("Activating %r combo targeting %r", card, target)
			actions = card.get_actions("combo")
		else:
			log.info("Activating %r action targeting %r", card, target)
			actions = card.get_actions("play")

		source.target = target
		source.game.main_power(source, actions, target)

		if player.extra_battlecries and card.has_battlecry:
			source.game.main_power(source, actions, target)

		if card.overload:
			source.game.queue_actions(card, [Overload(player, card.overload)])


class Destroy(TargetedAction):
	"""
	Destroy character targets.
	"""
	def do(self, source, target):
		if target.delayed_destruction:
			#  If the card is in PLAY, it is instead scheduled to be destroyed
			# It will be moved to the graveyard on the next Death event
			log.info("%r marks %r for imminent death", source, target)
			target.to_be_destroyed = True
		else:
			log.info("%r destroys %r", source, target)
			if target.type == CardType.ENCHANTMENT:
				target.remove()
			else:
				target.reset()
				target.zone = Zone.GRAVEYARD


class Discard(TargetedAction):
	"""
	Discard card targets in a player's hand
	"""
	TARGET = ActionArg()
	def do(self, source, target):
		self.broadcast(source, EventListener.ON, target)
		target.discard()
		self.broadcast(source, EventListener.AFTER, target)


class Discover(TargetedAction):
	"""
	Opens a generic choice for three random cards matching a filter.
	"""
	TARGET = ActionArg()
	CARDS = CardArg()

	def get_target_args(self, source, target):
		if target.hero.data.card_class != CardClass.NEUTRAL:
			# use hero class for Discover if not neutral (eg. Ragnaros)
			discover_class = target.hero.data.card_class
		elif source.data.card_class != CardClass.NEUTRAL:
			# use card class for neutral hero classes
			discover_class = source.data.card_class
		else:
			# use random class for neutral hero classes with neutral cards
			discover_class = random_class()

		picker = self._args[1] * 3
		picker = picker.copy_with_weighting(1, card_class=CardClass.NEUTRAL)
		picker = picker.copy_with_weighting(4, card_class=discover_class)
		return [picker.evaluate(source)]

	def do(self, source, target, cards):
		log.info("%r discovers %r for %s", source, cards, target)
		source.game.queue_actions(source, [GenericChoice(target, cards)])


class Draw(TargetedAction):
	"""
	Make player targets draw a card from their deck.
	"""
	TARGET = ActionArg()
	CARD = CardArg()

	def get_target_args(self, source, target):
		if target.deck:
			card = target.deck[-1]
		else:
			card = None
		return [card]

	def do(self, source, target, card):
		if card is None:
			target.fatigue()
			return []
		card.draw()
		self.broadcast(source, EventListener.ON, target, card, source)

		return [card]


class Fatigue(TargetedAction):
	"""
	Hit a player with a tick of fatigue
	"""
	def do(self, source, target):
		if target.cant_fatigue:
			log.info("%s can't fatigue and does not take damage", target)
			return
		target.fatigue_counter += 1
		log.info("%s takes %i fatigue damage", target, target.fatigue_counter)
		return source.game.queue_actions(source, [Hit(target.hero, target.fatigue_counter)])


class ForceDraw(TargetedAction):
	"""
	Draw card targets into their owners hand
	"""
	def do(self, source, target):
		target.draw()


class DrawUntil(TargetedAction):
	"""
	Make target player target draw up to \a amount cards minus their hand count.
	"""
	TARGET = ActionArg()
	AMOUNT = IntArg()

	def do(self, source, target, amount):
		difference = max(0, amount - len(target.hand))
		if difference > 0:
			return source.game.queue_actions(source, [Draw(target) * difference])


class FullHeal(TargetedAction):
	"""
	Fully heal character targets.
	"""
	def do(self, source, target):
		source.heal(target, target.max_health)


class GainArmor(TargetedAction):
	"""
	Make hero targets gain \a amount armor.
	"""
	TARGET = ActionArg()
	AMOUNT = IntArg()

	def do(self, source, target, amount):
		target.armor += amount
		self.broadcast(source, EventListener.ON, target, amount)


class GainMana(TargetedAction):
	"""
	Give player targets \a Mana crystals.
	"""
	TARGET = ActionArg()
	AMOUNT = IntArg()

	def do(self, source, target, amount):
		target.max_mana = max(target.max_mana + amount, 0)


class SpendMana(TargetedAction):
	"""
	Make player targets spend \a amount Mana.
	"""
	TARGET = ActionArg()
	AMOUNT = IntArg()

	def do(self, source, target, amount):
		# TODO(czxcjx): Maybe merge this with player.pay_cost()?
		used_temp = max(0, min(target.temp_mana, amount))
		amount -= used_temp
		target.temp_mana -= used_temp
		target.used_mana = max(target.used_mana + amount, 0)


class Give(TargetedAction):
	"""
	Give player targets card \a id.
	"""
	TARGET = ActionArg()
	CARD = CardArg()

	def do(self, source, target, cards):
		log.info("Giving %r to %s", cards, target)
		ret = []
		if not hasattr(cards, "__iter__"):
			# Support Give on multiple cards at once (eg. Echo of Medivh)
			cards = [cards]
		for card in cards:
			if len(target.hand) >= target.max_hand_size:
				log.info("Give(%r) fails because %r's hand is full", card, target)
				continue
			card.controller = target
			card.zone = Zone.HAND
			ret.append(card)
		return ret


class Hit(TargetedAction):
	"""
	Hit character targets by \a amount.
	"""
	TARGET = ActionArg()
	AMOUNT = IntArg()

	def do(self, source, target, amount):
		amount = source.get_damage(amount, target)
		if amount:
			return source.game.queue_actions(source, [Predamage(target, amount)])[0][0]
		return 0


class Heal(TargetedAction):
	"""
	Heal character targets by \a amount.
	"""
	TARGET = ActionArg()
	AMOUNT = IntArg()

	def do(self, source, target, amount):
		if source.controller.healing_as_damage:
			return source.game.queue_actions(source, [Hit(target, amount)])

		amount <<= source.controller.healing_double
		amount = min(amount, target.damage)
		if amount:
			# Undamaged targets do not receive heals
			log.info("%r heals %r for %i", source, target, amount)
			target.damage -= amount
			self.queue_broadcast(self, (source, EventListener.ON, target, amount))


class ManaThisTurn(TargetedAction):
	"""
	Give player targets \a amount Mana this turn.
	"""
	TARGET = ActionArg()
	AMOUNT = IntArg()

	def do(self, source, target, amount):
		target.temp_mana += min(target.max_resources - target.mana, amount)


class Mill(TargetedAction):
	"""
	Mill \a count cards from the top of the player targets' deck.
	"""
	TARGET = ActionArg()
	AMOUNT = IntArg()

	def do(self, source, target, count):
		target.mill(count)


class Morph(TargetedAction):
	"""
	Morph minion target into \a minion id
	"""
	TARGET = ActionArg()
	CARD = CardArg()

	def get_target_args(self, source, target):
		card = _eval_card(source, self._args[1])
		assert len(card) == 1
		card = card[0]
		card.controller = target.controller
		return [card]

	def do(self, source, target, card):
		log.info("Morphing %r into %r", target, card)
		target_zone = target.zone
		if card.zone != target_zone:
			# Transfer the zone position
			card._summon_index = target.zone_position
			# In-place morph is OK, eg. in the case of Lord Jaraxxus
			card.zone = target_zone
		target.clear_buffs()
		target.zone = Zone.SETASIDE
		target.morphed = card
		return card


class FillMana(TargetedAction):
	"""
	Refill \a amount mana crystals from player targets.
	"""
	TARGET = ActionArg()
	AMOUNT = IntArg()

	def do(self, source, target, amount):
		target.used_mana -= amount


class Retarget(TargetedAction):
	TARGET = ActionArg()
	CARD = CardArg()

	def do(self, source, target, new_target):
		if not new_target:
			return
		assert len(new_target) == 1
		new_target = new_target[0]
		if target.type in (CardType.HERO, CardType.MINION) and target.attacking:
			log.info("Retargeting %r's attack to %r", target, new_target)
			source.game.proposed_defender.defending = False
			source.game.proposed_defender = new_target
		else:
			log.info("Retargeting %r from %r to %r", target, target.target, new_target)
			target.target = new_target

		return new_target


class Reveal(TargetedAction):
	"""
	Reveal secret targets.
	"""
	def do(self, source, target):
		log.info("Revealing secret %r", target)
		self.broadcast(source, EventListener.ON, target)
		target.zone = Zone.GRAVEYARD


class CompleteQuest(TargetedAction):
	"""
	Quest progress + 1
	"""
	CARD = CardArg()

	def do(self, source, card):
		if source.id != "UNG_116": # Not Rogue Quest
			source.quest_progress += 1
		else:
			name = card.data.__str__()
			if name in source.quest_map:
				source.quest_map[name] += 1
			else:
				source.quest_map[name] = 1
			source.quest_progress = max(source.quest_progress, source.quest_map[name])
		log.info("Complete Quest %r, Process %r/%r", source, source.quest_progress, source.quest_progress_total)
		if source.quest_progress >= source.quest_progress_total:
			log.info("Get quest reward")
			action = source.data.scripts.reward
			source.game.main_power(source, action, None)


class SetCurrentHealth(TargetedAction):
	"""
	Sets the current health of the character target to \a amount.
	"""
	TARGET = ActionArg()
	AMOUNT = IntArg()

	def do(self, source, target, amount):
		log.info("Setting current health on %r to %i", target, amount)
		maxhp = target.max_health
		target.damage = max(0, maxhp - amount)


class SetTag(TargetedAction):
	"""
	Sets targets' given tags.
	"""
	TARGET = ActionArg()
	TAGS = ActionArg()

	def do(self, source, target, tags):
		if isinstance(tags, dict):
			for tag, value in tags.items():
				target.tags[tag] = value
		else:
			for tag in tags:
				target.tags[tag] = True


class UnsetTag(TargetedAction):
	"""
	Unset targets' given tags.
	"""
	TARGET = ActionArg()
	TAGS = ActionArg()

	def do(self, source, target, tags):
		for tag in tags:
			target.tags[tag] = False


class Silence(TargetedAction):
	"""
	Silence minion targets.
	"""
	TARGET = ActionArg()
	def do(self, source, target):
		log.info("Silencing %r", self)
		self.broadcast(source, EventListener.ON, target)

		target.clear_buffs()
		for attr in target.silenceable_attributes:
			if getattr(target, attr):
				setattr(target, attr, False)

		# Handle spellpower
		if getattr(target, "spellpower"):
			setattr(target, "spellpower", 0)

		# Wipe the event listeners
		target._events = []
		target.silenced = True


class Summon(TargetedAction):
	"""
	Make player targets summon \a id onto their field.
	This works for equipping weapons as well as summoning minions.
	"""
	TARGET = ActionArg()
	CARD = CardArg()

	def _broadcast(self, entity, source, at, *args):
		# Prevent cards from triggering off their own summon
		if entity is args[1]:
			return
		return super()._broadcast(entity, source, at, *args)

	def do(self, source, target, cards):
		log.info("%s summons %r", target, cards)
		if not isinstance(cards, list):
			cards = [cards]

		for card in cards:
			if not card.is_summonable():
				continue
			if card.controller != target:
				card.controller = target
			if card.zone != Zone.PLAY:
				if source.type == CardType.MINION and source.zone == Zone.PLAY:
					source_index = source.controller.field.index(source)
					card._summon_index = source_index + ((self.trigger_index + 1) % 2)
				card.zone = Zone.PLAY
			if hasattr(card, 'race') and card.race == Race.TOTEM:
				card.controller.totems_played_this_game += 1
			self.queue_broadcast(self, (source, EventListener.ON, target, card))
			self.broadcast(source, EventListener.AFTER, target, card)

		return cards

class Shuffle(TargetedAction):
	"""
	Shuffle card targets into player target's deck.
	"""
	TARGET = ActionArg()
	CARD = CardArg()

	def do(self, source, target, cards):
		log.info("%r shuffles into %s's deck", cards, target)
		if not isinstance(cards, list):
			cards = [cards]

		for card in cards:
			if card.controller != target:
				card.controller = target
			card.zone = Zone.DECK
			target.shuffle_deck()


class Swap(TargetedAction):
	"""
	Swap minion target with \a other.
	Behaviour is undefined when swapping more than two minions.
	"""
	TARGET = ActionArg()
	OTHER = ActionArg()

	def get_target_args(self, source, target):
		other = self.eval(self._args[1], source)
		if not other:
			return (None, )
		assert len(other) == 1
		return [other[0]]

	def do(self, source, target, other):
		if other is not None:
			orig = target.zone
			target.zone = other.zone
			other.zone = orig


class SwapHealth(TargetedAction):
	"""
	Swap health between two minions using \a buff.
	"""
	TARGET = ActionArg()
	OTHER = ActionArg()
	BUFF = ActionArg()

	def do(self, source, target, other, buff):
		other = other[0]
		buff1 = source.controller.card(buff)
		buff1.health = other.health
		buff2 = source.controller.card(buff)
		buff2.health = target.health
		buff1.apply(target)
		buff2.apply(other)


class Steal(TargetedAction):
	"""
	Make the controller take control of targets.
	The controller is the controller of the source of the action.
	"""
	TARGET = ActionArg()
	CONTROLLER = ActionArg()

	def get_target_args(self, source, target):
		if len(self._args) > 1:
			# Controller was specified
			controller = self.eval(self._args[1], source)
			assert len(controller) == 1
			controller = controller[0]
		else:
			# Default to the source's controller
			controller = source.controller
		return [controller]

	def do(self, source, target, controller):
		log.info("%s takes control of %r", controller, target)
		zone = target.zone
		target.zone = Zone.SETASIDE
		target.controller = controller
		target.turns_in_play = 0  # To ensure summoning sickness
		target.zone = zone


class UnlockOverload(TargetedAction):
	"""
	Unlock the target player's overload, both current and owed.
	"""
	def do(self, source, target):
		log.info("%s overload gets cleared", target)
		target.overloaded = 0
		target.overload_locked = 0

class SummonJadeGolem(TargetedAction):
	"""
	Summons a Jade Golem for target player according to his Jade Golem Status
	"""
	TARGET = ActionArg()
	CARD = CardArg()

	def get_target_args(self, source, target):
		jade_size = "CFM_712_t" + str(target.jade_golem).zfill(2)
		return _eval_card(source, jade_size)

	def do(self, source, target, card):
		log.info("%s summons a Jade Golem for %s", source, target)
		target.jade_golem = target.jade_golem+1 if target.jade_golem <=29 else 30
		#jade_golem = _eval_card(source, jade_size)[0]
		if card.is_summonable():
			card.zone = Zone.PLAY
			summon_action = Summon(target, card)
			self.queue_broadcast(summon_action, (target, EventListener.ON, target, card))
			self.broadcast(target, EventListener.ON, target, card)
			self.resolve_broadcasts()

class ExtraAttack(TargetedAction):
	"""
	Get target an extra attack change
	"""
	TARGET = ActionArg()

	def do(self, source, target):
		log.info("%s gets an extra attack change.", target)
		target.num_attacks -= 1

class CastSpell(TargetedAction):
	"""
	Cast Random Spell, Target Random
	"""
	CARD = CardArg()

	def is_playable(self, card):
		zone = card.parent_card.zone if card.parent_card else card.zone
		if PlayReq.REQ_NUM_MINION_SLOTS in card.requirements:
			if card.requirements[PlayReq.REQ_NUM_MINION_SLOTS] > card.controller.minion_slots:
				return False
		if len(card.controller.opponent.field) < card.requirements.get(PlayReq.REQ_MINIMUM_ENEMY_MINIONS, 0):
			return False
		if len(card.controller.game.board) < card.requirements.get(PlayReq.REQ_MINIMUM_TOTAL_MINIONS, 0):
			return False
		if PlayReq.REQ_ENTIRE_ENTOURAGE_NOT_IN_PLAY in card.requirements:
			if not [id for id in card.entourage if not card.controller.field.contains(id)]:
				return False
		if PlayReq.REQ_WEAPON_EQUIPPED in card.requirements:
			if not card.controller.weapon:
				return False
		if PlayReq.REQ_FRIENDLY_MINION_DIED_THIS_GAME in card.requirements:
			if not card.controller.graveyard.filter(type=CardType.MINION):
				return False
		if card.controller.secrets.contains(card):
			return False
		return True

	def is_valid_target(self, card, target, requirements = None):
		if target.type == CardType.MINION:
			if target.dead:
				return False
		
		if requirements is None:
			requirements = card.requirements

		for req, param in requirements.items():
			if req == PlayReq.REQ_MINION_TARGET:
				if target.type != CardType.MINION:
					return False
			elif req == PlayReq.REQ_FRIENDLY_TARGET:
				if target.controller != card.controller:
					return False
			elif req == PlayReq.REQ_ENEMY_TARGET:
				if target.controller == card.controller:
					return False
			elif req == PlayReq.REQ_DAMAGED_TARGET:
				if not target.damage:
					return False
			elif req == PlayReq.REQ_FROZEN_TARGET:
				if not target.frozen:
					return False
			elif req == PlayReq.REQ_TARGET_MAX_ATTACK:
				if target.atk > param or 0:
					return False
			elif req == PlayReq.REQ_TARGET_WITH_RACE:
				if target.type != CardType.MINION or target.race != param:
					return False
			elif req == PlayReq.REQ_HERO_TARGET:
				if target.type != CardType.HERO:
					return False
			elif req == PlayReq.REQ_TARGET_MIN_ATTACK:
				if target.atk < param or 0:
					return False
			elif req == PlayReq.REQ_MUST_TARGET_TAUNTER:
				if not target.taunt:
					return False
			elif req == PlayReq.REQ_UNDAMAGED_TARGET:
				if target.damage:
					return False
			elif req == PlayReq.REQ_LEGENDARY_TARGET:
				if target.rarity != Rarity.LEGENDARY:
					return False
			elif req == PlayReq.REQ_TARGET_WITH_BATTLECRY:
				if not target.has_battlecry:
					return False
			elif req == PlayReq.REQ_TARGET_WITH_DEATHRATTLE:
				if not target.has_deathrattle:
					return False

			return True

	def play_targets(self, card):
		return [target for target in card.game.characters if self.is_valid_target(card, target)]

	def do(self, source, cards):
		player = source.controller
		if not isinstance(cards, list):
			cards = [cards]	
		if not(source.zone == Zone.PLAY and not(source.dead) and not(source.silenced)):
			return
		for card in cards:
			log.info("%r casting spell %r", source, card)
			if card.has_choose_one and not(player.choose_both):
				card = random.choice(card.get_actions("choose"))
				log.info("Random choosing %r", card)

			if self.is_playable(card) == False:
				log.info("%r isn't playable", card)
				return

			targets = self.play_targets(card)
			if len(targets) > 0:
				target = random.choice(targets)
				log.info("Choosing target %r", target)
			else:
				target = None

			if card.has_combo and player.combo:
				log.info("Activating %r combo targeting %r", card, target)
				actions = card.get_actions("combo")
			else:
				log.info("Activating %r action targeting %r", card, target)
				actions = card.get_actions("play")

			source.target = target
			source.game.main_power(source, actions, target)

			if card.overload:
				source.game.queue_actions(card, [Overload(player, card.overload)])

			while player.choice:
				choice = random.choice(player.choice.cards)
				print("Choosing card %r" % (choice))
				player.choice.choose(choice)


class SwapState(TargetedAction):
	"""
	Swap health between two minions using \a buff.
	"""
	TARGET = ActionArg()
	OTHER = ActionArg()
	BUFF = ActionArg()

	def do(self, source, target, other, buff):
		other = other[0]
		buff1 = source.controller.card(buff)
		buff1.atk = other.atk - target.atk
		buff1.health = other.health
		buff2 = source.controller.card(buff)
		buff2.atk = target.atk - other.atk
		buff2.health = target.health
		buff1.apply(target)
		buff2.apply(other)

class SetState(TargetedAction):
	"""
	Copy target attack and health using \a buff.
	"""
	TARGET = ActionArg()
	OTHER = ActionArg()
	BUFF = ActionArg()

	def do(self, source, target, other, buff):
		other = other[0]
		buff1 = source.controller.card(buff)
		buff1.atk = other.atk - target.atk
		buff1.health = other.health
		buff1.apply(target)

class BuffState(TargetedAction):
	"""
	Buff target with other state
	"""
	TARGET = ActionArg()
	OTHER = ActionArg()
	BUFF = ActionArg()

	def do(self, source, target, other, buff):
		other = other[0]
		buff1 = source.controller.card(buff)
		buff1.atk = other.atk
		buff1.health = other.health + target.health
		buff1.apply(target)

class Kazakus(TargetedAction):
	PLAYER = ActionArg()

	def do(self, source, player):
		if not(player.choice):
			player.choice = self
		else:
			player.next_choice.append(self)
		self.source = source
		self.player = player
		cards = ["CFM_621t11", "CFM_621t12", "CFM_621t13"]
		choose_list = []
		for card in cards:
			choose_list.append(player.card(card))
		self.cards = choose_list
		self.min_count = 1
		self.max_count = 1
		player.kazakus = []

	def choose(self, card):
		if card not in self.cards:
			raise InvalidAction("%r is not a valid choice (one of %r)" % (card, self.cards))
		self.player.kazakus.append(card)
		self.player.choice = None
		self.player.game.queue_actions(self.source, [Kazakus_step2(self.player)])

class Kazakus_step2(TargetedAction):
	PLAYER = ActionArg()

	def do(self, source, player):
		player.choice = self
		self.source = source
		self.player = player
		cards = random.sample([["CFM_621t2", "CFM_621t3", "CFM_621t4", "CFM_621t5",
			"CFM_621t6", "CFM_621t8", "CFM_621t9",
			"CFM_621t10", "CFM_621t37"],
				["CFM_621t16", "CFM_621t17", "CFM_621t18", "CFM_621t19",
			"CFM_621t20", "CFM_621t21", "CFM_621t22",
			"CFM_621t23", "CFM_621t24", "CFM_621t38"],
				["CFM_621t25", "CFM_621t26", "CFM_621t27", "CFM_621t28",
			"CFM_621t29", "CFM_621t30", "CFM_621t31",
			"CFM_621t32", "CFM_621t33", "CFM_621t39"]][player.kazakus[0].cost//5], 3)
		choose_list = []
		for card in cards:
			choose_list.append(player.card(card))
		self.cards = choose_list
		self.min_count = 1
		self.max_count = 1

	def choose(self, card):
		if card not in self.cards:
			raise InvalidAction("%r is not a valid choice (one of %r)" % (card, self.cards))
		self.player.kazakus.append(card)
		self.player.choice = None
		self.player.game.queue_actions(self.source, [Kazakus_step3(self.player)])

class Kazakus_step3(TargetedAction):
	PLAYER = ActionArg()

	def do(self, source, player):
		player.choice = self
		self.source = source
		self.player = player
		cards = [["CFM_621t2", "CFM_621t3", "CFM_621t4", "CFM_621t5",
			"CFM_621t6", "CFM_621t8", "CFM_621t9",
			"CFM_621t10", "CFM_621t37"],
				["CFM_621t16", "CFM_621t17", "CFM_621t18", "CFM_621t19",
			"CFM_621t20", "CFM_621t21", "CFM_621t22",
			"CFM_621t23", "CFM_621t24", "CFM_621t38"],
				["CFM_621t25", "CFM_621t26", "CFM_621t27", "CFM_621t28",
			"CFM_621t29", "CFM_621t30", "CFM_621t31",
			"CFM_621t32", "CFM_621t33", "CFM_621t39"]][player.kazakus[0].cost//5]
		cards.remove(player.kazakus[1].id)
		cards = random.sample(cards, 3)
		choose_list = []
		for card in cards:
			choose_list.append(player.card(card))
		self.cards = choose_list
		self.min_count = 1
		self.max_count = 1

	def choose(self, card):
		if card not in self.cards:
			raise InvalidAction("%r is not a valid choice (one of %r)" % (card, self.cards))
		self.player.kazakus.append(card)
		if not(self.player.next_choice):
			self.player.choice = None
		else:
			self.player.choice = self.player.next_choice.pop(0)
		potion = self.player.card(["CFM_621t", "CFM_621t14", "CFM_621t15"][self.player.kazakus[0].cost//5])
		if self.player.kazakus[1].id > self.player.kazakus[2].id:
			(self.player.kazakus[1], self.player.kazakus[2]) = (self.player.kazakus[2], self.player.kazakus[1])
		potion.data.scripts.play = self.player.kazakus[1].data.scripts.play + self.player.kazakus[2].data.scripts.play
		self.player.give(potion)
		self.player.kazakus = []


class Adapt(GameAction):
	TARGET = ActionArg()

	def get_args(self, source):
		cards = self._args[0]
		if isinstance(cards, Selector):
			cards = cards.eval(source.game, source)
		elif isinstance(cards, LazyValue):
			cards = cards.evaluate(source)

		return [cards]

	def do(self, source, target):
		if not(source.controller.choice):
			source.controller.choice = self
		else:
			source.controller.next_choice.append(self)
		self.source = source
		self.target = target
		if not isinstance(target, list):
			self.target = [target]
		log.info("TARGET: %r", target)
		self.player = source.controller
		cards = ["UNG_999t10","UNG_999t2","UNG_999t3",
			"UNG_999t4","UNG_999t5","UNG_999t6",
			"UNG_999t7","UNG_999t8","UNG_999t13","UNG_999t14"]
		cards = random.sample(cards, 3)
		choose_list = []
		for card in cards:
			choose_list.append(self.player.card(card))
		log.info("%r adpating, adapt choose list is %r", self.target, choose_list)
		self.cards = choose_list
		self.min_count = 1
		self.max_count = 1
		
	def choose(self, card):
		if card not in self.cards:
			raise InvalidAction("%r is not a valid choice (one of %r)" % (card, self.cards))
		if not(self.player.next_choice):
			self.player.choice = None
		else:
			self.player.choice = self.player.next_choice.pop(0)
		log.info("%r adapting, adapt choose is %r", self.target, card)
		actions = card.get_actions("play")
		log.info(actions)
		for v in self.target:
			self.source.target = v
			self.source.game.main_power(self.source, actions, v)