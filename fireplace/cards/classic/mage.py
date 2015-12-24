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
	events = Damage(CHARACTER, None, SELF).on(Freeze(Damage.TARGET))


# Ethereal Arcanist
class EX1_274:
	events = OWN_TURN_END.on(Find(FRIENDLY_SECRETS) & Buff(SELF, "EX1_274e"))

EX1_274e = buff(+2, +2)


# Archmage Antonidas
class EX1_559:
	events = OWN_SPELL_PLAY.on(Give(CONTROLLER, "CS2_029"))


# Sorcerer's Apprentice
class EX1_608:
	update = Refresh(FRIENDLY_HAND + SPELL, {GameTag.COST: -1})


# Kirin Tor Mage
class EX1_612:
	play = Buff(FRIENDLY_HERO, "EX1_612o")

class EX1_612o:
	update = Refresh(FRIENDLY_HAND + SECRET, {GameTag.COST: SET(0)})
	events = Play(CONTROLLER, SECRET).on(Destroy(SELF))


# Mana Wyrm
class NEW1_012:
	events = OWN_SPELL_PLAY.on(Buff(SELF, "NEW1_012o"))

NEW1_012o = buff(atk=1)


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
		yield Hit(RANDOM_ENEMY_CHARACTER, 1) * count


# Pyroblast
class EX1_279:
	play = Hit(TARGET, 10)


##
# Secrets

# Spellbender
class tt_010:
	secret = Play(OPPONENT, SPELL, MINION).on(FULL_BOARD | (
		Reveal(SELF), Retarget(Play.CARD, Summon(CONTROLLER, "tt_010a"))
	))


# Counterspell
class EX1_287:
	secret = Play(OPPONENT, SPELL).on(
		Reveal(SELF), Counter(Play.CARD)
	)


# Ice Barrier
class EX1_289:
	secret = Attack(CHARACTER, FRIENDLY_HERO).on(
		Reveal(SELF), GainArmor(FRIENDLY_HERO, 8)
	)


# Mirror Entity
class EX1_294:
	secret = [
		Play(OPPONENT, MINION).after(
			Reveal(SELF), Summon(CONTROLLER, ExactCopy(Play.CARD))
		),
		Play(OPPONENT, ID("EX1_323h")).after(
			Reveal(SELF), Summon(CONTROLLER, "EX1_323")
		)  # :-)
	]


# Ice Block
class EX1_295:
	secret = Predamage(FRIENDLY_HERO).on(
		Lethal(FRIENDLY_HERO, Predamage.AMOUNT) & (
			Reveal(SELF), Buff(FRIENDLY_HERO, "EX1_295o")
		)
	)

EX1_295o = buff(immune=True)


# Vaporize
class EX1_594:
	secret = Attack(MINION, FRIENDLY_HERO).on(
		Reveal(SELF), Destroy(Attack.ATTACKER)
	)
