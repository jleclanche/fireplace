from ..utils import *


##
# Minions


class BT_196:
    """Keli'dan the Breaker"""

    # [x]<b>Battlecry:</b> Destroy a minion. If drawn this turn, instead
    # destroy all minions except this one.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE_AND_NOT_DRAWN_THIS_TURN: 0,
    }
    powered_up = Find(SELF + DRAWN_THIS_TURN)
    play = powered_up & Destroy(ALL_MINIONS - SELF) | Destroy(TARGET)


class BT_301:
    """Nightshade Matron"""

    # <b>Rush</b> <b>Battlecry:</b> Discard your highest Cost card.
    play = Discard(HIGHEST_COST(FRIENDLY_HAND))


class BT_304:
    """Enhanced Dreadlord"""

    # [x]<b>Taunt</b> <b>Deathrattle:</b> Summon a 5/5 Dreadlord with
    # <b>Lifesteal</b>.
    deathrattle = Summon(CONTROLLER, "BT_304t")


class BT_305:
    """Imprisoned Scrap Imp"""

    # <b>Dormant</b> for 2 turns. When this awakens, give all minions in your
    # hand +2/+1.
    tags = {GameTag.DORMANT: True}
    dormant_turns = 2
    awaken = Buff(FRIENDLY_HAND, "BT_305e")


BT_305e = buff(+2, +1)


class BT_307:
    """Darkglare"""

    # After your hero takes damage, refresh 2 Mana_Crystals.
    events = Damage(FRIENDLY_HERO).on(FillMana(CONTROLLER, 2))


class BT_309:
    """Kanrethad Ebonlocke"""

    # [x]Your Demons cost (1) less. <b>Deathrattle:</b> Shuffle 'Kanrethad
    # Prime' into your deck.
    update = Refresh(FRIENDLY_HAND + DEMON, {GameTag.COST: -1})
    deathrattle = Shuffle(CONTROLLER, "BT_309t")


class BT_309t:
    """Kanrethad Prime"""

    # <b>Battlecry:</b> Summon 3 friendly Demons that died_this game.
    play = Summon(CONTROLLER, Copy(RANDOM(FRIENDLY + KILLED + DEMON) * 3))


##
# Spells


class BT_199:
    """Unstable Felbolt"""

    # Deal $3 damage to an enemy minion and a random friendly one.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
    }
    play = Hit(TARGET, 3), Hit(RANDOM_FRIENDLY_MINION, 3)


class BT_300:
    """Hand of Gul'dan"""

    # When you play or discard this, draw 3 cards.
    play = discard = Draw(CONTROLLER) * 3


class BT_302:
    """The Dark Portal"""

    # Draw a minion. If you have at least 8 cards in hand, it costs (5) less.
    powered_up = Count(FRIENDLY_HAND - SELF) >= 7
    play = powered_up & (
        ForceDraw(RANDOM(FRIENDLY_DECK + MINION)).then(
            Buff(ForceDraw.TARGET, "BT_302e")
        )
    ) | (ForceDraw(RANDOM(FRIENDLY_DECK + MINION)))


class BT_302e:
    tags = {GameTag.COST: -5}
    events = REMOVED_IN_PLAY


class BT_306:
    """Shadow Council"""

    # Replace your hand with random Demons. Give them +2/+2.
    play = Morph(FRIENDLY_HAND, RandomDemon()).then(Buff(Morph.CARD, "BT_306e"))


BT_306e = buff(+2, +2)
