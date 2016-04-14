from ..utils import *


##
# Minions

# Ethereal Conjurer
class LOE_003:
	play = DISCOVER(RandomSpell())


# Museum Curator
class LOE_006:
	play = DISCOVER(RandomCollectible(deathrattle=True))


# Obsidian Destroyer
class LOE_009:
	events = OWN_TURN_END.on(Summon(CONTROLLER, "LOE_009t"))


# Reno Jackson
class LOE_011:
	powered_up = -FindDuplicates(FRIENDLY_DECK)
	play = powered_up & FullHeal(FRIENDLY_HERO)


# Tomb Pillager
class LOE_012:
	deathrattle = Give(CONTROLLER, "GAME_005")


# Rumbling Elemental
class LOE_016:
	events = Play(CONTROLLER, MINION + BATTLECRY).after(Hit(RANDOM_ENEMY_CHARACTER, 2))


# Keeper of Uldaman
class LOE_017:
	play = Buff(TARGET, "LOE_017e")

class LOE_017e:
	atk = SET(3)
	max_health = SET(3)


# Tunnel Trogg
class LOE_018:
	events = Overload(CONTROLLER).on(Buff(SELF, "LOE_018e") * Overload.AMOUNT)

LOE_018e = buff(atk=1)


# Unearthed Raptor
class LOE_019:
	play = Buff(SELF, "LOE_019e").then(CopyDeathrattles(Buff.BUFF, TARGET))

LOE_019e = buff(deathrattle=True)


# Desert Camel
class LOE_020:
	play = (
		Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + (COST == 1))),
		Summon(OPPONENT, RANDOM(ENEMY_DECK + (COST == 1)))
	)


# Dark Peddler
class LOE_023:
	play = DISCOVER(RandomCollectible(cost=1))


# Jeweled Scarab
class LOE_029:
	play = DISCOVER(RandomCollectible(cost=3))


# Naga Sea Witch
class LOE_038:
	update = Refresh(FRIENDLY_HAND, {GameTag.COST: SET(5)})


# Gorillabot A-3
class LOE_039:
	powered_up = Find(FRIENDLY_MINIONS + MECH - SELF)
	play = powered_up & DISCOVER(RandomMech())


# Huge Toad
class LOE_046:
	deathrattle = Hit(RANDOM_ENEMY_CHARACTER, 1)


# Tomb Spider
class LOE_047:
	play = DISCOVER(RandomBeast())


# Mounted Raptor
class LOE_050:
	deathrattle = Summon(CONTROLLER, RandomMinion(cost=1))


# Jungle Moonkin
class LOE_051:
	update = Refresh(OPPONENT, {GameTag.SPELLPOWER: +2})


# Djinni of Zephyrs
class LOE_053:
	events = Play(CONTROLLER, SPELL, FRIENDLY + MINION - SELF).after(Battlecry(Play.CARD, SELF))


# Anubisath Sentinel
class LOE_061:
	deathrattle = Buff(RANDOM_OTHER_FRIENDLY_MINION, "LOE_061e")

LOE_061e = buff(+3, +3)


# Fossilized Devilsaur
class LOE_073:
	powered_up = Find(FRIENDLY_MINIONS + BEAST)
	play = powered_up & Taunt(SELF)


# Fossilized (Unused)
LOE_073e = buff(taunt=True)


# Sir Finley Mrrgglton
class LOE_076:
	play = GenericChoice(CONTROLLER, RandomEntourage() * 3)


# Brann Bronzebeard:
class LOE_077:
	update = Refresh(CONTROLLER, {enums.EXTRA_BATTLECRIES: True})


# Elise Starseeker
class LOE_079:
	play = Shuffle(CONTROLLER, "LOE_019t")


# Map to the Golden Monkey
class LOE_019t:
	play = Shuffle(CONTROLLER, "LOE_019t2"), Draw(CONTROLLER)


# Golden Monkey
class LOE_019t2:
	play = Morph(FRIENDLY + (IN_HAND | IN_DECK), RandomLegendaryMinion())


# Summoning Stone
class LOE_086:
	events = OWN_SPELL_PLAY.on(
		Summon(CONTROLLER, RandomMinion(cost=Attr(Play.CARD, GameTag.COST)))
	)


