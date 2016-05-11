from ..utils import *


##
# Hero Powers

class TBA01_5:
	"Wild Magic"
	activate = Buff(Give(CONTROLLER, RandomSpell()), "TBA01_5e")

@custom_card
class TBA01_5e:
	tags = {
		GameTag.CARDNAME: "Wild Magic Buff",
		GameTag.CARDTYPE: CardType.ENCHANTMENT,
	}
	cost = SET(0)


class TBA01_6:
	"Molten Rage"
	activate = Summon(CONTROLLER, "CS2_118")


##
# Minions

class BRMC_84:
	"Dragonkin Spellcaster"
	play = Summon(CONTROLLER, "BRMA09_2Ht") * 2


class BRMC_85:
	"Lucifron"
	play = Buff(ALL_MINIONS - SELF, "CS2_063e")


class BRMC_86:
	"Atramedes"
	events = Play(OPPONENT).on(Buff(SELF, "BRMC_86e"))

BRMC_86e = buff(atk=2)

class BRMC_87:
	"Moira Bronzebeard"
	deathrattle = Summon(CONTROLLER, "BRM_028")


class BRMC_88:
	"Drakonid Slayer"
	events = Attack(SELF).on(CLEAVE)


class BRMC_91:
	"Son of the Flame"
	play = Hit(TARGET, 6)


class BRMC_92:
	"Coren Direbrew"
	play = Give(CONTROLLER, "EX1_407")
	tags = {
		enums.ALWAYS_WINS_BRAWLS: True,
	}


class BRMC_95:
	"Golemagg"
	cost_mod = -DAMAGE(FRIENDLY_HERO)


class BRMC_96:
	"High Justice Grimstone"
	events = OWN_TURN_BEGIN.on(Summon(CONTROLLER, RandomMinion(rarity=Rarity.LEGENDARY)))


class BRMC_97:
	"Vaelastrasz"
	update = Refresh(FRIENDLY_HAND, {GameTag.COST: -3})


# Burning Adrenaline (Unused)
BRMC_97e = buff(cost=-2)


class BRMC_98:
	"Razorgore"
	events = OWN_TURN_BEGIN.on(Buff(FRIENDLY_MINIONS, "BRMC_98e"))

BRMC_98e = buff(atk=3)


class BRMC_99:
	"Garr"
	events = SELF_DAMAGE.on(Summon(CONTROLLER, "BRMC_99e"))


##
# Spells

class BRMC_83:
	"Open the Gates"
	play = Summon(CONTROLLER, "BRMA09_2Ht") * 7


class BRMC_93:
	"Omnotron Defense System"
	play = Summon(CONTROLLER, RandomEntourage())


class BRMC_95h:
	"Core Hound Puppies"
	play = Summon(CONTROLLER, "BRMC_95he") * 2

class BRMC_95he:
	events = TURN_END.on(Summon(CONTROLLER, Copy(ID("BRMC_95he") + KILLED_THIS_TURN)))


class BRMC_100:
	"Living Bomb"
	play = Buff(TARGET, "BRMC_100e")

class BRMC_100e:
	events = OWN_TURN_BEGIN.on(Hit(FRIENDLY_MINIONS, 5))


##
# Weapons

class BRMC_94:
	"Sulfuras"
	deathrattle = Summon(CONTROLLER, "BRM_027p")
