from ..utils import *


##
# Minions


class LOOT_048:
    """Ironwood Golem"""

    # <b>Taunt</b> Can only attack if you have 3 or more Armor.
    update = (ARMOR(FRIENDLY_HAND) >= 3) | Refresh(SELF, {GameTag.CANT_ATTACK: True})


class LOOT_056:
    """Astral Tiger"""

    # <b>Deathrattle:</b> Shuffle a copy of this minion into_your_deck.
    deathrattle = Shuffle(CONTROLLER, Copy(SELF))


class LOOT_314:
    """Grizzled Guardian"""

    # <b>Taunt</b> <b>Deathrattle:</b> <b>Recruit</b> 2_minions that cost (4)_or_less.
    deathrattle = Recruit(COST <= 4) * 2


class LOOT_329:
    """Ixlid, Fungal Lord"""

    # After you play a minion, summon a copy of it.
    events = Play(CONTROLLER, MINION).after(Summon(CONTROLLER, ExactCopy(Play.CARD)))


class LOOT_351:
    """Greedy Sprite"""

    # <b>Deathrattle:</b> Gain an empty Mana Crystal.
    deathrattle = GainEmptyMana(CONTROLLER, 1)


##
# Spells


class LOOT_047:
    """Barkskin"""

    # Give a minion +3 Health. Gain 3 Armor.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Buff(TARGET, "LOOT_047e"), GainArmor(FRIENDLY_HERO, 3)


LOOT_047e = buff(health=3)


class LOOT_051:
    """Lesser Jasper Spellstone"""

    # Deal $2 damage to a minion. @<i>(Gain 3 Armor to upgrade.)</i>
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    progress_total = 3
    play = Hit(TARGET, 2)
    reward = Morph(SELF, "LOOT_051t1")

    class Hand:
        events = GainArmor(FRIENDLY_HERO).on(
            AddProgress(SELF, GainArmor.TARGET, GainArmor.AMOUNT)
        )


class LOOT_051t1:
    """Jasper Spellstone"""

    # Deal $4 damage to a minion. @
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Hit(TARGET, 4)
    progress_total = 3
    reward = Morph(SELF, "LOOT_051t2")

    class Hand:
        events = GainArmor(FRIENDLY_HERO).on(
            AddProgress(SELF, GainArmor.TARGET, GainArmor.AMOUNT)
        )


class LOOT_051t2:
    """Greater Jasper Spellstone"""

    # Deal $6 damage to a minion.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Hit(TARGET, 6)


class LOOT_054:
    """Branching Paths"""

    # [x]<b>Choose Twice -</b> Draw a card; Give your minions +1 Attack; Gain 6 Armor.
    play = Choice(CONTROLLER, ["LOOT_054b", "LOOT_054c", "LOOT_054d"]).then(
        Battlecry(Choice.CARD, None),
        Choice(CONTROLLER, ["LOOT_054b", "LOOT_054c", "LOOT_054d"]).then(
            Battlecry(Choice.CARD, None),
        ),
    )


class LOOT_054b:
    """Explore the Darkness"""

    # Give your minions +1 Attack.
    play = Buff(FRIENDLY_MINIONS, "LOOT_054be")


LOOT_054be = buff(atk=1)


class LOOT_054c:
    """Loot the Chest"""

    # Gain 6 Armor.
    play = GainArmor(FRIENDLY_HERO, 6)


class LOOT_054d:
    """Eat the Mushroom"""

    # Draw a card.
    play = Draw(CONTROLLER)


class LOOT_309:
    """Oaken Summons"""

    # Gain 6 Armor. <b>Recruit</b> a minion that costs (4) or less.
    play = GainArmor(FRIENDLY_HERO, 6), Recruit(COST <= 4)


##
# Weapons


class LOOT_392:
    """Twig of the World Tree"""

    # <b>Deathrattle:</b> Gain 10 Mana Crystals.
    deathrattle = GainMana(CONTROLLER, 10)
