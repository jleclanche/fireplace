from ..utils import *


##
# Minions

class CFM_312:
    """Jade Chieftain"""
    play = SummonJadeGolem(CONTROLLER).then(Taunt(SummonJadeGolem.CARD))


##
# Spells

class CFM_707:
    """Jade Lightning"""
    play = Hit(TARGET, 4), SummonJadeGolem(CONTROLLER)


##
# Weapons

class CFM_717:
    """Jade Claws"""
    play = SummonJadeGolem(CONTROLLER)
