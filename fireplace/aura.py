from .managers import CardManager
from .utils import CardList, fireplace_logger as logger


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
		logger.info("Summoning Aura %r", self)
		self.source.auras.append(self)
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
		logger.info("Removing %r affecting %r", self, self._buffed)
		self.source.game.auras.remove(self)
		for buff in self._buffs[:]:
			buff.destroy()
		del self._buffs
		del self._buffed
		self.source.auras.remove(self)


class AuraBuff:
	def __init__(self, source, entity):
		self.source = source
		self.entity = entity
		self.tags = CardManager(self)

	def __repr__(self):
		return "<AuraBuff on %r from %r>" % (self.entity, self.source)

	def update_tags(self, tags):
		self.tags.update(tags)
		self.tick = self.source.game.tick

	def destroy(self):
		self.entity.slots.remove(self)
		self.source.game.active_aura_buffs.remove(self)

	def _getattr(self, attr, i):
		value = getattr(self, attr, 0)
		if callable(value):
			return value(self.entity, i)
		return i + value


class Refresh:
	"""
	Refresh a buff or a set of tags on an entity
	"""
	def __init__(self, selector, tags):
		self.selector = selector
		self.tags = tags

	def trigger(self, source):
		entities = self.selector.eval(source.game, source)
		for entity in entities:
			tags = {}
			for tag, value in self.tags.items():
				if not isinstance(value, int) and not callable(value):
					value = value.evaluate(source)
				tags[tag] = value

			entity.refresh_buff(source, tags)


class TargetableByAuras:
	def refresh_buff(self, source, tags):
		for slot in self.slots[:]:
			if isinstance(slot, AuraBuff) and slot.source is source:
				slot.update_tags(tags)
				# Move the buff position at the end again
				self.slots.remove(slot)
				self.slots.append(slot)
				break
		else:
			buff = AuraBuff(source, self)
			buff.update_tags(tags)
			self.slots.append(buff)
			source.game.active_aura_buffs.append(buff)
