from ..utils import *


##
# Hero Powers


class HERO_03bp:
    """Dagger Mastery"""

    activate = Summon(CONTROLLER, "CS2_082")


class CS2_083b_H1(HERO_03bp):
    """Dagger Mastery (Maiev Shadowsong)"""

    pass


##
# Upgraded Hero Powers


class HERO_03bp2:
    """Poisoned Daggers"""

    activate = Summon(CONTROLLER, "AT_132_ROGUEt")


class AT_132_ROGUE_H1(HERO_03bp2):
    """Poisoned Daggers (Maiev Shadowsong)"""

    pass
