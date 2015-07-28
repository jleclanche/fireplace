"""
Base game rules (events, etc)
"""
from .actions import Attack, Damage, Destroy, Hit
from .dsl.selector import FRIENDLY_HERO, MINION, SELF


Poisonous = [
	Damage(MINION, None, SELF).on(Destroy(Damage.Args.TARGETS))
]


class WeaponRules:
	base_events = [
		Attack(FRIENDLY_HERO).on(Hit(SELF, 1))
	]
