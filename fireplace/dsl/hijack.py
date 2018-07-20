from contextlib import contextmanager

from .selector import Selector


class HijackedSelector(Selector):
	def __init__(self, *a, **kw):
		raise NotImplementedError

	def eval(self, entities, source):
		return self._hijack_.eval(entities, source)


def hijack(victim, replace):
	if victim.__class__ is not HijackedSelector:
		victim._truth_ = victim.__class__
	victim.__class__ = HijackedSelector
	victim._hijack_ = replace


def unhijack(victim):
	try:
		victim.__class__ = victim._truth_
	except AttributeError as e:
		raise ValueError("not a hijacked selector") from e


@contextmanager
def hijacked(victim, replace):
	if not isinstance(victim, Selector):
		raise TypeError("not a selector: %r" % (victim))
	prev = victim.__class__
	try:
		hijack(victim, replace)
		yield
	finally:
		victim.__class__ = prev
