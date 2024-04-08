from ..utils import *


##
# Minions


class GIL_510:
    """Mistwraith"""

    # Whenever you play an <b>Echo</b>_card, gain +1/+1.
    events = Play(CONTROLLER, ECHO).after(Buff(SELF, "GIL_510e"))


GIL_510e = buff(+1, +1)


class GIL_557:
    """Cursed Castaway"""

    # <b>Rush</b> <b>Deathrattle:</b> Draw a <b>Combo</b> card from your deck.
    deathrattle = ForceDraw(RANDOM(FRIENDLY_DECK + COMBO))


class GIL_598:
    """Tess Greymane"""

    # [x]<b>Battlecry:</b> Replay every card from another class you've played this game
    # <i>(targets chosen randomly)</i>.
    play = Replay(Copy(SHUFFLE(CARDS_PLAYED_THIS_GAME + OTHER_CLASS_CHARACTER)))


class GIL_677:
    """Face Collector"""

    # <b>Echo</b> <b>Battlecry:</b> Add a random <b>Legendary</b> minion to your hand.
    play = Give(CONTROLLER, RandomLegendaryMinion())


class GIL_827:
    """Blink Fox"""

    # <b>Battlecry:</b> Add a random card to your hand <i>(from your opponent's class).</i>
    play = Give(CONTROLLER, RandomCollectible(card_class=ENEMY_CLASS))


class GIL_902:
    """Cutthroat Buccaneer"""

    # <b>Combo:</b> Give your weapon +1 Attack.
    combo = Buff(FRIENDLY_WEAPON, "GIL_902e")


GIL_902e = buff(atk=1)


##
# Spells


class GIL_506:
    """Cheap Shot"""

    # <b>Echo</b> Deal $2 damage to a_minion.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 2)


class GIL_687:
    """WANTED!"""

    # Deal $3 damage to a minion. If that kills it, add a Coin to your hand.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 3), Dead(TARGET) & Give(CONTROLLER, THE_COIN)


class GIL_696:
    """Pick Pocket"""

    # <b>Echo</b> Add a random card to your hand <i>(from your opponent's class).</i>
    play = Give(CONTROLLER, RandomCollectible(card_class=ENEMY_CLASS))


##
# Weapons


class GIL_672:
    """Spectral Cutlass"""

    # [x]<b>Lifesteal</b> Whenever you play a card from another class, gain +1 Durability.
    events = Play(CONTROLLER, OTHER_CLASS_CHARACTER).after(Buff(SELF, "GIL_672e"))


GIL_672e = buff(health=1)
