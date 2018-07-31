from ..utils import *


##
# Minions

class CFM_691:
    """Jade Swarmer"""
    deathrattle = SummonJadeGolem(CONTROLLER)


##
# Spells

class CFM_690:
    """Jade Shuriken"""
    play = Hit(TARGET, 2)
    combo = Hit(TARGET, 2), SummonJadeGolem(CONTROLLER)
