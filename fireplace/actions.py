from enum import IntEnum
from .dsl import LazyNum, Picker, Selector
from .enums import CardType, Mulligan, PlayState, Zone
from .entity import Entity
from .utils import fireplace_logger as logger


def _eval_card(source, card):
	"""
	Return a Card instance from \a card
	The card argument can be:
	- A Card instance (nothing is done)
	- The string ID of the card (the card is created)
	- A Picker instance (a card is dynamically picked)
	"""
	if isinstance(card, Picker):
		card = card.pick(source)

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


class Action:  # Lawsuit
	class Args(IntEnum):
		"""
		Arguments given to Actions.
		Works like an IntEnum, with the value representing the argument index.
		"""
		pass

	def __init__(self, *args, **kwargs):
		self._args = args
		self._kwargs = kwargs
		self._argnames = []
		for e, arg in zip(self.Args, self._args):
			self._argnames.append(e.name)

	def __repr__(self):
		args = ["%s=%r" % (k, v) for k, v in zip(self._argnames, self._args)]
		return "<Action: %s(%s)>" % (self.__class__.__name__, ", ".join(args))

	def after(self, *actions):
		return EventListener(self, actions, EventListener.AFTER)

	def on(self, *actions):
		return EventListener(self, actions, EventListener.ON)

	def _broadcast(self, entity, source, at, *args):
		for event in entity.events:
			if event.at != at:
				continue
			if isinstance(event.trigger, self.__class__) and event.trigger.matches(entity, args):
				logger.info("%r triggers off %r from %r", entity, self, source)
				entity.trigger_event(source, event, args)

	def broadcast(self, source, at, *args):
		for entity in source.game.entities:
			self._broadcast(entity, source, at, *args)

		for entity in source.game.hands:
			self._broadcast(entity, source, at, *args)

	def get_args(self, source):
		return self._args

	def matches(self, source, args):
		for arg, match in zip(args, self._args):
			if match is None:
				# Allow matching Action(None, None, z) to Action(x, y, z)
				continue
			# this stuff is stupidslow
			res = match.eval([arg], source)
			if not res or res[0] is not arg:
				return False
		return True


class GameAction(Action):
	def trigger(self, source):
		args = self.get_args(source)
		source.game.manager.action(self, source, *args)
		self.do(source, *args)
		source.game.manager.action_end(self, source, *args)
		source.game.process_deaths()


class Attack(GameAction):
	"""
	Make \a ATTACKER attack \a DEFENDER
	"""
	class Args(Action.Args):
		ATTACKER = 0
		DEFENDER = 1

	def get_args(self, source):
		ret = super().get_args(source)
		return ret

	def do(self, source, attacker, defender):
		attacker.attacking = True
		defender.defending = True
		source.game.proposed_attacker = attacker
		source.game.proposed_defender = defender
		logger.info("%r attacks %r", attacker, defender)
		self.broadcast(source, EventListener.ON, attacker, defender)
		source.game._attack()


class BeginTurn(GameAction):
	"""
	Make \a player begin the turn
	"""
	class Args(Action.Args):
		PLAYER = 0

	def do(self, source, player):
		self.broadcast(source, EventListener.ON, player)
		source.game._begin_turn(player)


class Concede(GameAction):
	"""
	Make \a player concede
	"""
	class Args(Action.Args):
		PLAYER = 0

	def do(self, source, player):
		player.playstate = PlayState.QUIT


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
	class Args(Action.Args):
		ENTITY = 0

	def do(self, source, target):
		logger.info("Processing Death for %r", target)
		self.broadcast(source, EventListener.ON, target)
		if target.deathrattles:
			source.game.queue_actions(source, [Deathrattle(target)])


class EndTurn(GameAction):
	"""
	End the current turn
	"""
	class Args(Action.Args):
		PLAYER = 0

	def do(self, source, player):
		assert not player.choice, "Attempted to end a turn with a choice open"
		self.broadcast(source, EventListener.ON, player)
		source.game._end_turn()


class MulliganChoice(GameAction):
	class Args(Action.Args):
		PLAYER = 0

	def do(self, source, player):
		player.mulligan_state = Mulligan.INPUT
		player.choice = self
		# NOTE: Ideally, we give The Coin when the Mulligan is over.
		# Unfortunately, that's not compatible with Blizzard's way.
		self.cards = player.hand.exclude(id="GAME_005")
		self.player = player

	def choose(self, *cards):
		self.player.draw(len(cards))
		for card in cards:
			assert card in self.cards
			card.zone = Zone.DECK
		self.player.choice = None
		self.player.shuffle_deck()
		self.player.mulligan_state = Mulligan.DONE


