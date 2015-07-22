import logging
from itertools import chain
from .dsl import LazyNum, Picker, Selector
from .enums import CardType, PowSubType, Zone
from .entity import Entity


def _eval_card(source, card):
	"""
	Return a Card instance from \a card
	The card argument can be:
	- A Card instance (nothing is done)
	- The string ID of the card (the card is created)
	- A Picker instance (a card is dynamically picked)
	"""

	if isinstance(card, Picker):
		c = card.pick(source)
		card = [entity.id if not isinstance(entity, str) else entity for entity in c]

	if not isinstance(card, list):
		cards = [card]
	else:
		cards = card

	ret = []
	for card in cards:
		if isinstance(card, str):
			ret.append(source.game.card(card))
		else:
			ret.append(card)

	return ret


class EventListener:
	ON = 1
	AFTER = 2

	def __init__(self, trigger, actions, at, zone=Zone.PLAY, once=False):
		self.trigger = trigger
		self.actions = actions
		self.at = at
		self.once = once
		self.in_hand = zone == Zone.HAND

	def __repr__(self):
		return "<EventListener %r>" % (self.trigger)


class Action:  # Lawsuit
	args = ()
	type = PowSubType.TRIGGER

	def __init__(self, *args, **kwargs):
		self._args = args
		for k, v in zip(self.args, args):
			setattr(self, k, v)

	def __repr__(self):
		args = ["%s=%r" % (k, v) for k, v in zip(self.args, self._args)]
		return "<Action: %s(%s)>" % (self.__class__.__name__, ", ".join(args))

	def after(self, *actions, zone=Zone.PLAY):
		return EventListener(self, actions, EventListener.AFTER, zone=zone)

	def on(self, *actions, zone=Zone.PLAY):
		return EventListener(self, actions, EventListener.ON, zone=zone)

	def once(self, *actions, zone=Zone.PLAY):
		return EventListener(self, actions, EventListener.ON, zone=zone, once=True)

	def _broadcast(self, entity, source, at, *args):
		for event in entity._events:
			if entity.zone == Zone.HAND and not event.in_hand:
				continue
			if isinstance(event.trigger, self.__class__) and event.at == at and event.trigger.matches(entity, args):
				actions = []
				for action in event.actions:
					if callable(action):
						ac = action(entity, *args)
						if not ac:
							# Handle falsy returns
							continue
						if not hasattr(ac, "__iter__"):
							actions.append(ac)
						else:
							actions += action(entity, *args)
					else:
						actions.append(action)
				logging.debug("%r triggers off %r from %r", entity, self, source)
				source.game.queue_actions(entity, actions)
				if event.once:
					entity._events.remove(event)

	def broadcast(self, source, at, *args):
		for entity in source.game.hands:
			self._broadcast(entity, source, at, *args)

		for entity in source.game.entities:
			zone = getattr(entity, "zone", Zone.INVALID)
			if zone not in (Zone.PLAY, Zone.SECRET):
				continue
			self._broadcast(entity, source, at, *args)

	def matches(self, source, args):
		for arg, match in zip(args, self._args):
			# this stuff is stupidslow
			res = match.eval([arg], source)
			if not res or res[0] is not arg:
				return False
		return True


class GameAction(Action):
	def __init__(self, *args, **kwargs):
		self._args = args
		for k, v in zip(self.args, args):
			setattr(self, k, v)

	def get_args(self, source):
		return self._args

	def trigger(self, source):
		args = self.get_args(source)
		source.game.manager.action(self.type, source, *args)
		self.do(source, *args)
		source.game.manager.action_end(self.type, source, *args)
		source.game.process_deaths()


class Attack(GameAction):
	"""
	Make the source attack \a target
	"""
	args = ("source", "target")
	type = PowSubType.ATTACK

	def get_args(self, source):
		ret = super().get_args(source)
		self.source.attacking = True
		self.target.defending = True
		return ret

	def do(self, source, *args):
		source.game.proposed_attacker = self.source
		source.game.proposed_defender = self.target
		logging.info("%r attacks %r", self.source, self.target)
		self.broadcast(source, EventListener.ON, *args)
		source.game._attack()


class BeginTurn(GameAction):
	"""
	Make \a player begin the turn
	"""
	args = ("player", )
	type = None

	def do(self, source, *args):
		self.broadcast(source, EventListener.ON, self.player)
		source.game._begin_turn(self.player)


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

	def do(self, source, target):
		logging.info("Processing Death for %r", target)
		self.broadcast(source, EventListener.ON, target)
		if target.deathrattles:
			source.game.queue_actions(source, [Deathrattle(target)])


class EndTurn(GameAction):
	"""
	End the current turn
	"""
	args = ("player", )
	type = None

	def do(self, source, *args):
		self.broadcast(source, EventListener.ON, self.player)
		source.game._end_turn()


