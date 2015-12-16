from ..utils import *


##
# Minions

# Dalaran Aspirant
class AT_006:
	inspire = Buff(SELF, "AT_006e")

AT_006e = buff(spellpower=1)


# Spellslinger
class AT_007:
	play = Give(ALL_PLAYERS, RandomSpell())


# Coldarra Drake
class AT_008:
	update = Refresh(FRIENDLY_HERO_POWER, {GameTag.HEROPOWER_ADDITIONAL_ACTIVATIONS: SET(-1)})


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
	secret = Death(FRIENDLY + MINION).on(FULL_BOARD | (
		Reveal(SELF),
		Summon(CONTROLLER, RandomMinion(cost=COST(Death.ENTITY)))
	))
