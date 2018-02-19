from ..utils import *


##
# Minions

class LOE_003:
	"Ethereal Conjurer"
	play = DISCOVER(RandomSpell())


class LOE_006:
	"Museum Curator"
	play = DISCOVER(RandomCollectible(deathrattle=True))


class LOE_009:
	"Obsidian Destroyer"
	events = OWN_TURN_END.on(Summon(CONTROLLER, "LOE_009t"))


class LOE_011:
	"Reno Jackson"
	powered_up = -FindDuplicates(FRIENDLY_DECK)
	play = powered_up & FullHeal(FRIENDLY_HERO)


class LOE_012:
	"Tomb Pillager"
	deathrattle = Give(CONTROLLER, "GAME_005")


class LOE_016:
	"Rumbling Elemental"
	events = Play(CONTROLLER, MINION + BATTLECRY).after(Hit(RANDOM_ENEMY_CHARACTER, 2))


class LOE_017:
	"Keeper of Uldaman"
	play = Buff(TARGET, "LOE_017e")

class LOE_017e:
	atk = SET(3)
	max_health = SET(3)


class LOE_018:
	"Tunnel Trogg"
	events = Overload(CONTROLLER).on(Buff(SELF, "LOE_018e") * Overload.AMOUNT)

LOE_018e = buff(atk=1)


class LOE_019:
	"Unearthed Raptor"
	play = Buff(SELF, "LOE_019e").then(CopyDeathrattles(Buff.BUFF, TARGET))

LOE_019e = buff(deathrattle=True)


class LOE_020:
	"Desert Camel"
	play = (
		Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + (COST == 1))),
		Summon(OPPONENT, RANDOM(ENEMY_DECK + (COST == 1)))
	)


class LOE_023:
	"Dark Peddler"
	play = DISCOVER(RandomCollectible(cost=1))


class LOE_029:
	"Jeweled Scarab"
	play = DISCOVER(RandomCollectible(cost=3))


class LOE_038:
	"Naga Sea Witch"
	update = Refresh(FRIENDLY_HAND, {GameTag.COST: SET(5)})


class LOE_039:
	"Gorillabot A-3"
	powered_up = Find(FRIENDLY_MINIONS + MECH - SELF)
	play = powered_up & DISCOVER(RandomMech())


class LOE_046:
	"Huge Toad"
	deathrattle = Hit(RANDOM_ENEMY_CHARACTER, 1)


class LOE_047:
	"Tomb Spider"
	play = DISCOVER(RandomBeast())


class LOE_050:
	"Mounted Raptor"
	deathrattle = Summon(CONTROLLER, RandomMinion(cost=1))


class LOE_051:
	"Jungle Moonkin"
	update = Refresh(OPPONENT, {GameTag.SPELLPOWER: +2})


class LOE_053:
	"Djinni of Zephyrs"
	events = Play(CONTROLLER, SPELL, FRIENDLY + MINION - SELF).after(Battlecry(Play.CARD, SELF))


class LOE_061:
	"Anubisath Sentinel"
	deathrattle = Buff(RANDOM_OTHER_FRIENDLY_MINION, "LOE_061e")

LOE_061e = buff(+3, +3)


class LOE_073:
	"Fossilized Devilsaur"
	powered_up = Find(FRIENDLY_MINIONS + BEAST)
	play = powered_up & Taunt(SELF)


# Fossilized (Unused)
LOE_073e = buff(taunt=True)


class LOE_076:
	"Sir Finley Mrrgglton"
	play = GenericChoice(CONTROLLER, RandomBasicHeroPower() * 3)


class LOE_077:
	"Brann Bronzebeard"
	update = Refresh(CONTROLLER, {enums.EXTRA_BATTLECRIES: True})


class LOE_079:
	"Elise Starseeker"
	play = Shuffle(CONTROLLER, "LOE_019t")


class LOE_019t:
	"Map to the Golden Monkey"
	play = Shuffle(CONTROLLER, "LOE_019t2"), Draw(CONTROLLER)


class LOE_019t2:
	"Golden Monkey"
	play = Morph(FRIENDLY + (IN_HAND | IN_DECK), RandomLegendaryMinion())


class LOE_086:
	"Summoning Stone"
	events = OWN_SPELL_PLAY.on(
		Summon(CONTROLLER, RandomMinion(cost=Attr(Play.CARD, GameTag.COST)))
	)


