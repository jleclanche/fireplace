from ..utils import *


##
# Minions


class BT_004:
    """Imprisoned Observer"""

    # <b>Dormant</b> for 2 turns. When this awakens, deal 2 damage to all enemy
    # minions.
    tags = {GameTag.DORMANT: True}
    dormant_turns = 2
    awaken = Hit(ENEMY_MINIONS, 2)


class BT_014:
    """Starscryer"""

    # <b>Deathrattle:</b> Draw a spell.
    deathrattle = ForceDraw(RANDOM(FRIENDLY_DECK + SPELL))


class BT_022:
    """Apexis Smuggler"""

    # After you play a <b>Secret</b>, <b>Discover</b> a spell.
    events = Play(CONTROLLER, SECRET).after(DISCOVER(RandomSpell()))


class BT_028:
    """Astromancer Solarian"""

    # [x]<b>Spell Damage +1</b> <b>Deathrattle:</b> Shuffle 'Solarian Prime'
    # into your deck.
    deathrattle = Shuffle(CONTROLLER, "BT_028t")


class BT_028t:
    """Solarian Prime"""

    # <b>Spell Damage +1</b> <b>Battlecry:</b> Cast 5 random Mage spells
    # <i>(targets enemies if possible)</i>.
    play = CastSpellTargetsEnemiesIfPossible(RandomSpell(card_class=CardClass.MAGE) * 5)


##
# Spells


class BT_002:
    """Incanter's Flow"""

    # Reduce the Cost of spells in your deck by_(1).
    play = Buff(FRIENDLY_DECK + SPELL, "BT_002e")


class BT_002e:
    tags = {GameTag.COST: -1}
    events = REMOVED_IN_PLAY


class BT_003:
    """Netherwind Portal"""

    # <b>Secret:</b> After your opponent casts a spell, summon a random 4-Cost
    # minion.
    secret = Play(OPPONENT, SPELL).after(
        FULL_BOARD | (Reveal(SELF), Summon(CONTROLLER, RandomMinion(cost=4)))
    )


class BT_006:
    """Evocation"""

    # Fill your hand with random Mage spells. At the end of your turn, discard
    # them.
    play = Give(CONTROLLER, RandomSpell(card_class=CardClass.MAGE)).then(
        Buff(Give.CARD, "BT_006e")
    ) * (MAX_HAND_SIZE(CONTROLLER) - Count(FRIENDLY_HAND))


class BT_006e:
    class Hand:
        events = OWN_TURN_END.on(Destroy(OWNER))

    events = REMOVED_IN_PLAY


class BT_021:
    """Font of Power"""

    # <b>Discover</b> a Mage minion. If your deck has no minions, keep all 3.
    powered_up = -Find(FRIENDLY_DECK + MINION)
    play = powered_up & (
        Give(CONTROLLER, RandomMinion(card_class=CardClass.MAGE) * 3)
    ) | (DISCOVER(RandomMinion(card_class=CardClass.MAGE)))


class BT_072:
    """Deep Freeze"""

    # <b>Freeze</b> an enemy. Summon two 3/6 Water Elementals.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
    }
    play = Freeze(TARGET), Summon(CONTROLLER, "CS2_033") * 2


class BT_291:
    """Apexis Blast"""

    # Deal $5 damage. If your deck has no minions, summon a random 5-Cost
    # minion.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    powered_up = -Find(FRIENDLY_DECK + MINION)
    play = Hit(TARGET, 5), powered_up & Summon(CONTROLLER, RandomMinion(cost=5))
