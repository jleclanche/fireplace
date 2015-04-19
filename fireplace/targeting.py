"""
Targeting logic
"""

from .enums import CardType, PlayReq


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
	class BreakLabel:
		# no-op:
		def __init__(self, selector, stack):
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
			# breaks are just optimization -- filter them
			if "break" not in name.lower():
				prog.append(name.lstrip("_"))
		return "<{}: {}>".format(self.__class__.__name__, " ".join(prog))

	def __or__(self, other):
		result = Selector()
		result.program = self.program + [Selector._break_true] + other.program
		result.program += [Selector._or, Selector.BreakLabel]
		return result

	def __add__(self, other):
		result = Selector()
		result.program = self.program + [Selector._break_false] + other.program
		result.program += [Selector._and, Selector.BreakLabel]
		return result

	def __sub__(self, other):
		result = Selector()
		result.program = self.program + [Selector._break_false] + other.program
		result.program += [Selector._not, Selector._and, Selector.BreakLabel]
		return result

	def eval(self, entities, source):
		return [e for e in entities if self.test(e, source)]

	def test(self, entity, source):
		stack = []
		self.pc = 0
		while self.pc < len(self.program):
			op = self.program[self.pc]
			self.pc += 1
			if callable(op):
				op(self, stack)
			else:
				val = type(op).test(op, entity, source)
				stack.append(val)
		return stack[-1]

	# if stack has false, skips to the appropriate BreakLabel
	def _break_false(self, stack):
		if stack[-1] == False:
			self._break(stack)

	# same as _break_false, but if stack has true
	def _break_true(self, stack):
		if stack[-1] == True:
			self._break(stack)

	def _break(self, stack):
		depth = 1
		while self.pc < len(self.program):
			op = self.program[self.pc]
			if op == Selector._break_true or op == Selector._break_false:
				depth += 1
			if op == self.BreakLabel:
				depth -= 1
			self.pc += 1
			if depth == 0:
				break

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
