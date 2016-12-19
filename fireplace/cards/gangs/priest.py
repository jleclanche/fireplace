from ..utils import *

##
# Minions

class CFM_020:
	"Raza the Chained"
	play = Buff(CONTROLLER, "CFM_020e")

class CFM_020e:
	update = Refresh(FRIENDLY_HERO_POWER, {GameTag.COST: SET(0)})

class CFM_605:
	"Drakonid Operative"
	powered_up = HOLDING_DRAGON
	def play(self):
		decklist = [i.id for i in self.controller.opponent.deck]
		yield HOLDING_DRAGON & DISCOVER(RandomID(*decklist))

class CFM_606:
	"Mana Geode"
	events = Heal(SELF).on(Summon(CONTROLLER, "CFM_606t"))

class CFM_626:
	"Kabal Talonpriest"
	play = Buff(TARGET, "CFM_626e")

CFM_626e = buff(0, +3)

class CFM_657:
	"Kabal Songstealer"
	play = Silence(TARGET)

##
# Spells

class CFM_603:
	"Potion of Madness"
	play = Steal(TARGET), Buff(TARGET, "CFM_603e")

class CFM_603e:
	events = [
		TURN_END.on(Destroy(SELF), Steal(OWNER, OPPONENT)),
		Silence(OWNER).on(Steal(OWNER, OPPONENT))
	]
	tags = {GameTag.CHARGE: True}

#class CFM_604:
#	"Greater Healing Potion"

#class CFM_661:
#	"Pint-Size Potion"

#class CFM_662:
#	"Dragonfire Potion"

