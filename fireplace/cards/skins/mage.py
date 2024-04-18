from ..utils import *


##
# Hero Powers


class HERO_08bp:
    """Fireblast (Jaina Proudmoore)"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    activate = Hit(TARGET, 1)


class CS2_034_H1(HERO_08bp):
    """Fireblast (Medivh)"""

    pass


class CS2_034_H2(HERO_08bp):
    """Fireblast (Khadgar)"""

    pass


class HERO_08ebp(HERO_08bp):
    """Fireblast (Kel'Thuzad)"""

    pass


##
# Upgraded Hero Powers


class HERO_08bp2:
    """Fireblast Rank 2"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    activate = Hit(TARGET, 2)


class CS2_034_H1_AT_132(HERO_08bp2):
    """Fireblast Rank 2 (Medivh)"""

    pass


class CS2_034_H2_AT_132(HERO_08bp2):
    """Fireblast Rank 2 (Khadgar)"""

    pass


class HERO_08ebp2(HERO_08bp2):
    """Fireblast Rank 2 (Kel'Thuzad)"""

    pass