# Wobbling Runts
class LOE_089:
	deathrattle = (
		Summon(CONTROLLER, "LOE_089t"),
		Summon(CONTROLLER, "LOE_089t2"),
		Summon(CONTROLLER, "LOE_089t3")
	)


# Arch-Thief Rafaam
class LOE_092:
	play = DISCOVER(RandomID("LOEA16_3", "LOEA16_5", "LOEA16_4"))


# Lantern of Power
class LOEA16_3:
	play = Buff(TARGET, "LOEA16_3e")

LOEA16_3e = buff(+10, +10)


# Timepiece of Horror
class LOEA16_4:
	def play(self):
		count = self.controller.get_spell_damage(10)
		yield Hit(RANDOM_ENEMY_CHARACTER, 1) * count


# Mirror of Doom
class LOEA16_5:
	play = Summon(CONTROLLER, "LOEA16_5t")


# Eerie Statue
class LOE_107:
	update = Find(ALL_MINIONS - SELF) & Refresh(SELF, {GameTag.CANT_ATTACK: True})


# Ancient Shade
class LOE_110:
	play = Shuffle(CONTROLLER, "LOE_110t")

# Ancient Curse
class LOE_110t:
	draw = Destroy(SELF), Hit(FRIENDLY_HERO, 7), Draw(CONTROLLER)


# Reliquary Seeker
class LOE_116:
	powered_up = Count(FRIENDLY_MINIONS) == 6
	play = (Count(FRIENDLY_MINIONS) == 7) & Buff(SELF, "LOE_009e")

LOE_009e = buff(+4, +4)


# Animated Armor
class LOE_119:
	update = Refresh(FRIENDLY_HERO, {GameTag.HEAVILY_ARMORED: True})


##
# Spells

# Forgotten Torch
class LOE_002:
	play = Hit(TARGET, 3), Shuffle(CONTROLLER, "LOE_002t")

class LOE_002t:
	play = Hit(TARGET, 6)


# Curse of Rafaam
class LOE_007:
	play = Give(OPPONENT, "LOE_007t")

# Cursed!
class LOE_007t:
	class Hand:
		events = OWN_TURN_BEGIN.on(Hit(FRIENDLY_HERO, 2))


# Anyfin Can Happen
class LOE_026:
	play = Summon(CONTROLLER, Copy(RANDOM(KILLED + MURLOC) * 7))


# Entomb
class LOE_104:
	play = Steal(TARGET), Shuffle(CONTROLLER, TARGET)


# Explorer's Hat
class LOE_105:
	play = Buff(TARGET, "LOE_105e")

class LOE_105e:
	deathrattle = Give(CONTROLLER, "LOE_105")
	tags = {
		GameTag.ATK: +1,
		GameTag.HEALTH: +1,
		GameTag.DEATHRATTLE: True,
	}


# Excavated Evil
class LOE_111:
	play = Hit(ALL_MINIONS, 3), Shuffle(OPPONENT, Copy(SELF))


# Everyfin is Awesome
class LOE_113:
	cost_mod = -Count(FRIENDLY_MINIONS + MURLOC)
	play = Buff(FRIENDLY_MINIONS, "LOE_113e")

LOE_113e = buff(+2, +2)


# Raven Idol
class LOE_115:
	choose = ("LOE_115a", "LOE_115b")

class LOE_115a:
	play = DISCOVER(RandomMinion())

class LOE_115b:
	play = DISCOVER(RandomSpell())


##
# Secrets

# Dart Trap
class LOE_021:
	secret = Activate(OPPONENT, HERO_POWER).on(
		Reveal(SELF), Hit(RANDOM_ENEMY_CHARACTER, 5)
	)


# Sacred Trial
class LOE_027:
	secret = Play(OPPONENT, MINION | HERO).after(
		(Count(ENEMY_MINIONS) >= 4) & (
			Reveal(SELF), Destroy(Play.CARD)
		)
	)


##
# Weapons

# Cursed Blade
class LOE_118:
	update = Refresh(FRIENDLY_HERO, buff="LOE_118e")

class LOE_118e:
	tags = {GameTag.INCOMING_DAMAGE_MULTIPLIER: True}
