import ast
import uuid
import sys
from hearthstone.enums import CardType
from . import logging


class CalculatedProperty:
	"""
	A data descriptor intended for card attributes that are influenced
	by buffs.

	If the `eager` keyword argument is true, the value of the property is
	computed each time it is accessed. Otherwise, it is computed every time it
	is changed, or attached entities change their copy.
	"""
	__slots__ = ("_name", "_default", "_eager", "_xname", "_basename")

	def __init__(self, default, *, eager=False):
		self._name = None
		self._default = default
		self._eager = eager

	def _setup(self, cls, name):
		self._name = sys.intern(name)
		self._xname = sys.intern("_" + name)
		self._basename = sys.intern("!" + name)

		setattr(cls, self._xname, self._default)

		class _Calculated(type(self)):
			__slots__ = ()

			if self._eager:
				def __get__(self, inst, owner):
					return self._calculate(inst)
			else:
				"""
				def __get__(self, inst, owner):
					return inst.{self._xname}
				def __set__(self, inst, v):
					inst.{self._basename} = v
					self.recalculate(inst)
				"""
				exec(compile(ast.fix_missing_locations(ast.Module([
					ast.FunctionDef("__get__", ast.arguments([ast.arg("self", None), ast.arg("inst", None), ast.arg("owner", None)], None, [], [], None, []),
					                [ast.Return(ast.Attribute(ast.Name("inst", ast.Load()), self._xname, ast.Load()))], [], None),
					ast.FunctionDef("__set__", ast.arguments([ast.arg("self", None), ast.arg("inst", None), ast.arg("v", None)], None, [], [], None, []),
					                [ast.Assign([ast.Attribute(ast.Name("inst", ast.Load()), self._basename, ast.Store())], ast.Name("v", ast.Load())),
					                 ast.Expr(ast.Call(ast.Attribute(ast.Name("self", ast.Load()), "recalculate", ast.Load()), [ast.Name("inst", ast.Load())], []))], [], None)])),
					"<generated code for %r>" % (self), "exec"))

		self.__class__ = _Calculated

	def __get__(self, inst, owner):
		# XXX for documentation only
		assert False, "you shouldn't call this"
		if inst is None:
			return self
		if self._eager:
			return self._calculate(inst)
		return getattr(inst, self._xname)

	def __set__(self, inst, v):
		setattr(inst, self._basename, v)
		self.recalculate(inst)

	def _calculate(self, owner):
		raise NotImplementedError

	def recalculate(self, owner):
		if not self._eager:
			setattr(owner, self._xname, self._calculate(owner))
		if owner.is_enchantment and getattr(owner, "owner", False):
			self.recalculate(owner.owner)

	def __repr__(self):
		return "<CalculatedProperty %s>" % (self._name)


class BooleanProperty(CalculatedProperty):
	__slots__ = ()

	def __init__(self, **kw):
		super().__init__(False, **kw)

	def _calculate(self, owner):
		return (
			getattr(owner, self._basename, False) or
			any(getattr(buff, self._name, False) for buff in owner.buffs) or
			any(getattr(slot, self._name, False) for slot in owner.slots) or
			getattr(owner.data.scripts, self._name, lambda s, x: x)(self, False)
		)


class SlotProperty(CalculatedProperty):
	__slots__ = ('_f',)

	def __init__(self, f=any, **kw):
		self._f = f
		super().__init__(False, **kw)

	def _calculate(self, owner):
		return self._f(getattr(slot, self._name, False) for slot in owner.slots)


class IntProperty(CalculatedProperty):
	__slots__ = ()

	def __init__(self, **kw):
		super().__init__(0, **kw)

	def _calculate(self, owner):
		return max(owner._getattr(self._name, 0), 0)


class EntityMeta(type):
	def __init__(cls, name, bases, namespace):
		for k, v in list(cls.__dict__.items()):
			if not isinstance(v, CalculatedProperty):
				continue
			v._setup(cls, k)

		properties = {}

		for t in reversed(cls.mro()):
			properties.update({ k: v for k, v in t.__dict__.items() if isinstance(v, CalculatedProperty) })

		cls.properties = properties


class BaseEntity(metaclass=EntityMeta):
	base_events = []
	logger = logging.log
	ignore_scripts = False
	type = CardType.INVALID
	is_enchantment = False

	def __init__(self):
		self.manager = self.Manager(self)
		self.play_counter = 0
		self.tags = self.manager
		self.uuid = uuid.uuid4()

		if self.data:
			self._events = self.data.scripts.events[:]
		else:
			self._events = []

	def __int__(self):
		return self.entity_id

	@property
	def is_card(self):
		"""
		True if the Entity is a real card (as opposed to a Player, Game, ...)
		"""
		return self.type > CardType.PLAYER

	@property
	def events(self):
		return self.base_events + self._events

	@property
	def update_scripts(self):
		if self.data and not self.ignore_scripts:
			yield from self.data.scripts.update

	def log(self, message, *args):
		self.logger.info(message, *args)

	def get_actions(self, name):
		actions = getattr(self.data.scripts, name)
		if callable(actions):
			actions = actions(self)
		return actions

	def trigger_event(self, source, event, args):
		"""
		Trigger an event on the Entity
		* \a source: The source of the event
		* \a event: The event being triggered
		* \a args: A list of arguments to pass to the callback
		"""
		actions = []
		for action in event.actions:
			if callable(action):
				ac = action(self, *args)
				if not ac:
					# Handle falsy returns
					continue
				if not hasattr(ac, "__iter__"):
					actions.append(ac)
				else:
					actions += action(self, *args)
			else:
				actions.append(action)
		ret = source.game.trigger(self, actions, args)
		if event.once:
			self._events.remove(event)

		return ret

	def get_damage(self, amount: int, target) -> int:
		"""
		Override to modify the damage dealt to a target from the given amount.
		"""
		if target.immune:
			self.log("%r is immune to %s for %i damage", target, self, amount)
			return 0
		return amount


class BuffableEntity(BaseEntity):
	def __init__(self):
		super().__init__()
		self.buffs = []
		self.slots = []

	def _getattr(self, attr, i):
		i += getattr(self, "!" + attr, 0)
		for buff in self.buffs:
			i = buff._getattr(attr, i)
		for slot in self.slots:
			i = slot._getattr(attr, i)
		if self.ignore_scripts:
			return i
		return getattr(self.data.scripts, attr, lambda s, x: x)(self, i)

	def calculate_buffs(self):
		for k, v in self.properties.items():
			v.recalculate(self)

	def clear_buffs(self):
		if self.buffs:
			self.log("Clearing buffs from %r", self)
			for buff in self.buffs[:]:
				buff.remove()
			self.calculate_buffs()


class Entity(BuffableEntity):
	pass
