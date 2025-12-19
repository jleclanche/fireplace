from ..utils import *


##
# Hero Powers


class HERO_01bp:
    """Armor Up! (Garrosh Hellscream)"""

    activate = GainArmor(FRIENDLY_HERO, 2)


class CS2_102_H1(HERO_01bp):
    """Armor Up! (Magni Bronzebeard)"""

    pass


class CS2_102_H3(HERO_01bp):
    """Armro Up! (Deathwing)"""

    pass


##
# Upgraded Hero Powers


class HERO_01bp2:
    """Tank Up!"""

    activate = GainArmor(FRIENDLY_HERO, 4)


class CS2_102_H1_AT_132(HERO_01bp2):
    """Tank Up! (Magni Bronzebeard)"""

    pass


class CS2_102_H3_AT_132(HERO_01bp2):
    """Tank Up! (Deathwing)"""

    pass
