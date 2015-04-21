from ..utils import *


##
# Minions

# Quartermaster
class GVG_060:
	def action(self):
		for recruit in self.controller.field.filter(id="CS2_101t"):
			yield [Buff(recruit, "GVG_060e")]


# Bolvar Fordragon
class GVG_063:
	@hand
	def OWN_MINION_DESTROY(self, minion):
		return [Buff(SELF, "GVG_063a")]


##
# Spells

# Seal of Light
class GVG_057:
	action = [Heal(FRIENDLY_HERO, 4), Buff(FRIENDLY_HERO, "GVG_057a")]


##
# Weapons

# Coghammer
class GVG_059:
	action = [SetTag(RANDOM_FRIENDLY_MINION, {GameTag.TAUNT: True, GameTag.DIVINE_SHIELD: True})]
