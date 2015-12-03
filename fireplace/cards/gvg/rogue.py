from ..utils import *


##
# Minions

# Goblin Auto-Barber
class GVG_023:
	play = Buff(FRIENDLY_WEAPON, "GVG_023a")

GVG_023a = buff(atk=1)


# One-eyed Cheat
class GVG_025:
	events = Summon(CONTROLLER, PIRATE - SELF).on(Stealth(SELF))


# Iron Sensei
class GVG_027:
	events = OWN_TURN_END.on(Buff(RANDOM(FRIENDLY_MINIONS + MECH - SELF), "GVG_027e"))

GVG_027e = buff(+2, +2)


# Trade Prince Gallywix
class GVG_028:
	events = Play(OPPONENT, SPELL - ID("GVG_028t")).on(
		Give(CONTROLLER, Copy(Play.CARD)),
		Give(OPPONENT, "GVG_028t")
	)

class GVG_028t:
	play = ManaThisTurn(CONTROLLER, 1)


##
# Spells

# Tinker's Sharpsword Oil
class GVG_022:
	play = Buff(FRIENDLY_WEAPON, "GVG_022a")
	combo = Buff(FRIENDLY_WEAPON, "GVG_022a"), Buff(RANDOM_FRIENDLY_CHARACTER, "GVG_022b")

GVG_022a = buff(atk=3)  # Weapon
GVG_022b = buff(atk=3)  # Minion


# Sabotage
class GVG_047:
	play = Destroy(RANDOM_ENEMY_MINION)
	combo = Destroy(ENEMY_WEAPON | RANDOM_ENEMY_MINION)


##
# Weapons

# Cogmaster's Wrench
class GVG_024:
	update = Find(FRIENDLY_MINIONS + MECH) & Refresh(SELF, {GameTag.ATK: +2})
