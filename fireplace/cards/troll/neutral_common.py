from ..utils import *


##
# Minions


class TRL_010:
    """Half-Time Scavenger"""

    # <b>Stealth</b> <b>Overkill</b>: Gain 3 Armor.
    overkill = GainArmor(FRIENDLY_HERO, 3)


class TRL_015:
    """Ticket Scalper"""

    # <b>Overkill</b>: Draw 2 cards.
    overkill = Draw(CONTROLLER) * 2


class TRL_020:
    """Sightless Ranger"""

    # <b>Rush</b> <b>Overkill</b>: Summon two 1/1_Bats.
    overkill = SummonBothSides(CONTROLLER, "TRL_020t") * 2


class TRL_151:
    """Former Champ"""

    # <b>Battlecry:</b> Summon a 5/5_Hotshot.
    play = Summon(CONTROLLER, "TRL_151t")


class TRL_312:
    """Spellzerker"""

    # Has <b>Spell Damage +2</b> while damaged.
    enrage = Refresh(SELF, buff="TRL_312e")


TRL_312e = buff(spellpower=2)


class TRL_363:
    """Saronite Taskmaster"""

    # <b>Deathrattle:</b> Summon a 0/3 Free Agent with <b>Taunt</b> for_your opponent.
    deathrattle = Summon(OPPONENT, "TRL_363t")


class TRL_406:
    """Dozing Marksman"""

    # Has +4 Attack while damaged.
    enrage = Refresh(SELF, buff="TRL_406e")


TRL_406e = buff(atk=+4)


class TRL_503:
    """Scarab Egg"""

    # <b>Deathrattle:</b> Summon three 1/1 Scarabs.
    deathrattle = Summon(CONTROLLER, "TRL_503t") * 3


class TRL_505:
    """Helpless Hatchling"""

    # <b>Deathrattle:</b> Reduce the Cost of a Beast in your hand by (1).
    deathrattle = Buff(RANDOM(FRIENDLY_HAND + BEAST), "TRL_505e")


class TRL_505e:
    events = REMOVED_IN_PLAY
    tags = {GameTag.COST: -1}


class TRL_506:
    """Gurubashi Chicken"""

    # <b>Overkill:</b> Gain +5 Attack.
    overkill = Buff(SELF, "TRL_506e")


TRL_506e = buff(atk=5)


class TRL_507:
    """Sharkfin Fan"""

    # After your hero attacks, summon a 1/1 Pirate.
    events = Attack(FRIENDLY_HERO).after(Summon(CONTROLLER, "TRL_507t"))


class TRL_508:
    """Regeneratin' Thug"""

    # At the start of your turn, restore #2 Health to this_minion.
    events = OWN_TURN_BEGIN.on(Heal(SELF, 2))


class TRL_509:
    """Banana Buffoon"""

    # <b>Battlecry:</b> Add 2 Bananas to your hand.
    play = Give(CONTROLLER, "TRL_509t") * 2


class TRL_509t:
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(TARGET, "TRL_509te")


TRL_509te = buff(+1, +1)


class TRL_512:
    """Cheaty Anklebiter"""

    # <b>Lifesteal</b> <b>Battlecry:</b> Deal 1 damage.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = Hit(TARGET, 1)


class TRL_515:
    """Rabble Bouncer"""

    # <b>Taunt</b> Costs (1) less for each enemy minion.
    cost_mod = -Count(ENEMY_MINIONS)


class TRL_517:
    """Arena Fanatic"""

    # <b>Battlecry:</b> Give all minions in your hand +1/+1.
    play = Buff(FRIENDLY_HAND + MINION, "TRL_517e2")


TRL_517e2 = buff(+1, +1)


class TRL_525:
    """Arena Treasure Chest"""

    # <b>Deathrattle:</b> Draw 2 cards.
    deathrattle = Draw(CONTROLLER) * 2


class TRL_526:
    """Dragonmaw Scorcher"""

    # <b>Battlecry:</b> Deal 1 damage to all other minions.
    play = Hit(ALL_MINIONS - SELF, 1)


class TRL_531:
    """Rumbletusk Shaker"""

    # <b>Deathrattle:</b> Summon a 3/2 Rumbletusk Breaker.
    deathrattle = Summon(CONTROLLER, "TRL_531t")


class TRL_546:
    """Ornery Tortoise"""

    # <b>Battlecry:</b> Deal 5 damage to your hero.
    play = Hit(FRIENDLY_HERO, 5)
