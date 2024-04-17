from ..utils import *


##
# Minions


class BT_188:
    """Shadowjeweler Hanar"""

    # [x]After you play a <b>Secret</b>, <b>Discover</b> a <b>Secret</b> from a
    # different class.
    events = Play(CONTROLLER, SECRET).after(
        DISCOVER(RandomSpell(card_class=ANOTHER_CLASS, secret=True))
    )


class BT_702:
    """Ashtongue Slayer"""

    # <b>Battlecry:</b> Give a <b><b>Stealth</b>ed</b> minion +3 Attack and
    # <b>Immune</b> this turn.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_STEALTHED_TARGET: 0,
    }
    play = Buff(TARGET, "BT_702e")


BT_702e = buff(atk=3, immune=True)


class BT_703:
    """Cursed Vagrant"""

    # <b>Deathrattle:</b> Summon a 7/5 Shadow with <b>Stealth</b>.
    deathrattle = Summon(CONTROLLER, "BT_703t")


class BT_710:
    """Greyheart Sage"""

    # [x]<b>Battlecry:</b> If you control a <b><b>Stealth</b>ed</b> minion,
    # draw 2 cards.
    powered_up = Find(FRIENDLY_MINIONS + STEALTH)
    play = powered_up & Draw(CONTROLLER) * 2


class BT_711:
    """Blackjack Stunner"""

    # [x]<b>Battlecry:</b> If you control a <b>Secret</b>, return a minion to
    # its owner's hand. It costs (1) more.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE_AND_MINIMUM_FRIENDLY_SECRETS: 1,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    powered_up = Find(FRIENDLY_SECRETS)
    play = powered_up & (Bounce(TARGET), Buff(TARGET, "BT_711e"))


class BT_711e:
    tags = {GameTag.COST: +1}
    events = REMOVED_IN_PLAY


class BT_713:
    """Akama"""

    # [x]<b>Stealth</b> <b>Deathrattle:</b> Shuffle 'Akama Prime' into your
    # deck.
    deathrattle = Shuffle(CONTROLLER, "BT_713t")


class BT_713t:
    """Akama Prime"""

    # Permanently <b><b>Stealth</b>ed</b>.
    update = Refresh(SELF, {GameTag.STEALTH: True})


##
# Spells


class BT_042:
    """Bamboozle"""

    # [x]<b>Secret:</b> When one of your minions is attacked, transform it into
    # a random one that costs (3) more.
    secret = Attack(None, FRIENDLY_MINIONS).on(
        Reveal(SELF), Retarget(Attack.ATTACKER, Evolve(Attack.DEFENDER, 3))
    )


class BT_707:
    """Ambush"""

    # [x]<b>Secret:</b> After your opponent plays a minion, summon a 2/3
    # Ambusher with <b>Poisonous</b>.
    secret = Play(OPPONENT, MINION).after(
        FULL_BOARD | (Reveal(SELF), Summon(CONTROLLER, "BT_707t"))
    )


class BT_709:
    """Dirty Tricks"""

    # [x]<b>Secret:</b> After your opponent casts a spell, draw 2 cards.
    secret = Play(OPPONENT, SPELL).after(
        FULL_HAND | (Reveal(SELF), Draw(CONTROLLER) * 2)
    )
