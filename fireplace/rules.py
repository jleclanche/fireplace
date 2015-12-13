"""
Base game rules (events, etc)
"""
from .actions import Attack, Damage, Destroy, Hit
from .dsl.selector import FRIENDLY_HERO, MINION, SELF


POISONOUS = Damage(MINION, None, SELF).on(Destroy(Damage.TARGETS))


class WeaponRules:
	base_events = [
		Attack(FRIENDLY_HERO).after(Hit(SELF, 1))
	]