class Play(GameAction):
	"""
	Make the source player play \a card, on \a target or None.
	Choose play action from \a choose or None.
	"""
	args = ("card", "target", "choose")
	type = PowSubType.PLAY

	def _broadcast(self, entity, source, at, *args):
		# Prevent cards from triggering off their own play
		if entity is self.card:
			return
		return super()._broadcast(entity, source, at, *args)

	def get_args(self, source):
		return (source, ) + self._args

	def do(self, source, *args):
		card = self.card
		if card.has_target():
			assert self.target
		card.target = self.target

		if self.choose:
			# Choose One cards replace the action on the played card
			assert self.choose in card.data.choose_cards
			chosen = source.game.card(self.choose)
			chosen.controller = source
			logging.info("Choose One from %r: %r", card, chosen)
			if chosen.has_target():
				chosen.target = self.target
			card.chosen = chosen
		card.choose = self.choose

		source.game.no_aura_refresh = True
		source.game._play(card)
		# NOTE: A Play is not a summon! But it sure looks like one.
		# We need to fake a Summon broadcast.
		summon_action = Summon(source, card)
		self.broadcast(source, EventListener.ON, *args)
		summon_action.broadcast(source, EventListener.ON, source, card)
		source.game.no_aura_refresh = False
		card.action()
		summon_action.broadcast(source, EventListener.AFTER, source, card)
		self.broadcast(source, EventListener.AFTER, *args)
		source.combo = True
		source.cards_played_this_turn += 1
		if card.type == CardType.MINION:
			source.minions_played_this_turn += 1

		card.target = None
		card.choose = None


class TargetedAction(Action):
	args = ("targets", )
	selectors = ("targets", )

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.times = 1

	def __repr__(self):
		args = ["%s=%r" % (k, v) for k, v in zip(self.args[1:], self._args[1:])]
		return "<TargetedAction: %s(%s)>" % (self.__class__.__name__, ", ".join(args))

	def __mul__(self, value):
		self.times = value
		return self

	def eval(self, selector, source):
		if isinstance(selector, Entity):
			return [selector]
		else:
			return selector.eval(source.game, source)

	def get_args(self, source, target):
		return (target, )

	def evaluate_selectors(self, source):
		ret = []
		for k, v in zip(self.args, self._args):
			if k in self.selectors:
				if isinstance(v, Entity):
					ret.append([v])
				elif isinstance(v, Action):
					# eg. Unstable Portal: Buff(Give(...), ...)
					ret.append(v.trigger(source)[0])
				else:
					ret.append(v.eval(source.game, source))
			else:
				ret.append(v)
		return ret

	def trigger(self, source):
		ret = []
		times = self.times
		if isinstance(times, LazyNum):
			times = times.evaluate(source)
		for i in range(times):
			args = self.evaluate_selectors(source)
			targets = args[0]
			source.game.manager.action(self.type, source, targets, *self._args)
			logging.info("%r triggering %r targeting %r", source, self, targets)
			for target in targets:
				extra_args = self.get_args(source, target)
				ret.append(self.do(source, *extra_args))
			source.game.manager.action_end(self.type, source, targets, *self._args)
		return ret


class Buff(TargetedAction):
	"""
	Buff character targets with Enchantment \a id
	"""
	args = ("targets", "id")

	def do(self, source, target):
		source.buff(target, self.id)


class Bounce(TargetedAction):
	"""
	Bounce minion targets on the field back into the hand.
	"""
	def do(self, source, target):
		target.bounce()


class Damage(TargetedAction):
	"""
	Damage target by \a amount.
	"""
	args = ("targets", "amount")

	def do(self, source, target, *args):
		amount = target._hit(source, self.amount)
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
				logging.info("Triggering deathrattles for %r again", target)
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
		target.discard()


class Draw(TargetedAction):
	"""
	Make player targets draw \a count cards.
	"""
	def do(self, source, target):
		if not target.deck:
			target.fatigue()
			return []
		card = target.deck[-1]
		card.draw()

		return [card]


class ForceDraw(TargetedAction):
	"""
	Make player targets draw \a cards from their deck.
	"""
	args = ("targets", "cards")

	def do(self, source, target):
		cards = self.eval(self.cards, source)
		for card in cards:
			card.draw()


class ForcePlay(TargetedAction):
	"""
	Make player targets play \a cards from their hand (at no cost).
	"""
	args = ("targets", "cards")

	def do(self, source, target):
		cards = self.eval(self.cards, source)
		for card in cards:
			target.summon(card)


class FullHeal(TargetedAction):
	"""
	Fully heal character targets.
	"""
	def do(self, source, target):
		source.heal(target, target.health)


class GainArmor(TargetedAction):
	"""
	Make hero targets gain \a amount armor.
	"""
	args = ("targets", "amount")

	def do(self, source, target):
		target.armor += self.amount
		self.broadcast(source, EventListener.ON, target, self.amount)


