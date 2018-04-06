from ..utils import *


class UNG_999t2:
	"Living Spores"
	play = Buff(TARGET, "UNG_999t2e")

class UNG_999t2e:
	tags = {GameTag.DEATHRATTLE: True}
	deathrattle = Summon(CONTROLLER, "UNG_999t2t1") * 2


class UNG_999t3:
	"Flaming Claws"
	play = Buff(TARGET, "UNG_999t3e")

UNG_999t3e = buff(atk=3)


class UNG_999t4:
	"Rocky Carapace"
	play = Buff(TARGET, "UNG_999t4e")

UNG_999t4e = buff(health=3)


class UNG_999t5:
	"Liquid Membrane"
	play = Buff(TARGET, "UNG_999t5e")

class UNG_999t5e:
	tags = {GameTag.CANT_BE_TARGETED: True}


class UNG_999t6:
	"Massive"
	play = Buff(TARGET, "UNG_999t6e")

class UNG_999t6e:
	play = Taunt(TARGET)


class UNG_999t7:
	"Lightning Speed"
	play = Buff(TARGET, "UNG_999t7e")

class UNG_999t7e:
	play = GiveWindfury(TARGET)


class UNG_999t8:
	"Crackling Shield"
	play = Buff(TARGET, "UNG_999t8e")

class UNG_999t8e:
	play = GiveDivineShield(TARGET)


class UNG_999t10:
	"Shrouding Mist"
	play = Buff(TARGET - STEALTH, "UNG_999t10e")

class UNG_999t10e:
	tags = {GameTag.STEALTH: True}
	events = OWN_TURN_BEGIN.on(Unstealth(OWNER), Destroy(SELF))


class UNG_999t13:
	"Poison Spit"
	play = Buff(TARGET, "UNG_999t13e")

class UNG_999t13e:
	play = GivePoisonous(TARGET)


class UNG_999t14:
	"Volcanic Might"
	play = Buff(TARGET, "UNG_999t14e")

UNG_999t14e = buff(+1, +1)
