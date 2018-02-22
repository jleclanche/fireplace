from ..utils import *


##
# Minions

class OG_023:
	"Primal Fusion"
	play = Buff(TARGET, "OG_023t") * Count(FRIENDLY_MINIONS + TOTEM)

OG_023t = buff(+1, +1)


class OG_026:
	"Eternal Sentinel"
	play = UnlockOverload(CONTROLLER)


class OG_028:
	"Thing from Below"
	cost_mod = -Attr(CONTROLLER, 'totems_played_this_game')

class OG_209:
	"Hallazeal the Ascended"
	events = Damage(source=SPELL + FRIENDLY).on(Heal(FRIENDLY_HERO, Damage.AMOUNT))


class OG_328:
	"Master of Evolution"
	play = (COST(TARGET) >= 12) | Morph(TARGET, RandomMinion(cost=COST_ADD(TARGET)))


##
# Spells

class OG_027:
	"Evolve"
	def play(self):
		for i in self.controller.field:
			if i.cost<12:
				into = RandomMinion(cost=i.cost_add).evaluate(self.controller)
				yield Morph(i, into)

class OG_206:
	"Stormcrack"
	play = Hit(TARGET, 4)


##
# Weapons

class OG_031:
	"Hammer of Twilight"
	deathrattle = Summon(CONTROLLER, "OG_031a")
