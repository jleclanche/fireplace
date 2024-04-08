from ..utils import *


@custom_card
class VAN_EX1_145:
    tags = {
        GameTag.CARDNAME: "Preparation (Old)",
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.CLASS: CardClass.ROGUE,
        GameTag.RARITY: Rarity.EPIC,
        GameTag.COST: 0,
    }
    play = Buff(CONTROLLER, "VAN_EX1_145o")


@custom_card
class VAN_EX1_145o:
    tags = {
        GameTag.CARDNAME: "Preparation (Old)",
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }
    update = Refresh(FRIENDLY_HAND + SPELL, {GameTag.COST: -3})
    events = OWN_SPELL_PLAY.on(Destroy(SELF))
