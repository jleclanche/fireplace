"""
Targeting logic
"""

from enum import IntEnum
from .enums import CardType, PlayReq
from .utils import CardList


# Requirements-based targeting
def isValidTarget(self, target, requirements=None):
	if target.type == CardType.MINION:
		if target.dead:
			return False
		if target.stealthed and self.controller != target.controller:
			return False
		if target.immune and self.controller != target.controller:
			return False
		if self.type == CardType.SPELL and target.cantBeTargetedByAbilities:
			return False
		if self.type == CardType.HERO_POWER and target.cantBeTargetedByHeroPowers:
			return False

	if requirements is None:
		requirements = self.requirements

	for req, param in requirements.items():
		if req == PlayReq.REQ_MINION_TARGET:
			if target.type != CardType.MINION:
				return False
		elif req == PlayReq.REQ_FRIENDLY_TARGET:
			if target.controller != self.controller:
				return False
		elif req == PlayReq.REQ_ENEMY_TARGET:
			if target.controller == self.controller:
				return False
		elif req == PlayReq.REQ_DAMAGED_TARGET:
			if not target.damage:
				return False
		elif req == PlayReq.REQ_TARGET_MAX_ATTACK:
			if target.atk > param or 0:
				return False
		elif req == PlayReq.REQ_NONSELF_TARGET:
			if target is self:
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

		# fireplace reqs
		elif req == PlayReq.REQ_SPELL_TARGET:
			if target.type != CardType.SPELL:
				return False
		elif req == PlayReq.REQ_WEAPON_TARGET:
			if target.type != CardType.WEAPON:
				return False
		elif req == PlayReq.REQ_NO_MINIONS_PLAYED_THIS_TURN:
			if self.controller.minionsPlayedThisTurn:
				return False
		elif req == PlayReq.REQ_TARGET_HAS_BATTLECRY:
			if not target.hasBattlecry:
				return False
		elif req == PlayReq.REQ_SOURCE_IS_ENRAGED:
			if not self.enraged:
				return False
	return True


class Selector:
	"""
	A Forth-like program consisting of methods of Selector and members of
	IntEnum classes. The IntEnums must have appropriate test() methods
	    def test(self, entity)
	returning a boolean, true if entity matches the condition.
	"""
	class MergeFilter:
		"""
		Signals the start of a merge: the following commands define the filter
		to be passed after Merge
		"""
		pass

	class Merge:
		"""
		Ops between Merge and Unmerge are classes with merge() methods
		    def merge(self, selector, entities)
		that operate on the full collection specified by the ops between
		MergeFilter and Merge.
		"""
		pass

	class Unmerge:
		pass

	def __init__(self, *args):
		self.program = []
		first = True
		for arg in args:
			self.program.append(arg)
			if not first:
				self.program.append(Selector._or)
			first = False

	def __repr__(self):
		prog = []
		for op in self.program:
			name = ""
			if hasattr(op, "__name__"):
				name = op.__name__
			elif isinstance(op, IntEnum):
				name = op.name
			else:
				name = repr(op)
			prog.append(name.lstrip("_"))
		return "<{}: {}>".format(self.__class__.__name__, " ".join(prog))

	def __or__(self, other):
		result = Selector()
		result.program = self.program + other.program
		result.program.append(Selector._or)
		return result

	def __add__(self, other):
		result = Selector()
		result.program = self.program + other.program
		result.program.append(Selector._and)
		return result

	def __sub__(self, other):
		result = Selector()
		result.program = self.program + other.program
		result.program += [Selector._not, Selector._and]
		return result

	def eval(self, entities, source):
		self.opc = 0 # outer program counter
		result = []
		while self.opc < len(self.program):
			if self.program[self.opc] != Selector.MergeFilter:
				result += [e for e in entities if self.test(e, source)]
				self.opc = self.pc
				if self.opc >= len(self.program):
					break
			else:
				self.opc += 1
			# handle merge step:
			merge_input = CardList([e for e in entities if self.test(e, source)])
			self.opc = self.pc
			merge_output = CardList()
			while self.opc < len(self.program):
				op = self.program[self.opc]
				self.opc += 1
				if op == Selector.Unmerge:
					break
				merge_output += op.merge(self, merge_input)
			negated = False
			combined = False
			while self.opc < len(self.program):
				# special handling for operators on merged collections:
				op = self.program[self.opc]
				if op == Selector._or:
					result += [e for e in merge_output]
					combined = True
				elif op == Selector._and:
					result = [e for e in result if (e in merge_output) != negated]
					combined = True
				elif op == Selector._not:
					negated = not negated
				else:
					break
				self.opc += 1
			if not combined:
				# assume or
				result += merge_output
		return result

	def test(self, entity, source):
		stack = []
		self.pc = self.opc # program counter
		while self.pc < len(self.program):
			op = self.program[self.pc]
			self.pc += 1
			if op == Selector.Merge or op == Selector.MergeFilter:
				break
			if callable(op):
				op(self, stack)
			else:
				val = type(op).test(op, entity, source)
				stack.append(val)
		return stack[-1]

	# boolean ops:
	def _and(self, stack):
		a = stack.pop()
		b = stack.pop()
		stack.append(a and b)

	def _or(self, stack):
		a = stack.pop()
		b = stack.pop()
		stack.append(a or b)

	def _not(self, stack):
		stack.append(not stack.pop())


class SelfSelector(Selector):
	"""
	Selects the source.
	"""
	class IsSelf:
		def test(self, entity, source):
			return entity is source

	def __init__(self):
		self.program = [self.IsSelf()]

	def eval(self, entities, source):
		return [source]

	def test(self, entity, source):
		return entity is source

SELF = SelfSelector()
