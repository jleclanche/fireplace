from ..utils import *


##
# Minions

class OG_109:
	"Darkshire Librarian"
	play = Discard(RANDOM(FRIENDLY_HAND))
	deathrattle = Draw(CONTROLLER)


class OG_113:
	"Darkshire Councilman"
	events = Summon(MINION, CONTROLLER).on(Buff(SELF, "OG_113e"))

OG_113e = buff(atk=1)


class OG_121:
	"Cho'gall"
	play = Buff(CONTROLLER, "OG_121e")

class OG_121e:
	events = OWN_SPELL_PLAY.on(Destroy(SELF))
	update = Refresh(CONTROLLER, {GameTag.SPELLS_COST_HEALTH: True})


class OG_241:
	"Possessed Villager"
	deathrattle = Summon(CONTROLLER, "OG_241a")


class OG_302:
	"Usher of Souls"
	events = Death(FRIENDLY_MINIONS).on(Buff(CTHUN, "OG_302e"))

OG_302e = buff(+1, +1)

##
# Spells

class OG_114:
	"Forbidden Ritual"
	play = (
		Summon(CONTROLLER, "OG_114a") * Attr(CONTROLLER, "mana"),
		SpendMana(CONTROLLER, Attr(CONTROLLER, "mana")),
	)

class OG_116:
	"Spreading Madness"
	play = Hit(RANDOM_CHARACTER, 1) * 9


class OG_118:
	"Renounce Darkness"
	def play(self):
		RandomClass = random.choice([
			"DRUID", "HUNTER", "MAGE", "PALADIN",
			"PRIEST", "ROGUE", "SHAMAN", "WARRIOR"]
		)
		ClassMap = {
			"DRUID": CardClass.DRUID,
			"HUNTER": CardClass.HUNTER,
			"MAGE": CardClass.MAGE,
			"PALADIN": CardClass.PALADIN,
			"PRIEST": CardClass.PRIEST,
			"ROGUE": CardClass.ROGUE,
			"SHAMAN": CardClass.SHAMAN,
			"WARRIOR": CardClass.WARRIOR
		}
		HeroPowerMap = {
			"DRUID": "CS2_017",
			"HUNTER": "DS1h_292",
			"MAGE": "CS2_034",
			"PALADIN": "CS2_101",
			"PRIEST": "CS1h_001",
			"ROGUE": "CS2_083b",
			"SHAMAN": "CS2_049",
			"WARRIOR": "CS2_102"
		}
		yield Summon(CONTROLLER, HeroPowerMap[RandomClass])
		yield Morph(FRIENDLY + (IN_DECK | IN_HAND) + WARRIOR, RandomCollectible(card_class=ClassMap[RandomClass])).then(
			Buff(Morph.CARD, "OG_118f")
		)


class OG_239:
	"DOOM!"
	def play(self):
		minion_count = len(self.controller.field) + len(self.controller.opponent.field)
		yield Destroy(ALL_MINIONS)
		yield Draw(CONTROLLER) * minion_count
