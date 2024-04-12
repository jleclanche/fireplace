from ..utils import *


##
# Minions


class DRG_027:
    """Umbral Skulker"""

    # [x]<b>Battlecry:</b> If you've <b>Invoked</b> twice, add 3 Coins to your hand.
    powered_up = INVOKED_TWICE
    play = powered_up & Give(CONTROLLER, THE_COIN) * 3


class DRG_031:
    """Necrium Apothecary"""

    # <b>Combo:</b> Draw a <b>Deathrattle</b> minion from your deck and gain its
    # <b>Deathrattle</b>.
    combo = ForceDraw(RANDOM(FRIENDLY_DECK + MINION + DEATHRATTLE)).then(
        CopyDeathrattleBuff(ForceDraw.TARGET, "DRG_031e")
    )


class DRG_034:
    """Stowaway"""

    # [x]<b>Battlecry:</b> If there are cards in your deck that didn't start there, draw 2
    # of them.
    play = ForceDraw(RANDOM(FRIENDLY_DECK - STARTING_DECK) * 2)


class DRG_035:
    """Bloodsail Flybooter"""

    # <b>Battlecry:</b> Add two 1/1 Pirates to your hand.
    play = Give(CONTROLLER, "DRG_035t") * 2


class DRG_036:
    """Waxadred"""

    # [x]<b>Deathrattle:</b> Shuffle a Candle into your deck that resummons Waxadred when
    # drawn.
    deathrattle = Shuffle(CONTROLLER, "DRG_036t")


class DRG_036t:
    play = Summon(CONTROLLER, "DRG_036")
    draw = CAST_WHEN_DRAWN


class DRG_037:
    """Flik Skyshiv"""

    # [x]<b>Battlecry:</b> Destroy a minion and all copies of it <i>(wherever they
    # are)</i>.
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0, PlayReq.REQ_MINION_TARGET: 0}
    play = Destroy(
        FilterSelector(
            lambda entity, source: getattr(entity, "id", None) == source.target.id
        )
    )


##
# Spells


class DRG_028:
    """Dragon's Hoard"""

    # <b>Discover</b> a <b>Legendary</b>_minion from another class.
    play = DISCOVER(RandomLegendaryMinion(card_class=ANOTHER_CLASS))


class DRG_030:
    """Praise Galakrond!"""

    # [x]Give a minion +1 Attack. <b>Invoke</b> Galakrond.
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}
    play = Buff(TARGET, "DRG_030e"), Invoke(CONTROLLER)


DRG_030e = buff(atk=1)


class DRG_033:
    """Candle Breath"""

    # Draw 3 cards. Costs (3)_less while you're holding a Dragon.
    cost_mod = HOLDING_DRAGON & -3
    play = Draw(CONTROLLER) * 3


class DRG_247:
    """Seal Fate"""

    # Deal $3 damage to an undamaged character. <b>Invoke</b> Galakrond.
    requirements = requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_UNDAMAGED_TARGET: 0,
    }
    play = Hit(TARGET, 3), Invoke(CONTROLLER)


##
# Heros


class DRG_610:
    """Galakrond, the Nightmare"""

    # [x]<b>Battlecry:</b> Draw 1 card. It costs (0). <i>(@)</i>
    progress_total = 2
    play = Draw(CONTROLLER).then(Buff(Draw.CARD, "DRG_610e"))
    reward = Find(SELF + FRIENDLY_HERO) | (
        Morph(SELF, "DRG_610t2").then(
            SetAttribute(CONTROLLER, "_galakrond", Morph.CARD),
        )
    )


class DRG_610t2:
    """Galakrond, the Apocalypse"""

    # [x]<b>Battlecry:</b> Draw 2 cards. They cost (0). <i>(@)</i>
    progress_total = 2
    play = Draw(CONTROLLER).then(Buff(Draw.CARD, "DRG_610e")) * 2
    reward = Find(SELF + FRIENDLY_HERO) | (
        Morph(SELF, "DRG_610t3").then(
            SetAttribute(CONTROLLER, "_galakrond", Morph.CARD),
        )
    )


class DRG_610t3:
    """Galakrond, Azeroth's End"""

    # [x]<b>Battlecry:</b> Draw 4 cards. They cost (0). Equip a 5/2 Claw.
    play = (
        Draw(CONTROLLER).then(Buff(Draw.CARD, "DRG_610e")) * 4,
        Summon(CONTROLLER, "DRG_238ht"),
    )


class DRG_238p2:
    """Galakrond's Guile"""

    # <b>Hero Power</b> Add a <b>Lackey</b> to your hand.
    activate = Give(CONTROLLER, RandomLackey())


class DRG_610e:
    tags = {GameTag.COST: 1}
    events = REMOVED_IN_PLAY
