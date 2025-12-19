from ..utils import *


##
# Minions


class BT_351:
    """Battlefiend"""

    # After your hero attacks, gain +1 Attack.
    events = Attack(FRIENDLY_HERO).after(Buff(CONTROLLER, "BT_351e"))


BT_351e = buff(atk=1)


class BT_355:
    """Wrathscale Naga"""

    # After a friendly minion dies, deal 3 damage to a_random enemy.
    events = Death(FRIENDLY + MINION).on(Hit(RANDOM_ENEMY_CHARACTER, 3))


class BT_407:
    """Ur'zul Horror"""

    # <b>Deathrattle:</b> Add a 2/1 Lost Soul to your hand.
    deathrattle = Give(CONTROLLER, "BT_407t")


class BT_416:
    """Raging Felscreamer"""

    # <b>Battlecry:</b> The next Demon you play costs (2) less.
    play = Buff(CONTROLLER, "BT_416e")


class BT_416e:
    update = Refresh(FRIENDLY_HAND + DEMON, {GameTag.COST: -2})
    events = Play(CONTROLLER, DEMON).on(Destroy(SELF))


class BT_481:
    """Nethrandamus"""

    # [x]<b>Battlecry:</b> Summon two random @-Cost minions. <i>(Upgrades each
    # time a friendly minion dies!)</i>
    class Hand:
        events = Death(FRIENDLY + MINION).on(AddProgress(SELF, Death.ENTITY))

    play = SummonBothSides(
        CONTROLLER, RandomMinion(cost=Min(Attr(SELF, GameTag.QUEST_PROGRESS), 10))
    )


class BT_487:
    """Hulking Overfiend"""

    # <b>Rush</b>. After this attacks and kills a minion, it may_attack again.
    events = Attack(SELF, ALL_MINIONS).after(Dead(Attack.DEFENDER) & ExtraAttack(SELF))


class BT_510:
    """Wrathspike Brute"""

    # [x]<b>Taunt</b> After this is attacked, deal 1 damage to all enemies.
    events = Attack(SELF).after(Hit(ENEMY_CHARACTERS, 1))


class BT_814:
    """Illidari Felblade"""

    # <b>Rush</b> <b>Outcast:</b> Gain <b>Immune</b> this_turn.
    outcast = Buff(SELF, "BT_814e")


BT_814e = buff(immune=True)


class BT_937:
    """Altruis the Outcast"""

    # [x]After you play the left- or right-most card in your hand, deal 1
    # damage to all enemies.
    events = Play(CONTROLLER, PLAY_OUTCAST).after(Hit(ENEMY_CHARACTERS, 1))


##
# Spells


class BT_173:
    """Command the Illidari"""

    # Summon six 1/1_Illidari with <b>Rush</b>.
    play = Summon(CONTROLLER, "BT_036t") * 6


class BT_175:
    """Twin Slice"""

    # Give your hero +2 Attack this turn. Add 'Second Slice' to your hand.
    play = Buff(FRIENDLY_HERO, "BT_175e"), Give(CONTROLLER, "BT_175t")


class BT_175t:
    """Second Slice"""

    # Give your hero +2_Attack this turn.
    play = Buff(FRIENDLY_HERO, "BT_175e")


BT_175e = buff(atk=2)


class BT_354:
    """Blade Dance"""

    # Deal damage equal to your hero's Attack to 3 random enemy minions.
    requirements = {PlayReq.REQ_MINIMUM_ENEMY_MINIONS: 1}
    play = Hit(RANDOM_ENEMY_MINION * 3, ATK(FRIENDLY_HERO))


class BT_427:
    """Feast of Souls"""

    # Draw a card for each friendly minion that died this turn.
    play = Draw(CONTROLLER) * Attr(CONTROLLER, GameTag.NUM_MINIONS_KILLED_THIS_TURN)


class BT_488:
    """Soul Split"""

    # Choose a friendly Demon. Summon a copy of it.
    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_TARGET_WITH_RACE: Race.DEMON,
    }
    play = Summon(CONTROLLER, ExactCopy(TARGET))


class BT_490:
    """Consume Magic"""

    # <b>Silence</b> an enemy_minion. <b>Outcast:</b> Draw a card.
    requirements = {
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Silence(TARGET)
    outcast = Silence(TARGET), Draw(CONTROLLER)


class BT_752:
    """Blur"""

    # Your hero can't take damage this turn.
    play = Buff(FRIENDLY_HERO, "BT_752e")


BT_752e = buff(immune=True)


class BT_753:
    """Mana Burn"""

    # Your opponent has 2 fewer Mana Crystals next turn.
    play = Buff(OPPONENT, "BT_753e")


class BT_753e:
    events = BeginTurn(OPPONENT).on(ManaThisTurn(OWNER, -2)), Destroy(SELF)


class BT_801:
    """Eye Beam"""

    # <b>Lifesteal</b>. Deal $3 damage to a minion. <b>Outcast:</b> This costs
    # (1).
    class Hand:
        update = Find(SELF + OUTERMOST_HAND) & Refresh(SELF, {GameTag.COST: SET(1)})

    play = Hit(TARGET, 3)


##
# Weapons


class BT_271:
    """Flamereaper"""

    # Also damages the minions next to whomever your hero_attacks.
    events = Attack(FRIENDLY_HERO).on(
        Hit(ADJACENT(Attack.DEFENDER), ATK(FRIENDLY_HERO))
    )


class BT_922:
    """Umberwing"""

    # <b>Battlecry:</b> Summon two 1/1 Felwings.
    play = Summon(CONTROLLER, "BT_922t") * 2
