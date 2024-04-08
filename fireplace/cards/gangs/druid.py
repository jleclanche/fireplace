from ..utils import *


##
# Minions


class CFM_308:
    """Kun the Forgotten King"""

    choose = ("CFM_308a", "CFM_308b")
    play = ChooseBoth(CONTROLLER) & (
        GainArmor(FRIENDLY_HERO, 10),
        FillMana(CONTROLLER, USED_MANA(CONTROLLER)),
    )


class CFM_308a:
    play = GainArmor(FRIENDLY_HERO, 10)


class CFM_308b:
    play = FillMana(CONTROLLER, USED_MANA(CONTROLLER))


class CFM_343(JadeGolemUtils):
    """Jade Behemoth"""

    play = SummonJadeGolem(CONTROLLER)


class CFM_617:
    """Celestial Dreamer"""

    powered_up = Find(FRIENDLY_MINIONS - SELF + (ATK >= 5))
    play = powered_up & Buff(SELF, "CFM_617e")


CFM_617e = buff(+2, +2)


class CFM_816:
    """Virmen Sensei"""

    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_WITH_RACE: 20,
    }
    play = Buff(TARGET, "CFM_816e")


CFM_816e = buff(+2, +2)


##
# Spells


class CFM_602(JadeGolemUtils):
    """Jade Idol"""

    choose = ("CFM_602a", "CFM_602b")
    play = ChooseBoth(CONTROLLER) & (
        SummonJadeGolem(CONTROLLER),
        Shuffle(CONTROLLER, "CFM_602") * 3,
    )


class CFM_602a(JadeGolemUtils):
    play = SummonJadeGolem(CONTROLLER)


class CFM_602b:
    play = Shuffle(CONTROLLER, "CFM_602") * 3


class CFM_614:
    """Mark of the Lotus"""

    play = Buff(FRIENDLY_MINIONS, "CFM_614e")


CFM_614e = buff(+1, +1)


class CFM_616:
    """Pilfered Power"""

    play = (Count(FRIENDLY_MINIONS) > 0) & (
        AT_MAX_MANA(CONTROLLER) & Give(CONTROLLER, "CS2_013t")
        | GainEmptyMana(
            CONTROLLER,
            Min(MAX_MANA(CONTROLLER) - MANA(CONTROLLER), Count(FRIENDLY_MINIONS)),
        )
    )


class CFM_713(JadeGolemUtils):
    """Jade Blossom"""

    requirements = {
        PlayReq.REQ_MINION_SLOT_OR_MANA_CRYSTAL_SLOT: 0,
    }
    play = SummonJadeGolem(CONTROLLER), GainEmptyMana(CONTROLLER, 1)


class CFM_811:
    """Lunar Visions"""

    play = (
        Draw(CONTROLLER).then(Find(Draw.CARD + MINION) & Buff(Draw.CARD, "CFM_811e"))
        * 2
    )


@custom_card
class CFM_811e:
    tags = {
        GameTag.CARDNAME: "Lunar Visions Buff",
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.COST: -2,
    }
    events = REMOVED_IN_PLAY
