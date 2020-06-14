from ..utils import *


##
# Hero Powers

class HERO_08bp:
	"""Fireblast (Jaina Proudmoore)"""
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
	activate = Hit(TARGET, 1)


class CS2_034_H1:
	"""Fireblast (Medivh)"""
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
	activate = HERO_08bp.activate


class CS2_034_H2:
	"""Fireblast (Khadgar)"""
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
	activate = HERO_08bp.activate


##
# Minions

class CS2_033:
	"""Water Elemental"""
	events = Damage(CHARACTER, None, SELF).on(Freeze(Damage.TARGET))


class EX1_274:
	"""Ethereal Arcanist"""
	events = OWN_TURN_END.on(Find(FRIENDLY_SECRETS) & Buff(SELF, "EX1_274e"))


EX1_274e = buff(+2, +2)


class EX1_559:
	"""Archmage Antonidas"""
	events = OWN_SPELL_PLAY.on(Give(CONTROLLER, "CS2_029"))


class EX1_608:
	"""Sorcerer's Apprentice"""
	update = Refresh(FRIENDLY_HAND + SPELL, {GameTag.COST: -1})


class EX1_612:
	"""Kirin Tor Mage"""
	play = Buff(CONTROLLER, "EX1_612o")


class EX1_612o:
	update = Refresh(FRIENDLY_HAND + SECRET, {GameTag.COST: SET(0)})
	events = Play(CONTROLLER, SECRET).on(Destroy(SELF))


class NEW1_012:
	"""Mana Wyrm"""
	events = OWN_SPELL_PLAY.on(Buff(SELF, "NEW1_012o"))


NEW1_012o = buff(atk=1)


##
# Spells

class CS2_022:
	"""Polymorph"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Morph(TARGET, "CS2_tk1")


class CS2_023:
	"""Arcane Intellect"""
	play = Draw(CONTROLLER) * 2


class CS2_024:
	"""Frostbolt"""
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Hit(TARGET, 3), Freeze(TARGET)


class CS2_025:
	"""Arcane Explosion"""
	play = Hit(ENEMY_MINIONS, 1)


class CS2_026:
	"""Frost Nova"""
	play = Freeze(ENEMY_MINIONS)


class CS2_027:
	"""Mirror Image"""
	requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
	play = Summon(CONTROLLER, "CS2_mirror") * 2


class CS2_028:
	"""Blizzard"""
	play = Hit(ENEMY_MINIONS, 2), Freeze(ENEMY_MINIONS)


class CS2_029:
	"""Fireball"""
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Hit(TARGET, 6)


class CS2_031:
	"""Ice Lance"""
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Find(TARGET + FROZEN) & Hit(TARGET, 4) | Freeze(TARGET)


class CS2_032:
	"""Flamestrike"""
	play = Hit(ENEMY_MINIONS, 4)


class EX1_275:
	"""Cone of Cold"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Hit(TARGET | TARGET_ADJACENT, 1), Freeze(TARGET | TARGET_ADJACENT)


class EX1_277:
	"""Arcane Missiles"""
	def play(self):
		count = self.controller.get_spell_damage(3)
		yield Hit(RANDOM_ENEMY_CHARACTER, 1) * count


class EX1_279:
	"""Pyroblast"""
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Hit(TARGET, 10)


##
# Secrets

class tt_010:
	"""Spellbender"""
	secret = Play(OPPONENT, SPELL, MINION).on(FULL_BOARD | (
		Reveal(SELF), Retarget(Play.CARD, Summon(CONTROLLER, "tt_010a"))
	))


class EX1_287:
	"""Counterspell"""
	secret = Play(OPPONENT, SPELL).on(
		Reveal(SELF), Counter(Play.CARD)
	)


class EX1_289:
	"""Ice Barrier"""
	secret = Attack(CHARACTER, FRIENDLY_HERO).on(
		Reveal(SELF), GainArmor(FRIENDLY_HERO, 8)
	)


class EX1_294:
	"""Mirror Entity"""
	secret = [
		Play(OPPONENT, MINION).after(
			Reveal(SELF), Summon(CONTROLLER, ExactCopy(Play.CARD))
		),
		Play(OPPONENT, ID("EX1_323h")).after(
			Reveal(SELF), Summon(CONTROLLER, "EX1_323")
		)  # :-)
	]


class EX1_295:
	"""Ice Block"""
	secret = Predamage(FRIENDLY_HERO).on(
		Lethal(FRIENDLY_HERO, Predamage.AMOUNT) & (
			Reveal(SELF),
			Buff(FRIENDLY_HERO, "EX1_295o"),
			Predamage(FRIENDLY_HERO, 0)
		)
	)


EX1_295o = buff(immune=True)


class EX1_594:
	"""Vaporize"""
	secret = Attack(MINION, FRIENDLY_HERO).on(
		Reveal(SELF), Destroy(Attack.ATTACKER)
	)
