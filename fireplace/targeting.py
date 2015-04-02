"""
Targeting logic
"""

from .enums import CardType, PlayReq


##
# Constants
# Only for use in getTargets()

TARGET_NONE = 0x0
TARGET_FRIENDLY = 0x1
TARGET_ENEMY = 0x2
TARGET_ANY = TARGET_FRIENDLY | TARGET_ENEMY
TARGET_MINION = 0x4
TARGET_HERO = 0x8
TARGET_WEAPON = 0x10
TARGET_CHARACTER = TARGET_MINION | TARGET_HERO
TARGET_MULTIPLE = 0x20
TARGET_HAND = 0x40

TARGET_FRIENDLY_HERO = TARGET_FRIENDLY | TARGET_HERO
TARGET_FRIENDLY_MINION = TARGET_FRIENDLY | TARGET_MINION
TARGET_FRIENDLY_WEAPON = TARGET_FRIENDLY | TARGET_WEAPON
TARGET_FRIENDLY_MINIONS = TARGET_FRIENDLY_MINION | TARGET_MULTIPLE
TARGET_FRIENDLY_CHARACTERS = TARGET_FRIENDLY_HERO | TARGET_FRIENDLY_MINIONS
TARGET_FRIENDLY_HAND = TARGET_FRIENDLY | TARGET_HAND

TARGET_ENEMY_HERO = TARGET_ENEMY | TARGET_HERO
TARGET_ENEMY_MINION = TARGET_ENEMY | TARGET_MINION
TARGET_ENEMY_WEAPON = TARGET_ENEMY | TARGET_WEAPON
TARGET_ENEMY_MINIONS = TARGET_ENEMY_MINION | TARGET_MULTIPLE
TARGET_ENEMY_CHARACTERS = TARGET_ENEMY_HERO | TARGET_ENEMY_MINIONS
TARGET_ENEMY_HAND = TARGET_ENEMY | TARGET_HAND

TARGET_ANY_MINION = TARGET_FRIENDLY_MINION | TARGET_ENEMY_MINION
TARGET_ANY_HERO = TARGET_FRIENDLY_HERO | TARGET_ENEMY_HERO
TARGET_ANY_WEAPON = TARGET_FRIENDLY_WEAPON | TARGET_ENEMY_WEAPON
TARGET_ANY_CHARACTER = TARGET_ANY_MINION | TARGET_ANY_HERO
TARGET_ANY_HAND = TARGET_FRIENDLY_HAND | TARGET_ENEMY_HAND
TARGET_ALL_MINIONS = TARGET_FRIENDLY_MINIONS | TARGET_ENEMY_MINIONS
TARGET_ALL_CHARACTERS = TARGET_ALL_MINIONS | TARGET_ANY_HERO


# Requirements-based targeting
def isValidTarget(self, target, requirements=None):
	if target.type == CardType.MINION:
		if target.dead:
			return False
		if target.stealthed and self.controller != target.controller:
			return False
		if target.immune and self.controller != target.controller:
			return False
		if self.type in (CardType.SPELL, CardType.HERO_POWER) and target.chromatic:
			return False

	if requirements is None:
		requirements = self.requirements

	for req, param in requirements.items():
		if req == PlayReq.REQ_MINION_TARGET:
			if target.type != CardType.MINION:
				return False
		elif req == PlayReq.REQ_FRIENDLY_TARGET:
			if target.controller != self.controller:
				return False
		elif req == PlayReq.REQ_ENEMY_TARGET:
			if target.controller == self.controller:
				return False
		elif req == PlayReq.REQ_DAMAGED_TARGET:
			if not target.damage:
				return False
		elif req == PlayReq.REQ_TARGET_MAX_ATTACK:
			if target.atk > param or 0:
				return False
		elif req == PlayReq.REQ_NONSELF_TARGET:
			if target is self:
				return False
		elif req == PlayReq.REQ_TARGET_WITH_RACE:
			if target.race != param:
				return False
		elif req == PlayReq.REQ_HERO_TARGET:
			if target.type != CardType.HERO:
				return False
		elif req == PlayReq.REQ_TARGET_MIN_ATTACK:
			if target.atk < param or 0:
				return False
		elif req == PlayReq.REQ_MUST_TARGET_TAUNTER:
			if not target.taunt:
				return False
		elif req == PlayReq.REQ_UNDAMAGED_TARGET:
			if target.damage:
				return False

		# fireplace reqs
		elif req == PlayReq.REQ_SPELL_TARGET:
			if target.type != CardType.SPELL:
				return False
		elif req == PlayReq.REQ_WEAPON_TARGET:
			if target.type != CardType.WEAPON:
				return False
		elif req == PlayReq.REQ_NO_MINIONS_PLAYED_THIS_TURN:
			if self.controller.minionsPlayedThisTurn:
				return False
		elif req == PlayReq.REQ_TARGET_HAS_BATTLECRY:
			if not target.hasBattlecry:
				return False
		elif req == PlayReq.REQ_SOURCE_IS_ENRAGED:
			if not self.enraged:
				return False
	return True
