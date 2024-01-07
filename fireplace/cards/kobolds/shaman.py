from ..utils import *


##
# Minions

class LOOT_062:
	"""Kobold Hermit"""
	# <b>Battlecry:</b> Choose a basic Totem. Summon it.
	play = Choice(CONTROLLER, BASIC_TOTEMS).then(
		Summon(CONTROLLER, Choice.CARD)
	)


class LOOT_358:
	"""Grumble, Worldshaker"""
	# <b>Battlecry:</b> Return your other minions to your hand. They cost (1).
	play = Bounce(FRIENDLY_MINIONS - SELF).then(Buff(Bounce.TARGET, "LOOT_358e"))


class LOOT_358e:
	cost = SET(1)
	events = REMOVED_IN_PLAY


class LOOT_517:
	"""Murmuring Elemental"""
	# <b>Battlecry:</b> Your next <b>Battlecry</b> this turn triggers_twice.
	play = Buff(CONTROLLER, "LOOT_517e")


class LOOT_517e:
	tags = {GameTag.TAG_ONE_TURN_EFFECT: True}
	update = Refresh(CONTROLLER, {enums.EXTRA_BATTLECRIES: True})
	events = Play(CONTROLLER, BATTLECRY).after(Destroy(SELF))


class LOOT_518:
	"""Windshear Stormcaller"""
	# <b>Battlecry:</b> If you control all 4 basic Totems, summon Al'Akir_the_Windlord.
	play = FindAll(
		*[FRIENDLY_MINIONS + ID(totem) for totem in BASIC_TOTEMS]
	) & Summon(CONTROLLER, "NEW1_010")


##
# Spells

class LOOT_060:
	"""Crushing Hand"""
	# Deal $8 damage to a minion. <b><b>Overload</b>:</b> (3)
	play = Hit(TARGET, 8)


class LOOT_064:
	"""Lesser Sapphire Spellstone"""
	# Summon 1 copy of a friendly minion. @<i>(<b>Overload</b> 3 Mana Crystals to
	# upgrade.)</i>
	play = Summon(CONTROLLER, ExactCopy(TARGET))
	progress_total = 3
	reward = Morph(SELF, "LOOT_064t1")

	class Hand:
		events = Play(CONTROLLER, DEATHRATTLE).after(AddProgress(SELF, Play.CARD))


class LOOT_064t1:
	"""Sapphire Spellstone"""
	# Summon 2 copies of a friendly minion. @
	play = Summon(CONTROLLER, ExactCopy(TARGET)) * 2
	progress_total = 3
	reward = Morph(SELF, "LOOT_064t2")

	class Hand:
		events = Play(CONTROLLER, DEATHRATTLE).after(AddProgress(SELF, Play.CARD))


class LOOT_064t2:
	"""Greater Sapphire Spellstone"""
	# Summon 3 copies of a friendly minion.
	play = Summon(CONTROLLER, ExactCopy(TARGET)) * 3


class LOOT_344:
	"""Primal Talismans"""
	# Give your minions "<b>Deathrattle:</b> Summon a random basic Totem."
	deathrattle = Buff(ALL_MINIONS, "LOOT_344e")


class LOOT_344e:
	tags = {
		GameTag.DEATHRATTLE: True
	}
	deathrattle = Summon(CONTROLLER, RandomBasicTotem())


class LOOT_373:
	"""Healing Rain"""
	# Restore #12 Health randomly split among all friendly characters.
	play = Heal(RANDOM_FRIENDLY_CHARACTER, 1) * SPELL_HEAL(12)


class LOOT_504:
	"""Unstable Evolution"""
	# Transform a friendly minion into one that costs (1) more. Repeatable this turn.
	play = Evolve(TARGET, 1), Give(CONTROLLER, "LOOT_504t")


class LOOT_504t:
	play = Evolve(TARGET, 1), Give(CONTROLLER, "LOOT_504t")
	events = OWN_TURN_END.on(Destroy(SELF))


##
# Weapons

class LOOT_506:
	"""The Runespear"""
	# After your hero attacks, <b>Discover</b> a spell and cast it with random targets.
	events = Attack(FRIENDLY_HERO).after(
		Discover(CONTROLLER, RandomSpell()).then(CastSpell(Discover.CARD))
	)
