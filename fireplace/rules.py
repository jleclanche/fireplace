"""
Base game rules (events, etc)
"""
from .cards.utils import *


FORGETFUL = Attack(SELF).on(COINFLIP & Retarget(SELF, RANDOM(ALL_CHARACTERS - Attack.DEFENDER - CONTROLLED_BY(SELF))))
POISONOUS = Damage(MINION, None, SELF).on(Destroy(Damage.TARGET))


class WeaponRules:
	base_events = [
		Attack(FRIENDLY_HERO).after(Hit(SELF, 1))
	]
