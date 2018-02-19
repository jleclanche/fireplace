from ..utils import *

##
# Minions

class CFM_308:
	"Kun the Forgotten King"
	choose = ("CFM_308a", "CFM_308b")
	play = ChooseBoth(CONTROLLER) & (GainArmor(FRIENDLY_HERO, 10), FillMana(CONTROLLER, USED_MANA(CONTROLLER)))

class CFM_308a:
	play = GainArmor(FRIENDLY_HERO, 10)

class CFM_308b:
	play = FillMana(CONTROLLER, USED_MANA(CONTROLLER))

class CFM_343:
	"Jade Behemoth"
	play = SummonJadeGolem(CONTROLLER)

class CFM_617:
	"Celestial Dreamer"
	powered_up = Find(FRIENDLY_MINIONS + (ATK >= 5))
	play = powered_up & Buff(SELF, "CFM_617e")

CFM_617e = buff(+2,+2)

class CFM_816:
	"Virmen Sensei"
	powered_up  = Find(FRIENDLY_MINIONS + BEAST)
	play = Buff(TARGET, "CFM_816e")

CFM_816e = buff(+2,+2)

##
# Spells

class CFM_602:
	"Jade Idol"
	choose = ("CFM_602a", "CFM_602b")
	play = ChooseBoth(CONTROLLER) & (SummonJadeGolem(CONTROLLER), Shuffle(CONTROLLER, "CFM_602") * 3)

class CFM_602a:
	play = SummonJadeGolem(CONTROLLER)

class CFM_602b:
	play = Shuffle(CONTROLLER, "CFM_602") * 3

class CFM_614:
	"Mark of the Lotus"
	play = Buff(FRIENDLY_MINIONS, "CFM_614e")

CFM_614e = buff(+1,+1)

class CFM_616:
	"Pilfered Power"
	play = (
		AT_MAX_MANA(CONTROLLER) &
		Give(CONTROLLER, "CS2_013t") |
		GainEmptyMana(CONTROLLER, Count(FRIENDLY_MINIONS))
	)

class CFM_713:
	"Jade Blossom"
	play = (
		AT_MAX_MANA(CONTROLLER) & SummonJadeGolem(CONTROLLER) |
		(SummonJadeGolem(CONTROLLER), *GainEmptyMana(CONTROLLER, 1))
		)

class CFM_811:
	"Lunar Visions"
	play = (Draw(CONTROLLER) * 2).then(
		Find(MINION + Draw.CARD) & Buff(Draw.CARD, "CFM_811e")
	)

@custom_card
class CFM_811e:
	tags = {
		GameTag.CARDNAME: "Lunar Visions Buff",
		GameTag.CARDTYPE: CardType.ENCHANTMENT,
		GameTag.COST: -2,
	}
	events = REMOVED_IN_PLAY


