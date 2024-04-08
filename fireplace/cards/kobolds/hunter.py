from ..utils import *


##
# Minions


class LOOT_078:
    """Cave Hydra"""

    # Also damages the minions next to whomever this attacks.
    events = Attack(SELF).on(CLEAVE)


class LOOT_511:
    """Kathrena Winterwisp"""

    # <b>Battlecry and Deathrattle:</b> <b>Recruit</b> a Beast.
    play = deathrattle = Recruit(BEAST)


class LOOT_520:
    """Seeping Oozeling"""

    # <b>Battlecry:</b> Gain the <b>Deathrattle</b> of a random minion in your deck.
    play = (
        CopyDeathrattleBuff(RANDOM(FRIENDLY_DECK + MINION + DEATHRATTLE), "LOOT_520e"),
    )


##
# Spells


class LOOT_077:
    """Flanking Strike"""

    # Deal $3 damage to a minion. Summon a 3/3 Wolf.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 3), Summon(CONTROLLER, "LOOT_077t")


class LOOT_079:
    """Wandering Monster"""

    # <b>Secret:</b> When an enemy attacks your hero, summon a 3-Cost minion as the new
    # target.
    secret = Attack(ENEMY_MINIONS, FRIENDLY_HERO).on(
        Reveal(SELF),
        Retarget(Attack.ATTACKER, Summon(CONTROLLER, RandomMinion(cost=3))),
    )


class LOOT_080:
    """Lesser Emerald Spellstone"""

    # Summon two 3/3_Wolves. <i>(Play a <b>Secret</b> to upgrade.)</i>
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Summon(CONTROLLER, "LOOT_077t") * 2

    class Hand:
        events = Play(CONTROLLER, SECRET).after(Morph(SELF, "LOOT_080t2"))


class LOOT_080t2:
    """Emerald Spellstone"""

    # Summon three 3/3_Wolves. <i>(Play a <b>Secret</b> to upgrade.)</i>
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Summon(CONTROLLER, "LOOT_077t") * 3

    class Hand:
        events = Play(CONTROLLER, SECRET).after(Morph(SELF, "LOOT_080t3"))


class LOOT_080t3:
    """Greater Emerald Spellstone"""

    # Summon four 3/3_Wolves.
    play = Summon(CONTROLLER, "LOOT_077t") * 4


class LOOT_217:
    """To My Side!"""

    # [x]Summon an Animal Companion, or 2 if your deck has no minions.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    entourage = ["NEW1_032", "NEW1_033", "NEW1_034"]
    play = Find(FRIENDLY_DECK + MINION) & (Summon(CONTROLLER, RandomEntourage())) | (
        Summon(CONTROLLER, RandomEntourage() * 2)
    )


class LOOT_522:
    """Crushing Walls"""

    # Destroy your opponent's left and right-most minions.
    play = Destroy(ENEMY_MINIONS + (LEFTMOST_FIELD | RIGTHMOST_FIELD))


##
# Weapons


class LOOT_085:
    """Rhok'delar"""

    # <b>Battlecry:</b> If your deck has no minions, fill your_hand with Hunter_spells.
    play = Find(FRIENDLY_DECK + MINION) | (
        Give(CONTROLLER, RandomSpell(card_class=CardClass.HUNTER))
        * (MAX_HAND_SIZE(CONTROLLER) - Count(FRIENDLY_HAND))
    )


class LOOT_222:
    """Candleshot"""

    # Your hero is <b>Immune</b> while attacking.
    update = Refresh(FRIENDLY_HERO, {GameTag.IMMUNE_WHILE_ATTACKING: True})
