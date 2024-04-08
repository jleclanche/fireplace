from ..utils import *


@custom_card
class VAN_CS2_103:
    tags = {
        GameTag.CARDNAME: "Charge (Old)",
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.CLASS: CardClass.WARRIOR,
        GameTag.RARITY: Rarity.COMMON,
        GameTag.COST: 3,
    }
    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Buff(TARGET, "VAN_CS2_103e2")


@custom_card
class VAN_CS2_103e2:
    tags = {
        GameTag.CARDNAME: "Charge",
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.CHARGE: True,
        GameTag.ATK: 2,
    }
