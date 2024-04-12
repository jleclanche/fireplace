from ..utils import *


##
# Minions


class TRL_059:
    """Bog Slosher"""

    # <b>Battlecry:</b> Return a friendly minion to your hand and give it +2/+2.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }
    play = Bounce(TARGET), Buff(TARGET, "TRL_059e")


TRL_059e = buff(+2, +2)


class TRL_060:
    """Spirit of the Frog"""

    # [x]<b>Stealth</b> for 1 turn. Whenever you cast a spell, draw a spell from your deck
    # that costs (1) more.
    events = (
        OWN_TURN_BEGIN.on(Unstealth(SELF)),
        Play(CONTROLLER, SPELL).on(
            ForceDraw(
                RANDOM(FRIENDLY_DECK + SPELL + (COST == (COST(Play.CARD) + Number(1))))
            )
        ),
    )


class TRL_085:
    """Zentimo"""

    # [x]Whenever you target a minion with a spell, cast it again on its neighbors.
    events = Play(CONTROLLER, SPELL, MINION).on(
        CastSpell(Play.CARD, ADJACENT(Play.TARGET))
    )


class TRL_345:
    """Krag'wa, the Frog"""

    # <b>Battlecry:</b> Return all spells you played last turn to_your hand.
    play = Give(CONTROLLER, Copy(CARDS_PLAYED_LAST_TURN + SPELL))


class TRL_522:
    """Wartbringer"""

    # <b>Battlecry:</b> If you played 2_spells this turn, deal 2_damage.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE_AND_MINIMUM_SPELLS_PLAYED_THIS_TURN: 2,
    }
    powered_up = Count(CARDS_PLAYED_THIS_TURN + SPELL) >= 2
    play = powered_up & Hit(TARGET, 2)


##
# Spells


class TRL_012:
    """Totemic Smash"""

    # Deal $2 damage. <b>Overkill</b>: Summon a basic Totem.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Hit(TARGET, 2)
    overkill = Summon(CONTROLLER, RandomBasicTotem())


class TRL_058:
    """Haunting Visions"""

    # The next spell you cast this turn costs (3) less. <b>Discover</b> a spell.
    play = (Buff(CONTROLLER, "TRL_058e"), DISCOVER(RandomSpell()))


class TRL_058e:
    update = Refresh(FRIENDLY_HAND + SPELL, {GameTag.COST: -3})
    events = Play(CONTROLLER, SPELL).on(Destroy(SELF))


class TRL_082:
    """Big Bad Voodoo"""

    # Give a friendly minion "<b>Deathrattle:</b> Summon a random minion that costs (1)
    # more."
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }
    play = Buff(TARGET, "TRL_082e")


class TRL_082e:
    tags = {GameTag.DEATHRATTLE: True}
    deathrattle = Summon(CONTROLLER, RandomMinion(cost=COST(OWNER) + Number(1)))


class TRL_351:
    """Rain of Toads"""

    # Summon three 2/4 Toads with <b>Taunt</b>. <b>Overload:</b> (3)
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, "TRL_351t") * 3


##
# Weapons


class TRL_352:
    """Likkim"""

    # Has +2 Attack while you have <b>Overloaded</b> Mana Crystals.
    update = OVERLOADED(CONTROLLER) & Refresh(SELF, {GameTag.ATK: 2})
