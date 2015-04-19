from ..utils import *


##
# Minions

# Ethereal Arcanist
class EX1_274:
	def OWN_TURN_END(self):
		if self.controller.secrets:
			return [Buff(SELF, "EX1_274e")]


# Archmage Antonidas
class EX1_559:
	def OWN_CARD_PLAYED(self, card):
		if card.type == CardType.SPELL:
			return [Give(CONTROLLER, "CS2_029")]


# Mana Wyrm
class NEW1_012:
	def OWN_CARD_PLAYED(self, card):
		if card.type == CardType.SPELL:
			return [Buff(SELF, "NEW1_012o")]


##
# Spells

# Polymorph
class CS2_022:
	action = [Morph(TARGET, "CS2_tk1")]


# Arcane Intellect
class CS2_023:
	action = [Draw(CONTROLLER, 2)]


# Frostbolt
class CS2_024:
	action = [Hit(TARGET, 3), Freeze(TARGET)]


# Arcane Explosion
class CS2_025:
	action = [Hit(ENEMY_MINIONS, 1)]


# Frost Nova
class CS2_026:
	action = [Freeze(ENEMY_MINIONS)]


# Mirror Image
class CS2_027:
	action = [Summon(CONTROLLER, "CS2_mirror"), Summon(CONTROLLER, "CS2_mirror")]


# Blizzard
class CS2_028:
	action = [Hit(ENEMY_MINIONS, 2), Freeze(ENEMY_MINIONS)]


# Fireball
class CS2_029:
	action = [Hit(TARGET, 6)]


# Ice Lance
class CS2_031:
	def action(self, target):
		if target.frozen:
			return [Hit(TARGET, 4)]
		return [Freeze(TARGET)]


# Flamestrike
class CS2_032:
	action = [Hit(ENEMY_MINIONS, 4)]


# Cone of Cold
class EX1_275:
	action = [Hit(TARGET | TARGET_ADJACENT, 1), Freeze(TARGET | TARGET_ADJACENT)]


# Arcane Missiles
class EX1_277:
	def action(self):
		count = 3 + self.controller.spellpower
		return [Hit(RANDOM_ENEMY_CHARACTER, 1) * count]


# Pyroblast
class EX1_279:
	action = [Hit(TARGET, 10)]


##
# Secrets

# Ice Barrier
class EX1_289:
	def BEFORE_ATTACK(self, source, target):
		if target == self.controller.hero:
			return [GainArmor(FRIENDLY_HERO, 8), Reveal(SELF)]


# Vaporize
class EX1_594:
	def ATTACK(self, source, target):
		if target == self.controller.hero and source.type == CardType.MINION:
			return [Destroy(source), Reveal(SELF)]
