from ..utils import *


##
# Minions

# Ethereal Conjurer
class LOE_003:
	play = Discover(CONTROLLER, RandomSpell())


# Museum Curator
class LOE_006:
	play = Discover(CONTROLLER, RandomCollectible(deathrattle=True))


# Obsidian Destroyer
class LOE_009:
	events = OWN_TURN_END.on(Summon(CONTROLLER, "LOE_009t"))


# Dark Peddler
class LOE_023:
	play = Discover(CONTROLLER, RandomCollectible(cost=1))


# Jeweled Scarab
class LOE_029:
	play = Discover(CONTROLLER, RandomCollectible(cost=3))


# Gorillabot A-3
class LOE_039:
	powered_up = Find(FRIENDLY_MINIONS + MECH)
	play = powered_up & Discover(CONTROLLER, RandomMech())


# Huge Toad
class LOE_046:
	deathrattle = Hit(RANDOM_ENEMY_CHARACTER, 1)


# Tomb Spider
class LOE_047:
	play = Discover(CONTROLLER, RandomBeast())


# Fossilized Devilsaur
class LOE_073:
	play = Find(FRIENDLY_MINIONS + BEAST) & Taunt(SELF)


# Ancient Shade
class LOE_110:
	play = Shuffle(CONTROLLER, "LOE_110t")

# Ancient Curse
class LOE_110t:
	draw = Destroy(SELF), Hit(FRIENDLY_HERO, 7), Draw(CONTROLLER)


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


# Everyfin is Awesome
class LOE_113:
	cost_mod = -Count(FRIENDLY_MINIONS + MURLOC)
	play = Buff(FRIENDLY_MINIONS, "LOE_113e")

LOE_113e = buff(+2, +2)


# Raven Idol
class LOE_115:
	choose = ("LOE_115a", "LOE_115b")

class LOE_115a:
	play = Discover(CONTROLLER, RandomMinion())

class LOE_115b:
	play = Discover(CONTROLLER, RandomSpell())


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
