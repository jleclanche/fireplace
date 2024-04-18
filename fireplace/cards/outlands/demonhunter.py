from ..utils import *


##
# Minions


class BT_187:
    """Kayn Sunfury"""

    # <b>Charge</b> All friendly attacks ignore_<b>Taunt</b>.
    update = Refresh(FRIENDLY_MINIONS, {GameTag.IGNORE_TAUNT: True})


class BT_321:
    """Netherwalker"""

    # <b>Battlecry:</b> <b>Discover</b> a Demon.
    play = DISCOVER(RandomDemon())


class BT_480:
    """Crimson Sigil Runner"""

    # <b>Outcast:</b> Draw a card.
    outcast = Draw(CONTROLLER)


class BT_486:
    """Pit Commander"""

    # <b>Taunt</b> At the end of your turn, summon a Demon from your deck.
    events = OWN_TURN_END.on(Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + DEMON)))


class BT_493:
    """Priestess of Fury"""

    # At the end of your turn, deal 6 damage randomly split among all enemies.
    events = OWN_TURN_END.on(Hit(RANDOM_ENEMY_CHARACTER, 1) * 6)


class BT_496:
    """Furious Felfin"""

    # [x]<b>Battlecry:</b> If your hero attacked this turn, gain +1 Attack and
    # <b>Rush</b>.
    powered_up = NUM_ATTACKS_THIS_TURN(FRIENDLY_HERO) > 0
    play = powered_up & Buff(SELF, "BT_496e")


BT_496e = buff(atk=1, rush=True)


class BT_509:
    """Fel Summoner"""

    # <b>Deathrattle:</b> Summon a random Demon from your_hand.
    deathrattle = Summon(CONTROLLER, RANDOM(FRIENDLY_HAND + DEMON))


class BT_761:
    """Coilfang Warlord"""

    # [x]<b>Rush</b> <b>Deathrattle:</b> Summon a 5/9 Warlord with
    # <b>Taunt</b>.
    deathrattle = Summon(CONTROLLER, "BT_761t")


class BT_934:
    """Imprisoned Antaen"""

    # [x]<b>Dormant</b> for 2 turns. When this awakens, deal 10 damage randomly
    # split among all enemies.
    # TODO need test
    tags = {GameTag.DORMANT: True}
    dormant_turns = 2
    awaken = Hit(RANDOM_ENEMY_CHARACTER, 1) * 10


##
# Spells


class BT_429:
    """Metamorphosis"""

    # Swap your Hero Power to "Deal 4 damage." After 2 uses, swap it back.
    # TODO need test
    play = (
        SetAttribute(SELF, "store_card", FRIENDLY_HERO_POWER),
        Summon(CONTROLLER, "BT_429p").then(
            SetAttribute(Summon.CARD, "store_card", GetAttribute(SELF, "store_card"))
        ),
        DelAttribute(SELF, "store_card"),
    )


class BT_429p:
    """Demonic Blast"""

    # [x]<b>Hero Power</b> Deal $4 damage. <i>(Two uses left!)</i>
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    activate = (
        Hit(TARGET, 4),
        Summon(CONTROLLER, "BT_429p2").then(
            SetAttribute(Summon.CARD, "store_card", GetAttribute(SELF, "store_card"))
        ),
    )


class BT_429p2:
    """Demonic Blast"""

    # [x]<b>Hero Power</b> Deal $4 damage. <i>(Last use!)</i>
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    activate = Hit(TARGET, 4), Summon(CONTROLLER, ExactCopy(STORE_CARD))


class BT_491:
    """Spectral Sight"""

    # [x]Draw a card. <b>Outcast:</b> Draw another.
    play = Draw(CONTROLLER)
    outcast = Draw(CONTROLLER) * 2


class BT_514:
    """Immolation Aura"""

    # Deal $1 damage to all minions twice.
    play = Hit(ALL_MINIONS, 1) * 2


class BT_601:
    """Skull of Gul'dan"""

    # Draw 3 cards. <b>Outcast:</b> Reduce their Cost by (3).
    play = Draw(CONTROLLER) * 3
    outcast = Draw(CONTROLLER).then(Buff(Draw.CARD, "BT_601e")) * 3


class BT_601e:
    tags = {GameTag.COST: -3}
    events = REMOVED_IN_PLAY


##
# Weapons


class BT_430:
    """Warglaives of Azzinoth"""

    # After attacking a minion, your hero may attack again.
    events = Attack(FRIENDLY_HERO, MINION).after(ExtraAttack(FRIENDLY_HERO))
