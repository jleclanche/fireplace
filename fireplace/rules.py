"""
Base game rules (events, etc)
"""
from .cards.utils import *


HEAVILY_ARMORED = [Predamage(SELF, lambda i: i > 1).on(Predamage(SELF, 1))]


class WeaponRules:
	base_events = [
		Attack(FRIENDLY_HERO).after(Hit(SELF, 1))
	]
