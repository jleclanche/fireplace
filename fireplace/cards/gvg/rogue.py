from ..utils import *


##
# Minions

# Goblin Auto-Barber
class GVG_023:
	play = Buff(FRIENDLY_WEAPON, "GVG_023a")


# One-eyed Cheat
class GVG_025:
	events = Summon(CONTROLLER, PIRATE - SELF).on(SetTag(SELF, {GameTag.STEALTH: True}))


# Iron Sensei
class GVG_027:
	events = OWN_TURN_END.on(Buff(RANDOM(FRIENDLY_MINIONS + MECH - SELF), "GVG_027e"))


# Trade Prince Gallywix
class GVG_028:
	events = Play(OPPONENT, SPELL).on(
		lambda self, player, card, *args: card.id != "GVG_028t" and (
			Give(player.opponent, card.id),
			Give(player, "GVG_028t")
		)
	)

class GVG_028t:
	play = ManaThisTurn(CONTROLLER, 1)


##
# Spells

# Tinker's Sharpsword Oil
class GVG_022:
	play = Buff(FRIENDLY_WEAPON, "GVG_022a")
	combo = Buff(FRIENDLY_WEAPON, "GVG_022a"), Buff(RANDOM_FRIENDLY_CHARACTER, "GVG_022b")


# Sabotage
class GVG_047:
	play = Destroy(RANDOM_ENEMY_MINION)
	combo = Destroy(ENEMY_WEAPON | RANDOM_ENEMY_MINION)

##
# Weapons

# Cogmaster's Wrench
class GVG_024:
	def atk(self, i):
		if self.controller.field.filter(race=Race.MECHANICAL):
			return i + 2
		return i
