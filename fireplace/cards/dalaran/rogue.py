from ..utils import *


##
# Minions


class DAL_415:
    """EVIL Miscreant"""

    # <b>Combo:</b> Add two random <b>Lackeys</b> to your hand.
    combo = Give(CONTROLLER, RandomLackey()) * 2


class DAL_416:
    """Hench-Clan Burglar"""

    # <b>Battlecry:</b> <b>Discover</b> a spell from another class.
    play = GenericChoice(CONTROLLER, RandomSpell(card_class=ANOTHER_CLASS) * 3)


class DAL_417:
    """Heistbaron Togwaggle"""

    # <b>Battlecry:</b> If you control a_<b>Lackey</b>, choose a fantastic treasure.
    powered_up = Find(FRIENDLY_MINIONS + LACKEY)
    play = powered_up & GenericChoice(
        CONTROLLER, ["LOOT_998h", "LOOT_998j", "LOOT_998l", "LOOT_998k"]
    )


class DAL_714:
    """Underbelly Fence"""

    # [x]<b>Battlecry:</b> If you're holding a card from another class, _gain +1/+1 and
    # <b><b>Rush</b>.</b>
    powered_up = Find(FRIENDLY_HAND + ANOTHER_CLASS)
    play = powered_up & Buff(SELF, "DAL_714e")


DAL_714e = buff(+1, +1, rush=True)


class DAL_719:
    """Tak Nozwhisker"""

    # [x]Whenever you shuffle a card into your deck, add a copy to your hand.
    events = Shuffle(CONTROLLER, source=FRIENDLY).after(
        Give(CONTROLLER, Copy(Shuffle.CARD))
    )


##
# Spells


class DAL_010:
    """Togwaggle's Scheme"""

    # Choose a minion. Shuffle @ |4(copy, copies) of it into your deck. <i>(Upgrades each
    # turn!)</i>
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Shuffle(CONTROLLER, Copy(TARGET)) * (
        Attr(SELF, GameTag.QUEST_PROGRESS) + Number(1)
    )

    class Hand:
        events = OWN_TURN_BEGIN.on(AddProgress(SELF, SELF))


class DAL_366:
    """Unidentified Contract"""

    # Destroy a minion. Gains a bonus effect in_your hand.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    entourage = ["DAL_366t1", "DAL_366t2", "DAL_366t3", "DAL_366t4"]
    play = Destroy(TARGET)
    draw = Morph(SELF, RandomEntourage())


class DAL_366t1:
    """Assassin's Contract"""

    # Destroy a minion. Summon a 1/1 Patient Assassin.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Destroy(TARGET), Summon(CONTROLLER, "EX1_522")


class DAL_366t2:
    """Recruitment Contract"""

    # Destroy a minion. Add_a copy of it to your hand.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Destroy(TARGET), Give(CONTROLLER, Copy(TARGET))


class DAL_366t3:
    """Lucrative Contract"""

    # Destroy a minion. Add 2 Coins to your hand.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Destroy(TARGET), Give(CONTROLLER, THE_COIN) * 2


class DAL_366t4:
    """Turncoat Contract"""

    # Destroy a minion. It_deals its damage to adjacent minions.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(SELF_ADJACENT, ATK(SELF), source=TARGET), Destroy(TARGET)


class DAL_716:
    """Vendetta"""

    # Deal $4 damage to a minion. Costs (0) if you're holding a card from another class.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 4)

    class Hand:
        update = Find(FRIENDLY_HAND + ANOTHER_CLASS) & Refresh(
            SELF, {GameTag.COST: SET(0)}
        )


class DAL_728:
    """Daring Escape"""

    # Return all friendly minions to your hand.
    play = Bounce(FRIENDLY_MINIONS)


##
# Weapons


class DAL_720:
    """Waggle Pick"""

    # [x]<b>Deathrattle:</b> Return a random friendly minion to your hand. It costs (2)
    # less.
    deathrattle = Bounce(RANDOM_OTHER_FRIENDLY_MINION).then(
        Buff(Bounce.TARGET, "GBL_002e")
    )
