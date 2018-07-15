from ..utils import *


# Pre-nerf Warsong Commander for tests
@custom_card
class FIREPLACE_EX1_084:
	tags = {
		GameTag.CARDNAME: "Warsong Commander (Old)",
		GameTag.CARDTYPE: CardType.MINION,
		GameTag.CLASS: CardClass.WARRIOR,
		GameTag.COST: 3,
		GameTag.ATK: 2,
		GameTag.HEALTH: 3,
	}
	events = Summon(CONTROLLER, MINION + (ATK <= 3)).after(
		Buff(Summon.CARD, "FIREPLACE_EX1_084e")
	)


@custom_card
class FIREPLACE_EX1_084e:
	tags = {
		GameTag.CARDNAME: "Charge (Old)",
		GameTag.CARDTYPE: CardType.ENCHANTMENT,
		GameTag.CHARGE: True,
	}
