"""
Targeting logic
"""

from .enums import PlayReq


##
# Constants
# Only for use in getTargets()

TARGET_NONE = 0x0
TARGET_FRIENDLY = 0x1
TARGET_ENEMY = 0x2
TARGET_ANY = TARGET_FRIENDLY | TARGET_ENEMY
TARGET_MINION = 0x4
TARGET_HERO = 0x8
TARGET_CHARACTER = TARGET_MINION | TARGET_HERO
TARGET_MULTIPLE = 0x10

TARGET_FRIENDLY_HERO = TARGET_FRIENDLY | TARGET_HERO
TARGET_FRIENDLY_MINION = TARGET_FRIENDLY | TARGET_MINION
TARGET_FRIENDLY_MINIONS = TARGET_FRIENDLY_MINION | TARGET_MULTIPLE
TARGET_FRIENDLY_CHARACTERS = TARGET_FRIENDLY_HERO | TARGET_FRIENDLY_MINIONS

TARGET_ENEMY_HERO = TARGET_ENEMY | TARGET_HERO
TARGET_ENEMY_MINION = TARGET_ENEMY | TARGET_MINION
TARGET_ENEMY_MINIONS = TARGET_ENEMY_MINION | TARGET_MULTIPLE
TARGET_ENEMY_CHARACTERS = TARGET_ENEMY_HERO | TARGET_ENEMY_MINIONS

TARGET_ANY_MINION = TARGET_FRIENDLY_MINION | TARGET_ENEMY_MINION
TARGET_ANY_HERO = TARGET_FRIENDLY_HERO | TARGET_ENEMY_HERO
TARGET_ANY_CHARACTER = TARGET_ANY_MINION | TARGET_ANY_HERO
TARGET_ALL_MINIONS = TARGET_FRIENDLY_MINIONS | TARGET_ENEMY_MINIONS
TARGET_ALL_CHARACTERS = TARGET_ALL_MINIONS | TARGET_ANY_HERO


# Requirements-based targeting
def isValidTarget(self, target):
	if target.stealth and self.owner != target.owner:
		return False
	for req in self.data.requirements:
		if req == PlayReq.REQ_MINION_TARGET:
			if target.type != CardType.MINION:
				return False
		elif req == PlayReq.REQ_FRIENDLY_TARGET:
			if target.owner != self.owner:
				return False
		elif req == PlayReq.REQ_ENEMY_TARGET:
			if target.owner == self.owner:
				return False
		elif req == PlayReq.REQ_DAMAGED_TARGET:
			if not target.isDamaged():
				return False
		elif req == PlayReq.REQ_TARGET_MAX_ATTACK:
			if target.atk > self.data.targetMaxAttack:
				return False
		elif req == PlayReq.REQ_NONSELF_TARGET:
			if target is self:
				return False
		elif req == PlayReq.REQ_TARGET_WITH_RACE:
			if target.race != self.data.targetRace:
				return False
		elif req == PlayReq.REQ_HERO_TARGET:
			if target.type != CardType.HERO:
				return False
		elif req == PlayReq.REQ_TARGET_MIN_ATTACK:
			if target.atk < self.data.targetMinAttack:
				return False
		elif req == PlayReq.REQ_MUST_TARGET_TAUNTER:
			if not target.taunt:
				return False
		elif req == PlayReq.REQ_UNDAMAGED_TARGET:
			if target.isDamaged():
				return False
	return True
