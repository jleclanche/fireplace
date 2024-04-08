from ..utils import *


@custom_card
class VAN_EX1_169:
    tags = {
        GameTag.CARDNAME: "Innervate (Old)",
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.CLASS: CardClass.DRUID,
        GameTag.RARITY: Rarity.FREE,
        GameTag.COST: 0,
    }
    play = ManaThisTurn(CONTROLLER, 2)