class Play(GameAction):
	"""
	Make the source player play \a card, on \a target or None.
	Choose play action from \a choose or None.
	"""
	class Args(Action.Args):
		PLAYER = 0
		CARD = 1
		TARGET = 2
		CHOOSE = 3

	def _broadcast(self, entity, source, at, *args):
		# Prevent cards from triggering off their own play
		if entity is args[1]:
			return
		return super()._broadcast(entity, source, at, *args)

	def get_args(self, source):
		return (source, ) + super().get_args(source)

	def do(self, source, player, card, target=None, choose=None):
		card.target = target

		if choose is not None:
			# Choose One cards replace the action on the played card
			chosen = player.card(choose)
			logger.info("Choose One from %r: %r", card, chosen)
			if chosen.has_target():
				chosen.target = target
			card.chosen = chosen
		card.choose = choose

		player.game.no_aura_refresh = True
		player.game._play(card)
		# NOTE: A Play is not a summon! But it sure looks like one.
		# We need to fake a Summon broadcast.
		summon_action = Summon(player, card)
		self.broadcast(player, EventListener.ON, player, card, target, choose)
		summon_action.broadcast(player, EventListener.ON, player, card)
		player.game.no_aura_refresh = False
		player.game.refresh_auras()
		card.action()
		summon_action.broadcast(player, EventListener.AFTER, player, card)
		self.broadcast(player, EventListener.AFTER, player, card, target, choose)
		player.combo = True
		player.cards_played_this_turn += 1
		if card.type == CardType.MINION:
			player.minions_played_this_turn += 1

		card.target = None
		card.choose = None


class TargetedAction(Action):
	class Args(Action.Args):
		TARGETS = 0

	def __init__(self, *args, **kwargs):
		self.source = kwargs.pop("source", None)
		super().__init__(*args, **kwargs)
		self.times = 1

	def __repr__(self):
		args = ["%s=%r" % (k, v) for k, v in zip(self._argnames[1:], self._args[1:])]
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
		for k, v in zip(self.Args, self._args):
			if k.name == "TARGETS":
				continue
			elif isinstance(v, Selector):
				# evaluate Selector arguments
				v = v.eval(source.game, source)
			elif isinstance(v, Action.Args):
				# This is used when an event listener triggers and the callback
				# Action has arguments of the type Action.Args.FOO
				# XXX we rely on source.event_args to be set, but it's very racey.
				# If multiple events happen on an entity at once, stuff will go wrong.
				assert source.event_args
				v = source.event_args[v]
			elif isinstance(v, LazyNum):
				# evaluate LazyNum arguments into ints
				v = v.evaluate(source)
			elif k.name == "CARDS":
				# HACK: card-likes are always named Args.CARDS
				v = _eval_card(source, v)
			ret.append(v)
		return ret

	def get_targets(self, source, t):
		if isinstance(t, Entity):
			return [t]
		elif isinstance(t, Action.Args):
			return [source.event_args[t]]
		elif isinstance(t, Action):
			# eg. Unstable Portal: Buff(Give(...), ...)
			return t.trigger(source)[0]
		else:
			return t.eval(source.game, source)

	def trigger(self, source):
		ret = []

		if self.source is not None:
			source = self.source.eval(source.game, source)
			assert len(source) == 1
			source = source[0]

		times = self.times
		if isinstance(times, LazyNum):
			times = times.evaluate(source)

		for i in range(times):
			args = self.get_args(source)
			targets = self.get_targets(source, args[0])
			args = args[1:]
			source.game.manager.action(self, source, targets, *args)
			logger.info("%r triggering %r targeting %r", source, self, targets)
			for target in targets:
				target_args = self.get_target_args(source, target)
				ret.append(self.do(source, target, *target_args))
			source.game.manager.action_end(self, source, targets, *self._args)

		return ret


class Buff(TargetedAction):
	"""
	Buff character targets with Enchantment \a id
	"""
	class Args(Action.Args):
		TARGETS = 0
		BUFF = 1

	def do(self, source, target, buff):
		kwargs = self._kwargs.copy()
		for k, v in kwargs.items():
			if isinstance(v, LazyNum):
				kwargs[k] = v.evaluate(source)
		return source.buff(target, buff, **kwargs)


