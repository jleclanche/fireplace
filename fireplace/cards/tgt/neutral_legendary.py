from ..utils import *


##
# Minions


class AT_070:
    """Skycap'n Kragg"""

    cost_mod = -Count(FRIENDLY_MINIONS + PIRATE)


class AT_122:
    """Gormok the Impaler"""

    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE_AND_MINIMUM_FRIENDLY_MINIONS: 4}
    play = (Count(FRIENDLY_MINIONS) >= 4) & Hit(TARGET, 4)


class AT_123:
    """Chillmaw"""

    deathrattle = HOLDING_DRAGON & Hit(ALL_MINIONS, 3)


class AT_124:
    """Bolf Ramshield"""

    events = Predamage(FRIENDLY_HERO).on(
        Predamage(FRIENDLY_HERO, 0), Hit(SELF, Predamage.AMOUNT)
    )


class AT_125:
    """Icehowl"""

    tags = {GameTag.CANNOT_ATTACK_HEROES: True}


class AT_127:
    """Nexus-Champion Saraad"""

    inspire = Give(CONTROLLER, RandomSpell())


class AT_128:
    """The Skeleton Knight"""

    deathrattle = JOUST & Bounce(SELF)


class AT_129:
    """Fjola Lightbane"""

    events = Play(CONTROLLER, SPELL, SELF).on(GiveDivineShield(SELF))


class AT_131:
    """Eydis Darkbane"""

    events = Play(CONTROLLER, SPELL, SELF).on(Hit(RANDOM_ENEMY_CHARACTER, 3))


class AT_132:
    """Justicar Trueheart"""

    play = UPGRADE_HERO_POWER
