from ..utils import *


##
# Minions

class ICC_047:
	"""Fatespinner"""
	choose = ("ICC_047a", "ICC_047b")
	player = ChooseBoth(CONTROLLER) & Morph(SELF, "ICC_047t2")


class ICC_047a:
	play = Morph(SELF, "ICC_047t").then(
		SetTag(Morph.CARD, {GameTag.SECRET_DEATHRATTLE: 1})
	)


class ICC_047b:
	play = Morph(SELF, "ICC_047t").then(
		SetTag(Morph.CARD, {GameTag.SECRET_DEATHRATTLE: 2})
	)


class ICC_047t:
	secret_deathrattles = (
		Buff(ALL_MINIONS, "ICC_047e"),
		Hit(ALL_MINIONS, 3)
	)


ICC_047e = buff(+2, +2)


class ICC_047t2:
	deathrattle = Buff(ALL_MINIONS, "ICC_047e"), Hit(ALL_MINIONS, 3)
	play = ChooseBoth(CONTROLLER) & Morph(SELF, "ICC_051t3")


class ICC_051:
	"""Druid of the Swarm"""
	choose = ("ICC_051a", "ICC_051b")


class ICC_051a:
	play = Morph(SELF, "ICC_051t")


class ICC_051b:
	play = Morph(SELF, "ICC_051t2")


class ICC_807:
	"""Strongshell Scavenger"""
	play = Buff(FRIENDLY_MINIONS + TAUNT, "ICC_807e")


ICC_807e = buff(+2, +2)


class ICC_808:
	"""Crypt Lord"""
	events = Summon(CONTROLLER, TAUNT).after(Buff(SELF, "ICC_808e"))


ICC_808e = buff(health=1)


class ICC_835:
	"""Hadronox"""
	play = Summon(CONTROLLER, Copy(FRIENDLY + KILLED + TAUNT))


##
# Spells

class ICC_050:
	"""Webweave"""
	play = Summon(CONTROLLER, "ICC_832t3") * 2


class ICC_054:
	"""Spreading Plague"""
	play = Summon(CONTROLLER, "ICC_832t4").then(
		(Count(FRIENDLY_MINIONS) < Count(ENEMY_MINIONS)) & CastSpell("ICC_054")
	)


class ICC_079:
	"""Gnash"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0}
	play = GainArmor(FRIENDLY_HERO, 3), Buff(FRIENDLY_HERO, "ICC_079e")


ICC_079e = buff(atk=3)


class ICC_085:
	"""Ultimate Infestation"""
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = (
		Hit(TARGET, 5),
		Draw(CONTROLLER) * 5,
		GainArmor(FRIENDLY_HERO, 5),
		Summon(CONTROLLER, "ICC_085t")
	)


##
# Heros

class ICC_832:
	"""Malfurion the Pestilent"""
	choose = ("ICC_832a", "ICC_832b")
	play = ChooseBoth(CONTROLLER) & (
		Summon(CONTROLLER, "ICC_832t4") * 2,
		Summon(CONTROLLER, "ICC_832t3") * 2,
	)


class ICC_832a:
	play = Summon(CONTROLLER, "ICC_832t4") * 2


class ICC_832b:
	play = Summon(CONTROLLER, "ICC_832t4") * 2


class ICC_832p:
	choose = ("ICC_832pa", "ICC_832pa")
	activate = ChooseBoth(CONTROLLER) & (
		GainArmor(FRIENDLY_HERO, 3), Buff(FRIENDLY_HERO, "ICC_832e")
	)


class ICC_832pa:
	activate = GainArmor(FRIENDLY_HERO, 3)


class ICC_832pb:
	activate = Buff(FRIENDLY_HERO, "ICC_832e")


ICC_832e = buff(atk=3)