class SwapAttackAndHealth(Buff):
	def do(self, source, target, buff):
		logger.info("%r swaps attack and health for %r", source, target)
		buff = super().do(source, target, buff)
		atk = target.health - target.atk
		health = target.atk - target.health
		buff._atk = atk
		buff._max_health = health
		target.damage = 0
		return buff


class Bounce(TargetedAction):
	"""
	Bounce minion targets on the field back into the hand.
	"""
	def do(self, source, target):
		target.bounce()


class Counter(TargetedAction):
	"""
	Counter a card, making it unplayable.
	"""
	def do(self, source, target):
		target.cant_play = True


class Damage(TargetedAction):
	"""
	Damage target by \a amount.
	"""
	class Args(Action.Args):
		TARGETS = 0
		AMOUNT = 1

	def do(self, source, target, amount):
		amount = target._hit(source, amount)
		if amount:
			self.broadcast(source, EventListener.ON, target, amount, source)


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
				logger.info("Triggering deathrattles for %r again", target)
				source.game.queue_actions(target, actions)


class Destroy(TargetedAction):
	"""
	Destroy character targets.
	"""
	def do(self, source, target):
		target._destroy()


class Discard(TargetedAction):
	"""
	Discard card targets in a player's hand
	"""
	def do(self, source, target):
		self.broadcast(source, EventListener.ON, target)
		target.discard()


class Draw(TargetedAction):
	"""
	Make player targets draw a card from their deck.
	"""
	class Args(Action.Args):
		TARGETS = 0
		CARD = 1

	def do(self, source, target):
		if not target.deck:
			target.fatigue()
			return []
		card = target.deck[-1]
		card.draw()
		self.broadcast(source, EventListener.ON, target, card, source)

		return [card]


class ForceDraw(TargetedAction):
	"""
	Draw card targets into their owners hand
	"""
	def do(self, source, target):
		target.draw()


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
	class Args(Action.Args):
		TARGETS = 0
		AMOUNT = 1

	def do(self, source, target, amount):
		target.armor += amount
		self.broadcast(source, EventListener.ON, target, amount)


class GainMana(TargetedAction):
	"""
	Give player targets \a Mana crystals.
	"""
	class Args(Action.Args):
		TARGETS = 0
		AMOUNT = 1

	def do(self, source, target, amount):
		target.max_mana += amount


class GainEmptyMana(TargetedAction):
	"""
	Give player targets \a amount empty Mana crystals.
	"""
	class Args(Action.Args):
		TARGETS = 0
		AMOUNT = 1

	def do(self, source, target, amount):
		target.max_mana += amount
		target.used_mana += amount


class Give(TargetedAction):
	"""
	Give player targets card \a id.
	"""
	class Args(Action.Args):
		TARGETS = 0
		CARDS = 1

	def do(self, source, target, cards):
		logger.info("Giving %r to %s", cards, target)
		ret = []
		for card in cards:
			if len(target.hand) >= target.max_hand_size:
				logger.info("Give(%r) fails because %r's hand is full", card, target)
				continue
			card.controller = target
			card.zone = Zone.HAND
			ret.append(card)
		return ret


class Hit(TargetedAction):
	"""
	Hit character targets by \a amount.
	"""
	class Args(Action.Args):
		TARGETS = 0
		AMOUNT = 1

	def do(self, source, target, amount):
		source.hit(target, amount)


class Heal(TargetedAction):
	"""
	Heal character targets by \a amount.
	"""
	class Args(Action.Args):
		TARGETS = 0
		AMOUNT = 1

	def do(self, source, target, amount):
		if source.controller.outgoing_healing_adjustment:
			# "healing as damage" (hack-ish)
			return source.hit(target, amount)

		amount *= (source.controller.healing_double + 1)
		amount = min(amount, target.damage)
		if amount:
			# Undamaged targets do not receive heals
			logger.info("%r heals %r for %i", source, target, amount)
			target.damage -= amount
			self.broadcast(source, EventListener.ON, target, amount)


class ManaThisTurn(TargetedAction):
	"""
	Give player targets \a amount Mana this turn.
	"""
	class Args(Action.Args):
		TARGETS = 0
		AMOUNT = 1

	def do(self, source, target, amount):
		target.temp_mana += min(target.max_resources - target.mana, amount)


class Mill(TargetedAction):
	"""
	Mill \a count cards from the top of the player targets' deck.
	"""
	class Args(Action.Args):
		TARGETS = 0
		COUNT = 1

	def do(self, source, target, count):
		target.mill(count)


