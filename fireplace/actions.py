import logging
import random
from .enums import CardType, PowSubType, Step
from .entity import Entity


class Action: # Lawsuit
	args = ()
	type = PowSubType.TRIGGER

	def __init__(self, *args, **kwargs):
		self.times = 1
		self._args = args
		for k, v in zip(self.args, args):
			setattr(self, k, v)

	def __repr__(self):
		args = ["%s=%r" % (k, v) for k, v in zip(self.args, self._args)]
		return "<Action: %s(%s)>" % (self.__class__.__name__, ", ".join(args))

	def __mul__(self, value):
		self.times *= value
		return self

	def eval(self, selector, source, game):
		if isinstance(selector, Entity):
			return [selector]
		else:
			return selector.eval(game, source)


class GameAction(Action):
	def __init__(self, *args, **kwargs):
		self._args = args
		for k, v in zip(self.args, args):
			setattr(self, k, v)

	def trigger(self, source, game):
		game.manager.action(self.type, source, *self._args)
		self.do(source, game)
		game.manager.action_end(self.type, source, *self._args)
		game._processDeaths()
		game.refreshAuras()


class Attack(GameAction):
	"""
	Make the source attack \a target
	"""
	args = ("target", )
	type = PowSubType.ATTACK

	def do(self, source, game):
		game._attack(source, self.target)


class BeginTurn(GameAction):
	"""
	Make \a player begin the turn
	"""
	args = ("player", )
	type = None

	def do(self, source, game):
		game._beginTurn(self.player)


class Deaths(GameAction):
	"""
	Process all deaths in the PLAY Zone.
	"""

	def do(self, source, game):
		game._processDeaths()


class EndTurn(GameAction):
	"""
	End the current turn
	"""
	type = None

	def do(self, source, game):
		game._endTurn()


class Play(GameAction):
	"""
	Make the source player play \a card, on \a target or None.
	Choose play action from \a choose or None.
	"""
	args = ("card", "target", "choose")
	type = PowSubType.PLAY

	def do(self, source, game):
		source._play(self.card, self.target, self.choose)


class TargetedAction(Action):
	args = ("targets", )

	def __repr__(self):
		args = ["%s=%r" % (k, v) for k, v in zip(self.args[1:], self._args[1:])]
		return "<TargetedAction: %s(%s)>" % (self.__class__.__name__, ", ".join(args))

	def trigger(self, source, game):
		targets = self.eval(self.targets, source, game)
		game.manager.action(self.type, source, targets, *self._args)
		for i in range(self.times):
			logging.info("%r triggering %r targeting %r", source, self, targets)
			for target in targets:
				self.do(source, game, target)
		game.manager.action_end(self.type, source, targets, *self._args)
		game._processDeaths()
		game.refreshAuras()


class Buff(TargetedAction):
	"""
	Buff character targets with Enchantment \a id
	"""
	args = ("targets", "id")

	def do(self, source, game, target):
		source.buff(target, self.id)


class Bounce(TargetedAction):
	"""
	Bounce minion targets on the field back into the hand.
	"""
	def do(self, source, game, target):
		target.bounce()


class Destroy(TargetedAction):
	"""
	Destroy character targets.
	"""
	def do(self, source, game, target):
		target._destroy()


class Discard(TargetedAction):
	"""
	Discard card targets in a player's hand
	"""
	def do(self, source, game, target):
		target.discard()


class Draw(TargetedAction):
	"""
	Make player targets draw \a count cards.
	"""
	args = ("targets", "count")

	def do(self, source, game, target):
		target.draw(self.count)


class ForceDraw(TargetedAction):
	"""
	Make player targets draw \a cards from their deck.
	"""
	args = ("targets", "cards")

	def do(self, source, game, target):
		cards = self.eval(self.cards, source, game)
		for card in cards:
			target.draw(card)


