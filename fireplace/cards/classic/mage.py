from ..utils import *


##
# Hero Powers

# Fireblast (Jaina Proudmoore)
class CS2_034:
	activate = Hit(TARGET, 1)

# Fireblast (Medivh)
class CS2_034_H1:
	activate = CS2_034.activate


##
# Minions

# Water Elemental
class CS2_033:
	events = Damage().on(
		lambda self, target, amount, source: source is self and Freeze(target)
	)


# Ethereal Arcanist
class EX1_274:
	events = OWN_TURN_END.on(Find(FRIENDLY_SECRETS) & Buff(SELF, "EX1_274e"))


# Archmage Antonidas
class EX1_559:
	events = OWN_SPELL_PLAY.on(Give(CONTROLLER, "CS2_029"))


# Sorcerer's Apprentice
class EX1_608:
	update = Refresh(FRIENDLY + SPELL + IN_HAND, {GameTag.COST: -1})


# Kirin Tor Mage
class EX1_612:
	play = Buff(FRIENDLY_HERO, "EX1_612o")

class EX1_612o:
	update = Refresh(FRIENDLY + SECRET + IN_HAND, {GameTag.COST: SET(0)})
	events = Play(FRIENDLY + SECRET).on(Destroy(SELF))


# Mana Wyrm
class NEW1_012:
	events = OWN_SPELL_PLAY.on(Buff(SELF, "NEW1_012o"))


##
# Spells

# Polymorph
class CS2_022:
	play = Morph(TARGET, "CS2_tk1")


# Arcane Intellect
class CS2_023:
	play = Draw(CONTROLLER) * 2


# Frostbolt
class CS2_024:
	play = Hit(TARGET, 3), Freeze(TARGET)


# Arcane Explosion
class CS2_025:
	play = Hit(ENEMY_MINIONS, 1)


# Frost Nova
class CS2_026:
	play = Freeze(ENEMY_MINIONS)


# Mirror Image
class CS2_027:
	play = Summon(CONTROLLER, "CS2_mirror") * 2


# Blizzard
class CS2_028:
	play = Hit(ENEMY_MINIONS, 2), Freeze(ENEMY_MINIONS)


# Fireball
class CS2_029:
	play = Hit(TARGET, 6)


# Ice Lance
class CS2_031:
	play = Find(TARGET + FROZEN) & Hit(TARGET, 4) | Freeze(TARGET)


# Flamestrike
class CS2_032:
	play = Hit(ENEMY_MINIONS, 4)


# Cone of Cold
class EX1_275:
	play = Hit(TARGET | TARGET_ADJACENT, 1), Freeze(TARGET | TARGET_ADJACENT)


# Arcane Missiles
class EX1_277:
	def play(self):
		count = self.controller.get_spell_damage(3)
		return Hit(RANDOM_ENEMY_CHARACTER, 1) * count


# Pyroblast
class EX1_279:
	play = Hit(TARGET, 10)


##
# Secrets

# Counterspell
class EX1_287:
	events = Play(OPPONENT, SPELL).on(
		Counter(Play.Args.CARD), Reveal(SELF)
	)


# Ice Barrier
class EX1_289:
	events = Attack(CHARACTER, FRIENDLY_HERO).on(
		GainArmor(FRIENDLY_HERO, 8), Reveal(SELF)
	)


# Mirror Entity
class EX1_294:
	events = Play(OPPONENT, MINION).after(
		Summon(CONTROLLER, ExactCopy(Play.Args.CARD)), Reveal(SELF)
	)


# Vaporize
class EX1_594:
	events = Attack(MINION, FRIENDLY_HERO).on(
		Destroy(Attack.Args.ATTACKER), Reveal(SELF)
	)