class Morph(TargetedAction):
	"""
	Morph minion target into \a minion id
	"""
	class Args(Action.Args):
		TARGETS = 0
		CARD = 1

	def get_target_args(self, source, target):
		card = _eval_card(source, self._args[1])
		assert len(card) == 1
		card = card[0]
		card.controller = target.controller
		return (card, )

	def do(self, source, target, card):
		logger.info("Morphing %r into %r", target, card)
		target.clear_buffs()
		target.zone = Zone.SETASIDE
		card.zone = Zone.PLAY
		return card


class Freeze(TargetedAction):
	"""
	Freeze character targets.
	"""
	def do(self, source, target):
		target.frozen = True


class FillMana(TargetedAction):
	"""
	Refill \a amount mana crystals from player targets.
	"""
	class Args(Action.Args):
		TARGETS = 0
		AMOUNT = 1

	def do(self, source, target, amount):
		target.used_mana -= amount


class Retarget(TargetedAction):
	class Args(Action.Args):
		TARGETS = 0
		CARDS = 1

	def do(self, source, target, new_target):
		assert len(new_target) == 1
		new_target = new_target[0]
		if target.type in (CardType.HERO, CardType.MINION) and target.attacking:
			logger.info("Retargeting %r's attack to %r", source, new_target)
			source.game.proposed_defender.defending = False
			source.game.proposed_defender = new_target
		else:
			logger.info("Retargeting %r from %r to %r", target, target.target, new_target)
			target.target = new_target

		return new_target


class Reveal(TargetedAction):
	"""
	Reveal secret targets.
	"""
	def do(self, source, target):
		logger.info("Revealing secret %r", target)
		self.broadcast(source, EventListener.ON, target)
		target.zone = Zone.GRAVEYARD


class SetCurrentHealth(TargetedAction):
	"""
	Sets the current health of the character target to \a amount.
	"""
	class Args(Action.Args):
		TARGETS = 0
		AMOUNT = 1

	def do(self, source, target, amount):
		logger.info("Setting current health on %r to %i", target, amount)
		maxhp = target.max_health
		target.damage = max(0, maxhp - amount)


class SetTag(TargetedAction):
	"""
	Sets various targets' tags to \a values.
	"""
	class Args(Action.Args):
		TARGETS = 0
		VALUES = 1

	def do(self, source, target, values):
		for k, v in values.items():
			if target.tags[k] != v:
				target.tags[k] = v


class Silence(TargetedAction):
	"""
	Silence minion targets.
	"""
	def do(self, source, target):
		target.silence()


class Summon(TargetedAction):
	"""
	Make player targets summon \a id onto their field.
	This works for equipping weapons as well as summoning minions.
	"""
	class Args(Action.Args):
		TARGETS = 0
		CARDS = 1

	def _broadcast(self, entity, source, at, *args):
		# Prevent cards from triggering off their own summon
		if entity is args[1]:
			return
		return super()._broadcast(entity, source, at, *args)

	def do(self, source, target, cards):
		logger.info("%s summons %r", target, cards)
		if not isinstance(cards, list):
			cards = [cards]

		for card in cards:
			if card.controller != target:
				card.controller = target
			if card.type == CardType.MINION and not target.minion_slots:
				continue
			self.broadcast(source, EventListener.ON, target, card)
			if card.zone != Zone.PLAY:
				card.zone = Zone.PLAY
			self.broadcast(source, EventListener.AFTER, target, card)

		return cards


class Shuffle(TargetedAction):
	"""
	Shuffle card targets into player target's deck.
	"""
	class Args(Action.Args):
		TARGETS = 0
		CARDS = 1

	def do(self, source, target, cards):
		logger.info("%r shuffles into %s's deck", cards, target)
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
	class Args(Action.Args):
		TARGETS = 0
		OTHER = 1

	def get_target_args(self, source, target):
		other = self.eval(self._args[1], source)
		if not other:
			return (None, )
		assert len(other) == 1
		return (other[0], )

	def do(self, source, target, other):
		if other is not None:
			orig = target.zone
			target.zone = other.zone
			other.zone = orig


class Steal(TargetedAction):
	"""
	Make the controller take control of targets.
	The controller is the controller of the source of the action.
	"""
	def do(self, source, target):
		logger.info("%s takes control of %r", self, target)
		zone = target.zone
		target.zone = Zone.SETASIDE
		target.controller = source.controller
		target.zone = zone


class UnlockOverload(TargetedAction):
	"""
	Unlock the target player's overload, both current and owed.
	"""
	def do(self, source, target):
		logger.info("%s overload gets cleared", target)
		target.overloaded = 0
		target.overload_locked = 0
