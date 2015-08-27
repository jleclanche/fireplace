import logging
from .utils import CardList


class Aura:
	"""
	A virtual Card class which is only for the source of the Enchantment buff on
	targets affected by an aura. It is only internal.
	"""

	def __init__(self, action, source):
		self.action = action
		self.selector = self.action._args[0]
		self.id = self.action._args[1]
		self.source = source
		self.to_be_destroyed = False
		self._buffed = CardList()
		self._buffs = CardList()
		# THIS IS A HACK
		# DON'T SHOOT, IT'S TEMPORARY
		self.on_enrage = self.id == "CS2_221e"

	def __repr__(self):
		return "<Aura (%r)>" % (self.id)

	@property
	def targets(self):
		if self.on_enrage and not self.source.enraged:
			return []
		return CardList(self.selector.eval(self.source.game, self.source))

	def summon(self):
		logging.info("Summoning Aura %r", self)
		self.source.game.auras.append(self)
		self.source.game.refresh_auras()

	def _buff(self, target):
		buff = self.source.buff(target, self.id)
		buff.aura_source = self
		self._buffs.append(buff)
		self._buffed.append(target)

	def _entity_buff(self, target):
		"Returns the buff created by this aura on \a target"
		for buff in target.buffs:
			if buff.aura_source is self:
				return buff

	def update(self):
		if self.to_be_destroyed:
			return self.destroy()

		targets = self.targets
		for target in targets:
			if not self._entity_buff(target):
				self._buff(target)
		# Make sure to copy the list as it can change during iteration
		for target in self._buffed[:]:
			# Remove auras no longer valid
			if target not in targets:
				buff = self._entity_buff(target)
				if buff:
					buff.destroy()
				self._buffed.remove(target)

	def destroy(self):
		logging.info("Removing %r affecting %r", self, self._buffed)
		self.source.game.auras.remove(self)
		for buff in self._buffs[:]:
			buff.destroy()
		del self._buffs
		del self._buffed
		self.source._auras.remove(self)
