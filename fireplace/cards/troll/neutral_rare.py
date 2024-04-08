from ..utils import *


##
# Minions


class TRL_057:
    """Serpent Ward"""

    # At the end of your turn, deal 2 damage to the enemy hero.
    events = OWN_TURN_END.on(Hit(ENEMY_HERO, 2))


class TRL_407:
    """Waterboy"""

    # <b>Battlecry:</b> Your next Hero Power this turn costs (0).
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(CONTROLLER, "TRL_407e")


class TRL_407e:
    update = Refresh(FRIENDLY_HERO_POWER, {GameTag.COST: SET(0)})
    events = Activate(CONTROLLER, HERO_POWER).on(Destroy(SELF))


class TRL_504:
    """Booty Bay Bookie"""

    # <b>Battlecry:</b> Give your opponent a Coin.
    play = Give(OPPONENT, THE_COIN)


class TRL_514:
    """Belligerent Gnome"""

    # [x]<b>Taunt</b> <b>Battlecry:</b> If your opponent has 2 or more minions, gain +1
    # Attack.
    play = (Count(ENEMY_MINIONS) >= 2) & Buff(SELF, "TRL_514e")


TRL_514e = buff(atk=1)


class TRL_520:
    """Murloc Tastyfin"""

    # [x]<b>Deathrattle:</b> Draw 2 Murlocs from your deck.
    deathrattle = ForceDraw(RANDOM(FRIENDLY_DECK + MURLOC)) * 2


class TRL_521:
    """Arena Patron"""

    # <b>Overkill:</b> Summon another Arena Patron.
    overkill = Summon(CONTROLLER, "TRL_521")


class TRL_523:
    """Firetree Witchdoctor"""

    # [x]<b>Battlecry:</b> If you're holding a Dragon, <b>Discover</b> a spell.
    powered_up = HOLDING_DRAGON
    play = powered_up & DISCOVER(RandomSpell())


class TRL_524:
    """Shieldbreaker"""

    # <b>Battlecry:</b> <b>Silence</b> an enemy minion with <b>Taunt</b>.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_MUST_TARGET_TAUNTER: 0,
    }
    play = Silence(TARGET)


class TRL_570:
    """Soup Vendor"""

    # Whenever you restore 3 or more Health to your hero, draw a card.
    events = Heal(FRIENDLY_HERO).on((Heal.AMOUNT >= 3) & Draw(CONTROLLER))
