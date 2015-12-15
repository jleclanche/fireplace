from ..utils import *


##
# Minions

# King of Beasts
class GVG_046:
	play = Buff(SELF, "GVG_046e") * Count(FRIENDLY_MINIONS + BEAST)

GVG_046e = buff(atk=1)


# Metaltooth Leaper
class GVG_048:
	play = Buff(RANDOM(FRIENDLY_MINIONS + MECH - SELF), "GVG_048e")

GVG_048e = buff(atk=2)


# Gahz'rilla
class GVG_049:
	events = SELF_DAMAGE.on(Buff(SELF, "GVG_049e"))

class GVG_049e:
	atk = lambda self, i: i * 2


# Steamwheedle Sniper
class GVG_087:
	update = Refresh(CONTROLLER, {GameTag.STEADY_SHOT_CAN_TARGET: True})


##
# Spells

# Call Pet
class GVG_017:
	play = Draw(CONTROLLER).then(
		Find(BEAST + Draw.CARD) & Buff(Draw.CARD, "GVG_017e")
	)

@custom_card
class GVG_017e:
	tags = {
		GameTag.CARDNAME: "Call Pet Buff",
		GameTag.CARDTYPE: CardType.ENCHANTMENT,
		GameTag.COST: -4,
	}


# Feign Death
class GVG_026:
	play = Deathrattle(FRIENDLY_MINIONS)


# Cobra Shot
class GVG_073:
	play = Hit(TARGET | ENEMY_HERO, 3)


##
# Weapons

# Glaivezooka
class GVG_043:
	play = Buff(RANDOM_FRIENDLY_MINION, "GVG_043e")

GVG_043e = buff(atk=1)
