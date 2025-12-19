from ..utils import *


##
# Hero Powers


class HERO_06bp:
    """Shapeshift"""

    activate = Buff(FRIENDLY_HERO, "CS2_017o"), GainArmor(FRIENDLY_HERO, 1)


CS2_017o = buff(atk=1)


class CS2_017_HS1(HERO_06bp):
    """Shapeshift (Lunara)"""

    pass


class CS2_017_HS2(HERO_06bp):
    """Shapeshift (Elise Starseeker)"""

    pass


class CS2_017_HS4(HERO_06bp):
    """Shapeshift (Dame Hazelbark)"""

    pass


##
# Upgraded Hero Powers


class HERO_06bp2:
    """Dire Shapeshift"""

    activate = Buff(FRIENDLY_HERO, "AT_132_DRUIDe"), GainArmor(FRIENDLY_HERO, 2)


AT_132_DRUIDe = buff(atk=2)


class AT_132_DRUIDa(HERO_06bp2):
    """Dire Shapeshift (Lunara)"""

    pass


class AT_132_DRUIDb(HERO_06bp2):
    """Dire Shapeshift (Elise Starseeker)"""

    pass


class AT_132_DRUIDc(HERO_06bp2):
    """Dire Shapeshift (Dame Hazelbark)"""

    pass
