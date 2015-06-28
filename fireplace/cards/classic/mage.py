from ..utils import *


##
# Hero Powers

# Fireblast (Jaina Proudmoore)
class CS2_034:
	activate = [Hit(TARGET, 1)]


##
# Minions

# Water Elemental
class CS2_033:
	events = [
		Damage().on(
			lambda self, target, amount, source: source is self and [Freeze(target)] or []
		)
	]


# Ethereal Arcanist
class EX1_274:
	events = [
		OWN_TURN_END.on(
			lambda self, player: player.secrets and [Buff(SELF, "EX1_274e")] or []
		)
	]


# Archmage Antonidas
class EX1_559:
	events = [
		OWN_SPELL_PLAY.on(Give(CONTROLLER, "CS2_029"))
	]


# Kirin Tor Mage
class EX1_612:
	action = [Buff(FRIENDLY_HERO, "EX1_612o")]

class EX1_612oa:
	cost = lambda self, i: 0


# Mana Wyrm
class NEW1_012:
	events = [
		OWN_SPELL_PLAY.on(Buff(SELF, "NEW1_012o"))
	]


##
# Spells

# Polymorph
class CS2_022:
	action = [Morph(TARGET, "CS2_tk1")]


# Arcane Intellect
class CS2_023:
	action = [Draw(CONTROLLER) * 2]


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
	action = [Summon(CONTROLLER, "CS2_mirror") * 2]


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
		count = self.controller.get_spell_damage(3)
		return [Hit(RANDOM_ENEMY_CHARACTER, 1) * count]


# Pyroblast
class EX1_279:
	action = [Hit(TARGET, 10)]


##
# Secrets

# Ice Barrier
class EX1_289:
	events = [
		Attack(CHARACTER, FRIENDLY_HERO).on(GainArmor(FRIENDLY_HERO, 8), Reveal(SELF), zone=Zone.SECRET)
	]


# Vaporize
class EX1_594:
	events = [
		Attack(MINION, FRIENDLY_HERO).on(
			lambda self, source, target: [Destroy(source), Reveal(SELF)],
		zone=Zone.SECRET)
	]
