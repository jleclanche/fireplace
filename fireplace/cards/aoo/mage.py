from ..utils import *


##
# Minions

class BT_022:
	"""Apexis Smuggler"""
	events = Play(CONTROLLER, SECRET).after(DISCOVER(RandomSpell()))


class BT_014:
	"""Starscryer"""
	deathrattle = ForceDraw(RANDOM(FRIENDLY_DECK + SPELL))


class BT_028:
	"""Astromancer Solarian"""
	deathrattle = Shuffle(CONTROLLER, "BT_028t")


class BT_028t:
	play = CastSpellTargetsEnemiesIfPossible(RandomSpell()) * 5


class BT_004:
	dormant = 2
	awaken = Hit(ENEMY_CHARACTERS, 2)


##
# Spells

class BT_006:
	"""Evocation"""
	play = Give(CONTROLLER, RandomSpell(card_class=CardClass.MAGE)).then(
		Buff(Give.CARD, "BT_006e")) * MAX_HAND_SIZE(CONTROLLER)


class BT_006e:
	events = OWN_TURN_END.on(Discard(OWNER))


class BT_021:
	"""Font of Power"""
	powered_up = -FindDuplicates(FRIENDLY_DECK)
	play = powered_up & (Give(CONTROLLER, RandomMinion(card_class=CardClass.MAGE)) * 3) | (
		DISCOVER(RandomMinion(card_class=CardClass.MAGE)))


class BT_002:
	"""Incanter's Flow"""
	play = Buff(FRIENDLY_DECK + SPELL, "BT_002e")


BT_002e = buff(cost=-1)


class BT_003:
	"""Netherwind Portal"""
	secret = Play(OPPONENT, SPELL).after(Summon(CONTROLLER, RandomMinion(cost=4)))


class BT_291:
	"""Apexis Blast"""
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
	powered_up = -FindDuplicates(FRIENDLY_DECK)
	play = Hit(TARGET, 5), powered_up & Summon(CONTROLLER, RandomMinion(cost=5))


class BT_072:
	"""Deep Freeze"""
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Freeze(TARGET), Summon(CONTROLLER, "CS2_033") * 2