class GainMana(TargetedAction):
	"""
	Give player targets \a Mana crystals.
	"""
	args = ("targets", "amount")

	def do(self, source, target):
		target.max_mana += self.amount


class Give(TargetedAction):
	"""
	Give player targets card \a id.
	"""
	args = ("targets", "card")

	def get_args(self, source, target):
		cards = _eval_card(source, self.card)
		return (target, cards)

	def do(self, source, target, cards):
		logging.debug("Giving %r to %s", cards, target)
		for card in cards:
			card.controller = target
			card.zone = Zone.HAND
		return cards


class Hit(TargetedAction):
	"""
	Hit character targets by \a amount.
	"""
	args = ("targets", "amount", "source")

	def get_args(self, source, target):
		if getattr(self, "source", None):
			source = self.source
		if isinstance(self.amount, LazyNum):
			amount = self.amount.evaluate(source)
		else:
			amount = self.amount
		return (target, amount, source)

	def do(self, source, target, amount, attack_source):
		if target.type == CardType.WEAPON:
			target.durability -= amount
		else:
			attack_source.hit(target, amount)


class Heal(TargetedAction):
	"""
	Heal character targets by \a amount.
	"""
	args = ("targets", "amount")

	def do(self, source, target):
		if source.controller.outgoing_healing_adjustment:
			# "healing as damage" (hack-ish)
			return source.hit(target, self.amount)

		amount = self.amount * (source.controller.healing_double + 1)
		amount = min(amount, target.damage)
		if amount:
			# Undamaged targets do not receive heals
			logging.info("%r heals %r for %i", source, target, amount)
			target.damage -= amount
			self.broadcast(source, EventListener.ON, target, amount)


class ManaThisTurn(TargetedAction):
	"""
	Give player targets \a amount Mana this turn.
	"""
	args = ("targets", "amount")

	def do(self, source, target):
		target.temp_mana += self.amount


class Mill(TargetedAction):
	"""
	Mill \a count cards from the top of the player targets' deck.
	"""
	args = ("targets", "count")

	def do(self, source, target):
		target.mill(self.count)


class Morph(TargetedAction):
	"""
	Morph minion target into \a minion id
	"""
	args = ("targets", "card")

	def get_args(self, source, target):
		card = _eval_card(source, self.card)
		if isinstance(card, list):
			assert len(card) == 1
			card = card[0]
		card.controller = target.controller
		return (target, card)

	def do(self, source, target, card):
		logging.info("Morphing %r into %r", self, card)
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
	args = ("targets", "amount")

	def do(self, source, target):
		target.used_mana -= self.amount


class Reveal(TargetedAction):
	"""
	Reveal secret targets.
	"""
	def do(self, source, target):
		logging.info("Revealing secret %r", target)
		self.broadcast(source, EventListener.ON, target)
		target.destroy()


class SetTag(TargetedAction):
	"""
	Sets various targets' tags to \a values.
	"""
	args = ("targets", "values")

	def do(self, source, target):
		for k, v in self.values.items():
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
	args = ("targets", "card")

	def _broadcast(self, entity, source, at, *args):
		# Prevent cards from triggering off their own summon
		if entity is args[1]:
			return
		return super()._broadcast(entity, source, at, *args)

	def get_args(self, source, target):
		cards = _eval_card(source, self.card)
		return (target, cards)

	def do(self, source, target, cards):
		logging.info("%s summons %r", target, cards)
		if not isinstance(cards, list):
			cards = [cards]

		for card in cards:
			if card.controller != target:
				card.controller = target
			if card.type == CardType.MINION and len(target.field) >= source.game.MAX_MINIONS_ON_FIELD:
				continue
			self.broadcast(source, EventListener.ON, target, card)
			card.zone = Zone.PLAY
			self.broadcast(source, EventListener.AFTER, target, card)


class Shuffle(TargetedAction):
	"""
	Shuffle card targets into player target's deck.
	"""
	args = ("targets", "card")

	def get_args(self, source, target):
		if isinstance(self.card, Selector):
			cards = self.card.eval(source.game, source)
		else:
			cards = _eval_card(source, self.card)
		return (target, cards)

	def do(self, source, target, cards):
		logging.info("%r shuffles into %s's deck", cards, target)
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
	args = ("targets", "other")

	def do(self, source, target):
		other = self.eval(self.other, source)
		if other:
			assert len(other) == 1
			other = other[0]
			orig = target.zone
			target.zone = other.zone
			other.zone = orig


class Steal(TargetedAction):
	"""
	Make the controller take control of targets.
	The controller is the controller of the source of the action.
	"""
	def do(self, source, target):
		logging.info("%s takes control of %r", self, target)
		zone = target.zone
		target.zone = Zone.SETASIDE
		target.controller = source.controller
		target.zone = zone
