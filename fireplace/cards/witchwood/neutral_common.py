from ..utils import *


##
# Minions


class GIL_118:
    """Deranged Doctor"""

    # <b>Deathrattle:</b> Restore 8 Health to your hero.
    deathrattle = Heal(FRIENDLY_HERO, 8)


class GIL_119:
    """Cauldron Elemental"""

    # Your other Elementals have +2 Attack.
    update = Refresh(FRIENDLY_MINIONS - SELF + ELEMENTAL, buff="GIL_119e")


GIL_119e = buff(atk=2)


class GIL_201:
    """Pumpkin Peasant"""

    # [x]<b>Lifesteal</b> Each turn this is in your hand, swap its Attack and Health.
    class Hand:
        events = OWN_TURN_BEGIN.on(Morph(SELF, Buff("GIL_201t", "GIL_200e")))


class GIL_201t:
    """Pumpkin Peasant"""

    # [x]<b>Lifesteal</b> Each turn this is in your hand, swap its Attack and Health.
    class Hand:
        events = OWN_TURN_BEGIN.on(Morph(SELF, Buff("GIL_201", "GIL_200e")))


class GIL_212:
    """Ravencaller"""

    # [x]<b>Battlecry:</b> Add two random 1-Cost minions to your hand.
    play = Give(CONTROLLER, RandomMinion(cost=1)) * 2


class GIL_213:
    """Tanglefur Mystic"""

    # <b>Battlecry:</b> Add a random 2-Cost minion to each player's hand.
    play = Give(PLAYER, RandomMinion(cost=2))


class GIL_513:
    """Lost Spirit"""

    # <b>Deathrattle:</b> Give your minions +1 Attack.
    deathrattle = Buff(FRIENDLY_MINIONS, "GIL_513e")


GIL_513e = buff(atk=1)


class GIL_526:
    """Wyrmguard"""

    # <b>Battlecry:</b> If you're holding a Dragon, gain +1 Attack and <b>Taunt</b>.
    powered_up = HOLDING_DRAGON
    play = powered_up & Buff(SELF, "GIL_526e")


GIL_526e = buff(atk=1, taunt=True)


class GIL_528:
    """Swift Messenger"""

    # [x]<b>Rush</b> Each turn this is in your hand, swap its Attack and Health.
    class Hand:
        events = OWN_TURN_BEGIN.on(Morph(SELF, Buff("GIL_528t", "GIL_200e")))


class GIL_528t:
    """Swift Messenger"""

    # [x]<b>Rush</b> Each turn this is in your hand, swap its Attack and Health.
    class Hand:
        events = OWN_TURN_BEGIN.on(Morph(SELF, Buff("GIL_528", "GIL_200e")))


class GIL_529:
    """Spellshifter"""

    # [x]<b>Spell Damage +1</b> Each turn this is in your hand, swap its Attack and Health.
    class Hand:
        events = OWN_TURN_BEGIN.on(Morph(SELF, Buff("GIL_529t", "GIL_200e")))


class GIL_529t:
    """Spellshifter"""

    # [x]<b>Spell Damage +1</b> Each turn this is in your hand, swap its Attack and Health.
    class Hand:
        events = OWN_TURN_BEGIN.on(Morph(SELF, Buff("GIL_529", "GIL_200e")))


class GIL_534:
    """Hench-Clan Thug"""

    # After your hero attacks, give this minion +1/+1.
    events = Attack(FRIENDLY_HERO).after(Buff(SELF, "GIL_534t"))


GIL_534t = buff(+1, +1)


class GIL_561:
    """Blackwald Pixie"""

    # <b>Battlecry:</b> Refresh your Hero Power.
    play = RefreshHeroPower(FRIENDLY_HERO_POWER)


class GIL_646:
    """Clockwork Automaton"""

    # Double the damage and_healing of your Hero_Power.
    update = Refresh(
        CONTROLLER,
        {
            GameTag.HERO_POWER_DOUBLE: 1,
        },
    )


class GIL_667:
    """Rotten Applebaum"""

    # <b>Taunt</b> <b>Deathrattle:</b> Restore 4 Health to your hero.
    deathrattle = Heal(FRIENDLY_HERO, 4)


class GIL_683:
    """Marsh Drake"""

    # <b>Battlecry:</b> Summon a 2/1 <b>Poisonous</b> Drakeslayer for your opponent.
    play = Summon(OPPONENT, "GIL_683t")


class GIL_816:
    """Swamp Dragon Egg"""

    # <b>Deathrattle:</b> Add a random Dragon to your hand.
    deathrattle = Give(CONTROLLER, RandomDragon())
