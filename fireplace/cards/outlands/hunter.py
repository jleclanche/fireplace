from ..utils import *


##
# Minions


class BT_201:
    """Augmented Porcupine"""

    # [x]<b>Deathrattle</b>: Deal this minion's Attack damage randomly split
    # among all enemies.
    deathrattle = Hit(RANDOM_ENEMY_CHARACTER, 1) * ATK(SELF)


class BT_202:
    """Helboar"""

    # <b>Deathrattle:</b> Give a random Beast in your hand +1/+1.
    deathrattle = Buff(RANDOM(FRIENDLY_HAND + BEAST), "BT_202e")


BT_202e = buff(+1, +1)


class BT_210:
    """Zixor, Apex Predator"""

    # [x]<b>Rush</b> <b>Deathrattle:</b> Shuffle 'Zixor Prime' into your deck.
    deathrattle = Shuffle(CONTROLLER, "BT_210t")


class BT_210t:
    """Zixor Prime"""

    # [x]<b>Rush</b> <b>Battlecry:</b> Summon 3 copies of this minion.
    play = Summon(CONTROLLER, ExactCopy(SELF)) * 3


class BT_211:
    """Imprisoned Felmaw"""

    # [x]<b>Dormant</b> for 2 turns. When this awakens, __attack a random
    # enemy.
    tags = {GameTag.DORMANT: True}
    dormant_turns = 2
    awaken = Attack(SELF, RANDOM_ENEMY_CHARACTER)


class BT_212:
    """Mok'Nathal Lion"""

    # <b>Rush</b>. <b>Battlecry:</b> Choose a friendly minion. Gain a copy of
    # its <b>Deathrattle</b>.
    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_TARGET_WITH_DEATHRATTLE: 0,
    }
    play = CopyDeathrattleBuff(TARGET, "BT_212e")


class BT_214:
    """Beastmaster Leoroxx"""

    # <b>Battlecry:</b> Summon 3 Beasts from your hand.
    play = Summon(CONTROLLER, RANDOM(FRIENDLY_HAND + BEAST) * 3)


##
# Spells


class BT_163:
    """Nagrand Slam"""

    # Summon four 3/5 Clefthoofs that attack random enemies.
    play = (
        Summon(CONTROLLER, "BT_163t").then(Attack(Summon.CARD, RANDOM_ENEMY_CHARACTER))
        * 4
    )


class BT_203:
    """Pack Tactics"""

    # <b>Secret:</b> When a friendly minion is attacked, summon a 3/3 copy.
    secret = Attack(None, FRIENDLY_MINIONS).on(
        FULL_BOARD
        | (
            Reveal(SELF),
            Summon(CONTROLLER, ExactCopy(Attack.DEFENDER)).then(
                Buff(Summon.CARD, "BT_203e")
            ),
        )
    )


class BT_203e:
    atk = SET(3)
    max_health = SET(3)


class BT_205:
    """Scrap Shot"""

    # Deal $3 damage. Give a random Beast in_your hand +3/+3.
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 3), Buff(RANDOM(FRIENDLY_HAND + BEAST), "BT_205e")


BT_205e = buff(+3, +3)


class BT_213:
    """Scavenger's Ingenuity"""

    # Draw a Beast. Give it +2/+2.
    play = ForceDraw(RANDOM(FRIENDLY_DECK + BEAST)).then(
        Buff(ForceDraw.TARGET, "BT_213e")
    )


BT_213e = buff(+2, +2)
