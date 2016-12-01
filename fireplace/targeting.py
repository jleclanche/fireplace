"""
Targeting logic
"""
from hearthstone.enums import CardType, PlayReq, Rarity


TARGETING_PREREQUISITES = (
	PlayReq.REQ_TARGET_TO_PLAY,
	PlayReq.REQ_TARGET_FOR_COMBO,
	PlayReq.REQ_TARGET_IF_AVAILABLE,
	PlayReq.REQ_TARGET_IF_AVAILABLE_AND_DRAGON_IN_HAND,
	PlayReq.REQ_TARGET_IF_AVAILABLE_AND_MINIMUM_FRIENDLY_MINIONS,
	PlayReq.REQ_TARGET_IF_AVAILABLE_AND_MINIMUM_FRIENDLY_SECRETS,
)


# Requirements-based targeting
def is_valid_target(self, target, requirements=None):
	if target is self:
		# Battlecries can never target themselves
		return False

	if target.type == CardType.MINION:
		if target.dead:
			return False
		if target.stealthed and self.controller != target.controller:
			return False
		if target.immune and self.controller != target.controller:
			return False
		if self.type == CardType.SPELL and target.cant_be_targeted_by_abilities:
			return False
		if self.type == CardType.HERO_POWER and target.cant_be_targeted_by_hero_powers:
			return False

	if target.cant_be_targeted_by_opponents and self.controller != target.controller:
		return False

	if requirements is None:
		requirements = self.requirements

	# Check if the entity can ever target other entities
	for req in TARGETING_PREREQUISITES:
		if req in requirements:
			break
	else:
		return False

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
		elif req == PlayReq.REQ_FROZEN_TARGET:
			if not target.frozen:
				return False
		elif req == PlayReq.REQ_TARGET_MAX_ATTACK:
			if target.atk > param or 0:
				return False
		elif req == PlayReq.REQ_TARGET_WITH_RACE:
			if target.type != CardType.MINION or target.race != param:
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
		elif req == PlayReq.REQ_LEGENDARY_TARGET:
			if target.rarity != Rarity.LEGENDARY:
				return False
		elif req == PlayReq.REQ_TARGET_WITH_BATTLECRY:
			if not target.has_battlecry:
				return False
		elif req == PlayReq.REQ_TARGET_WITH_DEATHRATTLE:
			if not target.has_deathrattle:
				return False

	return True
