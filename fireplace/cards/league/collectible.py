from ..utils import *


##
# Minions

# Obsidian Destroyer
class LOE_009:
	events = OWN_TURN_END.on(Summon(CONTROLLER, "LOE_009t"))


# Huge Toad
class LOE_046:
	deathrattle = Hit(RANDOM_ENEMY_CHARACTER, 1)


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


# Raven Idol
class LOE_115:
	choose = ("LOE_115a", "LOE_115b")


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
