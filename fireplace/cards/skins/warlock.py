from ..utils import *


##
# Hero Powers


class HERO_07bp:
    """Life Tap"""

    activate = Hit(FRIENDLY_HERO, 2), Draw(CONTROLLER)


class CS2_056_H1(HERO_07bp):
    """Life Tap (Nemsy Necrofizzle)"""

    pass


class CS2_056_H2(HERO_07bp):
    """Life Tap (Mecha-Jaraxxus)"""

    pass


##
# Upgraded Hero Powers


class HERO_07bp2:
    """Soul Tap"""

    activate = Draw(CONTROLLER)


class AT_132_WARLOCKa(HERO_07bp2):
    """Soul Tap (Nemsy Necrofizzle)"""

    pass


class AT_132_WARLOCKb(HERO_07bp2):
    """Soul Tap (Mecha-Jaraxxus)"""

    pass
