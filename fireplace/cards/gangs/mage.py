from ..utils import *

##
# Minions

class CFM_066:
	"Kabal Lackey"
	play = Buff(CONTROLLER, "EX1_612o")

class CFM_660:
	"Manic Soulcaster"
	play = Shuffle(CONTROLLER, Copy(TARGET))

class CFM_671:
	"Cryomancer"
	powered_up = Find(ENEMY_CHARACTERS + FROZEN)
	play = powered_up & Buff(SELF, "CFM_671e")

CFM_671e = buff(+2, +2)

class CFM_687:
	"Inkmaster Solia"
	powered_up = -FindDuplicates(FRIENDLY_DECK)
	play = powered_up & Buff(CONTROLLER, "CFM_687e")

class CFM_687e:
	update = Refresh(FRIENDLY_HAND + SPELL, {GameTag.COST: SET(0)})
	events = OWN_SPELL_PLAY.on(Destroy(SELF))


class CFM_760:
	"Kabal Crystal Runner"
	cost_mod = - Attr(CONTROLLER, "secrets_played_this_game") * 2

##
# Spells

class CFM_021:
	"Freezing Potion"
	play = Freeze(TARGET)

class CFM_065:
	"Volcanic Potion"
	play = Hit(ALL_MINIONS, 2)

class CFM_620:
	"Potion of Polymorph"
	secret = Play(OPPONENT, MINION).on(Reveal(SELF), Morph(Play.CARD, "CS2_tk1"))

class CFM_623:
	"Greater Arcane Missiles"
	play = Hit(RANDOM_ENEMY_CHARACTER, 3) * 3

