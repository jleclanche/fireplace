"""
Base game rules (events, etc)
"""
from .actions import Attack, Hit
from .dsl.selector import FRIENDLY_HERO, SELF


class WeaponRules:
	base_events = [
		Attack(FRIENDLY_HERO).on(Hit(SELF, 1))
	]
