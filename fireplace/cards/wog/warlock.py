from ..utils import *


##
# Minions

class OG_109:
	"Darkshire Librarian"
	play = Discard(RANDOM(FRIENDLY_HAND))
	deathrattle = Draw(CONTROLLER)


class OG_113:
	"Darkshire Councilman"
	events = Summon(MINION, CONTROLLER).on(Buff(SELF, "OG_113e"))

OG_113e = buff(atk=1)


class OG_121:
	"Cho'gall"
	play = Buff(CONTROLLER, "OG_121e")

class OG_121e:
	events = OWN_SPELL_PLAY.on(Destroy(SELF))
	update = Refresh(CONTROLLER, {GameTag.SPELLS_COST_HEALTH: True})


class OG_241:
	"Possessed Villager"
	deathrattle = Summon(CONTROLLER, "OG_241a")


##
# Spells

class OG_116:
	"Spreading Madness"
	play = Hit(RANDOM_CHARACTER, 1) * 9


class OG_239:
	"DOOM!"
	def play(self):
		minion_count = len(self.controller.field) + len(self.controller.opponent.field)
		yield Destroy(ALL_MINIONS)
		yield Draw(CONTROLLER) * minion_count