class LOE_089:
	"Wobbling Runts"
	deathrattle = (
		Summon(CONTROLLER, "LOE_089t"),
		Summon(CONTROLLER, "LOE_089t2"),
		Summon(CONTROLLER, "LOE_089t3")
	)


class LOE_092:
	"Arch-Thief Rafaam"
	play = DISCOVER(RandomID("LOEA16_3", "LOEA16_5", "LOEA16_4"))


class LOEA16_3:
	"Lantern of Power"
	play = Buff(TARGET, "LOEA16_3e")

LOEA16_3e = buff(+10, +10)


class LOEA16_4:
	"Timepiece of Horror"
	def play(self):
		count = self.controller.get_spell_damage(10)
		yield Hit(RANDOM_ENEMY_CHARACTER, 1) * count


class LOEA16_5:
	"Mirror of Doom"
	play = Summon(CONTROLLER, "LOEA16_5t")


class LOE_107:
	"Eerie Statue"
	update = Find(ALL_MINIONS - SELF) & Refresh(SELF, {GameTag.CANT_ATTACK: True})


class LOE_110:
	"Ancient Shade"
	play = Shuffle(CONTROLLER, "LOE_110t")

class LOE_110t:
	"Ancient Curse"
	draw = Destroy(SELF), Hit(FRIENDLY_HERO, 7), Draw(CONTROLLER)


class LOE_116:
	"Reliquary Seeker"
	powered_up = Count(FRIENDLY_MINIONS) == 6
	play = (Count(FRIENDLY_MINIONS) == 7) & Buff(SELF, "LOE_009e")

LOE_009e = buff(+4, +4)


class LOE_119:
	"Animated Armor"
	update = Refresh(FRIENDLY_HERO, {GameTag.HEAVILY_ARMORED: True})


##
# Spells

class LOE_002:
	"Forgotten Torch"
	play = Hit(TARGET, 3), Shuffle(CONTROLLER, "LOE_002t")

class LOE_002t:
	play = Hit(TARGET, 6)


class LOE_007:
	"Curse of Rafaam"
	play = Give(OPPONENT, "LOE_007t")

class LOE_007t:
	"Cursed!"
	class Hand:
		events = OWN_TURN_BEGIN.on(Hit(FRIENDLY_HERO, 2))


class LOE_026:
	"Anyfin Can Happen"
	play = Summon(CONTROLLER, Copy(RANDOM(KILLED + MURLOC) * 7))


class LOE_104:
	"Entomb"
	play = Steal(TARGET), Shuffle(CONTROLLER, TARGET)


class LOE_105:
	"Explorer's Hat"
	play = Buff(TARGET, "LOE_105e")

class LOE_105e:
	deathrattle = Give(CONTROLLER, "LOE_105")
	tags = {
		GameTag.ATK: +1,
		GameTag.HEALTH: +1,
		GameTag.DEATHRATTLE: True,
	}


class LOE_111:
	"Excavated Evil"
	play = Hit(ALL_MINIONS, 3), Shuffle(OPPONENT, Copy(SELF))


class LOE_113:
	"Everyfin is Awesome"
	cost_mod = -Count(FRIENDLY_MINIONS + MURLOC)
	play = Buff(FRIENDLY_MINIONS, "LOE_113e")

LOE_113e = buff(+2, +2)


class LOE_115:
	"Raven Idol"
	choose = ("LOE_115a", "LOE_115b")
	play = ChooseBoth(CONTROLLER) & (DISCOVER(RandomMinion()), DISCOVER(RandomSpell()))

class LOE_115a:
	play = DISCOVER(RandomMinion())

class LOE_115b:
	play = DISCOVER(RandomSpell())


##
# Secrets

class LOE_021:
	"Dart Trap"
	secret = Activate(OPPONENT, HERO_POWER).on(
		Reveal(SELF), Hit(RANDOM_ENEMY_CHARACTER, 5)
	)


class LOE_027:
	"Sacred Trial"
	secret = Play(OPPONENT, MINION | HERO).after(
		(Count(ENEMY_MINIONS) >= 4) & (
			Reveal(SELF), Destroy(Play.CARD)
		)
	)


##
# Weapons

class LOE_118:
	"Cursed Blade"
	update = Refresh(FRIENDLY_HERO, buff="LOE_118e")

class LOE_118e:
	tags = {GameTag.INCOMING_DAMAGE_MULTIPLIER: True}
