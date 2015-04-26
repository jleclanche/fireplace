import logging
import random
from .enums import CardType, PowSubType
from .entity import Entity


class Action: # Lawsuit
	args = ()

	def __init__(self, target, *args, **kwargs):
		self.target = target
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

	def trigger(self, source, game):
		targets = self.eval(self.target, source, game)
		for i in range(self.times):
			logging.info("%r triggering %r targeting %r", source, self, targets)
			for target in targets:
				self.do(source, target, game)
		game.action(PowSubType.TRIGGER, source)


class GameAction(Action):
	def __init__(self, *args, **kwargs):
		self._args = args
		for k, v in zip(self.args, args):
			setattr(self, k, v)

	def trigger(self, source, game):
		return self.do(source, game)


class Buff(Action):
	"""
	Buff character targets with Enchantment \a id
	"""
	args = ("id", )
	def do(self, source, target, game):
		source.buff(target, self.id)

class Bounce(Action):
	"""
	Bounce minion targets on the field back into the hand.
	"""
	def do(self, source, target, game):
		target.bounce()

class Destroy(Action):
	"""
	Destroy character targets.
	"""
	def do(self, source, target, game):
		target._destroy()

class Discard(Action):
	"""
	Discard card targets in a player's hand
	"""
	def do(self, source, target, game):
		target.discard()

class Draw(Action):
	"""
	Make player targets draw \a count cards.
	"""
	args = ("count", )
	def do(self, source, target, game):
		target.draw(self.count)

class ForceDraw(Action):
	"""
	Make player targets draw \a cards from their deck.
	"""
	args = ("cards", )
	def do(self, source, target, game):
		cards = self.eval(self.cards, source, game)
		for card in cards:
			target.draw(card)


class ForcePlay(Action):
	"""
	Make player targets play \a cards from their hand (at no cost).
	"""
	args = ("cards", )
	def do(self, source, target, game):
		cards = self.eval(self.cards, source, game)
		for card in cards:
			target.summon(card)


class FullHeal(Action):
	"""
	Fully heal character targets.
	"""
	def do(self, source, target, game):
		source.heal(target, target.health)

class GainArmor(Action):
	"""
	Make hero targets gain \a amount armor.
	"""
	args = ("amount", )
	def do(self, source, target, game):
		target.armor += self.amount


class GainMana(Action):
	"""
	Give player targets \a Mana crystals.
	"""
	args = ("amount", )
	def do(self, source, target, game):
		target.maxMana += self.amount


class Give(Action):
	"""
	Give player targets card \a id.
	"""
	args = ("id", )
	def do(self, source, target, game):
		target.give(self.id)


class GiveSparePart(Action):
	"""
	Give player targets a random Spare Part.
	This currently assumes the source has a Spare Part entourage.
	"""
	def do(self, source, target, game):
		target.give(random.choice(source.data.entourage))


class Hit(Action):
	"""
	Hit character targets by \a amount.
	"""
	args = ("amount", )
	def do(self, source, target, game):
		if target.type == CardType.WEAPON:
			target.durability -= self.amount
		else:
			source.hit(target, self.amount)

class Heal(Action):
	"""
	Heal character targets by \a amount.
	"""
	args = ("amount", )
	def do(self, source, target, game):
		source.heal(target, self.amount)

class ManaThisTurn(Action):
	"""
	Give player targets \a amount Mana this turn.
	"""
	args = ("amount", )
	def do(self, source, target, game):
		target.tempMana += self.amount

class Mill(Action):
	"""
	Mill \a count cards from the top of the player targets' deck.
	"""
	args = ("count", )
	def do(self, source, target, game):
		target.mill(self.count)

class Morph(Action):
	"""
	Morph minion target into \a minion id
	"""
	args = ("id", )
	def do(self, source, target, game):
		target.morph(self.id)

class Freeze(Action):
	"""
	Freeze character targets.
	"""
	def do(self, source, target, game):
		target.frozen = True

class FillMana(Action):
	"""
	Refill \a amount mana crystals from player targets.
	"""
	args = ("amount", )
	def do(self, source, target, game):
		target.usedMana -= self.amount


class Reveal(Action):
	"""
	Reveal secret targets.
	"""
	def do(self, source, target, game):
		target.reveal()


class SetTag(Action):
	"""
	Sets various targets' tags to \a values.
	"""
	args = ("values", )
	def do(self, source, target, game):
		for k, v in self.values.items():
			if target.tags[k] != v:
				target.tags[k] = v


class Silence(Action):
	"""
	Silence minion targets.
	"""
	def do(self, source, target, game):
		target.silence()

class Summon(Action):
	"""
	Make player targets summon \a id onto their field.
	This works for equipping weapons as well as summoning minions.
	"""
	args = ("id", )
	def do(self, source, target, game):
		target.summon(self.id)

class Swap(Action):
	"""
	Swap minion target with \a other.
	Behaviour is undefined when swapping more than two minions.
	"""
	args = ("other", )
	def do(self, source, target, game):
		other = self.eval(self.other, source, game)
		if other:
			assert len(other) == 1
			other = other[0]
			orig = target.zone
			target.zone = other.zone
			other.zone = orig

class TakeControl(Action):
	"""
	Make the controller take control of targets.
	The controller is the controller of the source of the action.
	"""
	def do(self, source, target, game):
		source.controller.takeControl(target)
