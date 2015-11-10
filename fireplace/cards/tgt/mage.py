from ..utils import *


##
# Minions

# Dalaran Aspirant
class AT_006:
	inspire = Buff(SELF, "AT_006e")


# Spellslinger
class AT_007:
	play = Give(ALL_PLAYERS, RandomSpell())


# Rhonin
class AT_009:
	deathrattle = Give(CONTROLLER, "EX1_277") * 3


##
# Spells

# Flame Lance
class AT_001:
	play = Hit(TARGET, 8)


# Arcane Blast
class AT_004:
	play = Hit(TARGET, 2)


# Polymorph: Boar
class AT_005:
	play = Morph(TARGET, "AT_005t")


##
# Secrets

# Effigy
class AT_002:
	events = Death(FRIENDLY + MINION).on(
		Reveal(SELF),
		Summon(CONTROLLER, RandomMinion(cost=Attr(Death.Args.ENTITY, GameTag.COST)))
	)