class ForcePlay(TargetedAction):
	"""
	Make player targets play \a cards from their hand (at no cost).
	"""
	args = ("targets", "cards")

	def do(self, source, game, target):
		cards = self.eval(self.cards, source, game)
		for card in cards:
			target.summon(card)


class FullHeal(TargetedAction):
	"""
	Fully heal character targets.
	"""
	def do(self, source, game, target):
		source.heal(target, target.health)

class GainArmor(TargetedAction):
	"""
	Make hero targets gain \a amount armor.
	"""
	args = ("targets", "amount")

	def do(self, source, game, target):
		target.armor += self.amount


class GainMana(TargetedAction):
	"""
	Give player targets \a Mana crystals.
	"""
	args = ("targets", "amount")

	def do(self, source, game, target):
		target.maxMana += self.amount


class Give(TargetedAction):
	"""
	Give player targets card \a id.
	"""
	args = ("targets", "id")

	def do(self, source, game, target):
		target.give(self.id)


class GiveSparePart(TargetedAction):
	"""
	Give player targets a random Spare Part.
	This currently assumes the source has a Spare Part entourage.
	"""
	def do(self, source, game, target):
		target.give(random.choice(source.data.entourage))


class Hit(TargetedAction):
	"""
	Hit character targets by \a amount.
	"""
	args = ("targets", "amount")

	def do(self, source, game, target):
		if target.type == CardType.WEAPON:
			target.durability -= self.amount
		else:
			source.hit(target, self.amount)


class Heal(TargetedAction):
	"""
	Heal character targets by \a amount.
	"""
	args = ("targets", "amount")

	def do(self, source, game, target):
		source.heal(target, self.amount)


class ManaThisTurn(TargetedAction):
	"""
	Give player targets \a amount Mana this turn.
	"""
	args = ("targets", "amount")

	def do(self, source, game, target):
		target.tempMana += self.amount


class Mill(TargetedAction):
	"""
	Mill \a count cards from the top of the player targets' deck.
	"""
	args = ("targets", "count")

	def do(self, source, game, target):
		target.mill(self.count)


class Morph(TargetedAction):
	"""
	Morph minion target into \a minion id
	"""
	args = ("targets", "id")

	def do(self, source, game, target):
		target.morph(self.id)


class Freeze(TargetedAction):
	"""
	Freeze character targets.
	"""
	def do(self, source, game, target):
		target.frozen = True


class FillMana(TargetedAction):
	"""
	Refill \a amount mana crystals from player targets.
	"""
	args = ("targets", "amount")

	def do(self, source, game, target):
		target.usedMana -= self.amount


class Reveal(TargetedAction):
	"""
	Reveal secret targets.
	"""
	def do(self, source, game, target):
		target.reveal()


class SetTag(TargetedAction):
	"""
	Sets various targets' tags to \a values.
	"""
	args = ("targets", "values")

	def do(self, source, game, target):
		for k, v in self.values.items():
			if target.tags[k] != v:
				target.tags[k] = v


class Silence(TargetedAction):
	"""
	Silence minion targets.
	"""
	def do(self, source, game, target):
		target.silence()


class Summon(TargetedAction):
	"""
	Make player targets summon \a id onto their field.
	This works for equipping weapons as well as summoning minions.
	"""
	args = ("targets", "card")

	def do(self, source, game, target):
		card = self.card
		if isinstance(card, str):
			card = game.card(self.card)
			card.controller = target
		logging.info("%s summons %r", target, card)
		card.summon()


class Swap(TargetedAction):
	"""
	Swap minion target with \a other.
	Behaviour is undefined when swapping more than two minions.
	"""
	args = ("targets", "other")

	def do(self, source, game, target):
		other = self.eval(self.other, source, game)
		if other:
			assert len(other) == 1
			other = other[0]
			orig = target.zone
			target.zone = other.zone
			other.zone = orig


class TakeControl(TargetedAction):
	"""
	Make the controller take control of targets.
	The controller is the controller of the source of the action.
	"""
	def do(self, source, game, target):
		source.controller.takeControl(target)
