from ..utils import *


##
# Minions


class BT_127:
    """Imprisoned Satyr"""

    # [x]<b>Dormant</b> for 2 turns. When this awakens, reduce the Cost of a
    # random minion in your hand by (5).
    tags = {GameTag.DORMANT: True}
    dormant_turns = 2
    awaken = Buff(RANDOM(FRIENDLY_HAND + MINION), "BT_127e")


class BT_127e:
    tags = {GameTag.COST: -5}
    events = REMOVED_IN_PLAY


class BT_131:
    """Ysiel Windsinger"""

    # Your spells cost (1).
    update = Refresh(FRIENDLY_HAND + SPELL, {GameTag.COST: SET(1)})


class BT_133:
    """Marsh Hydra"""

    # [x]<b>Rush</b> After this attacks, add a random 8-Cost minion to your
    # hand.
    events = Attack(SELF).after(Give(CONTROLLER, RandomMinion(cost=8)))


class BT_136:
    """Archspore Msshi'fn"""

    # [x]<b>Taunt</b> <b>Deathrattle:</b> Shuffle 'Msshi'fn Prime' into your
    # deck.
    deathrattle = Shuffle(CONTROLLER, "BT_136t")


class BT_136t:
    """Msshi'fn Prime"""

    # <b>Taunt</b> <b>Choose One -</b> Summon a 9/9 Fungal Giant with
    # <b>Taunt</b>; or <b>Rush</b>.
    choose = ("BT_136ta", "BT_136tb")
    play = ChooseBoth(CONTROLLER) & Summon(CONTROLLER, "BT_136tt3")


class BT_136ta:
    play = Summon(CONTROLLER, "BT_136tt1")


class BT_136ta:
    play = Summon(CONTROLLER, "BT_136tt2")


##
# Spells


class BT_128:
    """Fungal Fortunes"""

    # Draw 3 cards. Discard any minions drawn.
    play = Draw(CONTROLLER).then(Find(Draw.CARD + MINION) & Discard(Draw.CARD)) * 3


class BT_129:
    """Germination"""

    # Summon a copy of a friendly minion. Give the copy <b>Taunt</b>.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Summon(CONTROLLER, ExactCopy(TARGET)).then(Taunt(Summon.CARD))


class BT_130:
    """Overgrowth"""

    # Gain two empty Mana_Crystals.
    play = AT_MAX_MANA(CONTROLLER) & Give(CONTROLLER, "CS2_013t") | GainEmptyMana(
        CONTROLLER, 2
    )


class BT_132:
    """Ironbark"""

    # Give a minion +1/+3 and <b>Taunt</b>. Costs (0) if you have at least 7
    # Mana Crystals.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(TARGET, "BT_132e")

    class Hand:
        update = (MANA(CONTROLLER) >= 7) & Refresh(SELF, {GameTag.COST: SET(0)})


BT_132e = buff(atk=1, health=3, taunt=True)


class BT_134:
    """Bogbeam"""

    # Deal $3 damage to_a minion. Costs (0) if you have at least 7 Mana
    # Crystals.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 3)

    class Hand:
        update = (MANA(CONTROLLER) >= 7) & Refresh(SELF, {GameTag.COST: SET(0)})


class BT_135:
    """Glowfly Swarm"""

    # Summon a 2/2 Glowfly for each spell in your_hand.
    play = Summon(CONTROLLER, "BT_135t") * Count(FRIENDLY_HAND + SPELL)
