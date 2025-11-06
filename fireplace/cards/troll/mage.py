from ..utils import *


##
# Minions


class TRL_311:
    """Arcanosaur"""

    # <b>Battlecry:</b> If you played an_Elemental last turn, deal_3_damage_to_all other
    # minions.
    powered_up = ELEMENTAL_PLAYED_LAST_TURN
    play = powered_up & Hit(ALL_MINIONS - SELF, 3)


class TRL_315:
    """Pyromaniac"""

    # Whenever your Hero Power_kills a minion, draw a card.
    events = Activate(CONTROLLER, FRIENDLY_HERO_POWER).after(
        Dead(Activate.TARGET) & Draw(CONTROLLER)
    )


class TRL_316(ThresholdUtils):
    """Jan'alai, the Dragonhawk"""

    # [x]<b>Battlecry:</b> If your Hero Power dealt 8 damage this game, summon Ragnaros the
    # Firelord.@ <i>({0} left!)</i>@ <i>(Ready!)</i>
    play = ThresholdUtils.powered_up & Summon(CONTROLLER, "TRL_316t")


class TRL_316t:
    """Ragnaros the Firelord"""

    # Can't attack. At the end of your turn, deal 8 damage to a random enemy.
    events = OWN_TURN_END.on(Hit(RANDOM_ENEMY_CHARACTER, 8))


class TRL_318:
    """Hex Lord Malacrass"""

    # <b>Battlecry</b>: Add a copy of your opening hand to your hand <i>(except this
    # card)</i>.
    play = Give(CONTROLLER, Copy(STARTING_HAND - SELF))


class TRL_319:
    """Spirit of the Dragonhawk"""

    # [x]<b>Stealth</b> for 1 turn. Your Hero Power also targets adjacent minions.
    events = OWN_TURN_BEGIN.on(Unstealth(SELF))
    update = Refresh(CONTROLLER, buff="TRL_319e")


class TRL_319e:
    events = Activate(CONTROLLER, FRIENDLY_HERO_POWER).on(
        PlayHeroPower(FRIENDLY_HERO_POWER, ADJACENT(Activate.TARGET))
    )


class TRL_390:
    """Daring Fire-Eater"""

    # <b>Battlecry:</b> Your next Hero Power this turn deals 2_more damage.
    play = Buff(CONTROLLER, "TRL_390e")


class TRL_390e:
    update = Refresh(CONTROLLER, {GameTag.HEROPOWER_DAMAGE: 2})
    events = Activate(CONTROLLER, FRIENDLY_HERO_POWER).after(Destroy(SELF))


##
# Spells


class TRL_310:
    """Elemental Evocation"""

    # The next Elemental you_play this turn costs (2) less.
    play = Buff(CONTROLLER, "TRL_310e")


class TRL_310e:
    update = Refresh(FRIENDLY_HAND + ELEMENTAL, {GameTag.COST: -2})
    events = Play(CONTROLLER, ELEMENTAL).on(Destroy(SELF))


class TRL_313:
    """Scorch"""

    # [x]Deal $4 damage to a minion. Costs (1) if you played an Elemental last turn.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    cost_mod = ELEMENTAL_PLAYED_LAST_TURN & -1
    play = Hit(TARGET, 4)


class TRL_317:
    """Blast Wave"""

    # Deal $2 damage to_all minions. <b>Overkill</b>: Add a random Mage spell to your hand.
    play = Hit(ALL_MINIONS, 2)
    overkill = Give(CONTROLLER, RandomSpell(card_class=CardClass.MAGE))


class TRL_400:
    """Splitting Image"""

    # <b>Secret:</b> When one of your minions is attacked, summon a copy of it.
    secret = Attack(None, FRIENDLY_MINIONS).on(
        FULL_BOARD | (Reveal(SELF), Summon(CONTROLLER, ExactCopy(Attack.DEFENDER)))
    )
