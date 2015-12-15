"""
Base game rules (events, etc)
"""
from .cards.utils import *


FORGETFUL = Attack(SELF).on(
	COINFLIP & Retarget(SELF, RANDOM(ENEMY_CHARACTERS - Attack.DEFENDER))
)
POISONOUS = Damage(MINION, None, SELF).on(Destroy(Damage.TARGETS))


class WeaponRules:
	base_events = [
		Attack(FRIENDLY_HERO).after(Hit(SELF, 1))
	]
