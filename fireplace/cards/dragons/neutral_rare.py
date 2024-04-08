from ..utils import *


##
# Minions


class DRG_055:
    """Hoard Pillager"""

    # <b>Battlecry:</b> Equip one of your destroyed weapons.
    play = Summon(CONTROLLER, Copy(RANDOM(FRIENDLY + KILLED + WEAPON)))


class DRG_063:
    """Dragonmaw Poacher"""

    # <b>Battlecry:</b> If your opponent controls a Dragon, gain +4/+4 and <b>Rush</b>.
    powered_up = Find(ENEMY_MINIONS + DRAGON)
    play = powered_up & Buff(SELF, "DRG_063e")


DRG_063e = buff(+4, +4, rush=True)


class DRG_064:
    """Zul'Drak Ritualist"""

    # [x]<b>Taunt</b> <b>Battlecry:</b> Summon three random 1-Cost minions for your
    # opponent.
    play = Summon(OPPONENT, RandomMinion(cost=1)) * 3


class DRG_070:
    """Dragon Breeder"""

    # <b>Battlecry:</b> Choose a friendly Dragon. Add a copy of it to_your hand.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_WITH_RACE: Race.DRAGON,
    }
    play = Give(CONTROLLER, Copy(TARGET))


class DRG_071:
    """Bad Luck Albatross"""

    # <b>Deathrattle:</b> Shuffle two 1/1 Albatross into your opponent's deck.
    deathrattle = Shuffle(OPPONENT, "DRG_071t") * 2


class DRG_075:
    """Cobalt Spellkin"""

    # <b>Battlecry:</b> Add two 1-Cost spells from your class to_your hand.
    play = Give(CONTROLLER, RandomSpell(cost=1, card_class=FRIENDLY_CLASS)) * 2


class DRG_076:
    """Faceless Corruptor"""

    # [x]<b>Rush</b>. <b>Battlecry:</b> Transform one of your minions into a copy of this.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Morph(TARGET, ExactCopy(SELF))


class DRG_077:
    """Utgarde Grapplesniper"""

    # <b>Battlecry:</b> Both players draw a card. If it's a Dragon, summon it.
    play = (
        Draw(CONTROLLER).then(Find(Draw.CARD + DRAGON) & Summon(CONTROLLER, Draw.CARD)),
        Draw(OPPONENT).then(Find(Draw.CARD + DRAGON) & Summon(OPPONENT, Draw.CARD)),
    )


class DRG_078:
    """Depth Charge"""

    # At the start of your turn, deal 5 damage to ALL_minions.
    events = OWN_TURN_BEGIN.on(Hit(ALL_MINIONS, 5))
