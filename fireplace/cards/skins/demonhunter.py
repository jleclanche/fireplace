from ..utils import *


##
# Hero Powers


class HERO_10bp:
    """Demon Claws"""

    activate = Buff(FRIENDLY_HERO, "HERO_10bpe")


HERO_10bpe = buff(atk=1)


class HERO_10bbp(HERO_10bp):
    """ "Demon Claws (Aranna Starseeker)"""

    pass


##
# Upgraded Hero Powers


class HERO_10bp2:
    """Demon's Bite"""

    activate = Buff(FRIENDLY_HERO, "HERO_10pe2")


HERO_10pe2 = buff(atk=2)


class HERO_10bbp2(HERO_10bp2):
    """ "Demon's Bite (Aranna Starseeker)"""

    pass
