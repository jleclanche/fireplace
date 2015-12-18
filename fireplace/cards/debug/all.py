from ..utils import *


# Damage 1
class XXX_001:
	play = Hit(TARGET, 1)


# Damage 5
class XXX_002:
	play = Hit(TARGET, 5)


# Restore 1
class XXX_003:
	play = Heal(TARGET, 1)


# Restore 5
class XXX_004:
	play = Heal(TARGET, 5)


# Destroy
class XXX_005:
	play = Destroy(TARGET)


# Break Weapon
class XXX_006:
	play = Destroy(ENEMY_WEAPON)


# Enable for Attack
class XXX_007:
	play = GiveCharge(TARGET)


# Freeze
class XXX_008:
	play = Freeze(TARGET)


# Enchant
class XXX_009:
	play = Buff(TARGET, "XXX_009e")


# Silence - debug
class XXX_010:
	play = Silence(TARGET)


# Summon a random Secret
class XXX_011:
	play = Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + SECRET))


# Bounce
class XXX_012:
	play = Bounce(TARGET)


# Discard
class XXX_013:
	play = Discard(FRIENDLY_HAND)


# Mill 10
class XXX_014:
	play = Mill(CONTROLLER, 10)


# Crash
class XXX_015:
	def play(self):
		assert False


# Snake Ball
class XXX_016:
	play = Summon("EX1_554t") * 5


# Draw 3 Cards
class XXX_017:
	play = Draw(CONTROLLER) * 3


# Destroy All Minions
class XXX_018:
	play = Destroy(ALL_MINIONS)


# Molasses
class XXX_019:
	play = UnsetTag(CONTROLLER, (GameTag.TIMEOUT, ))


# Damage all but 1
class XXX_020:
	play = SetCurrentHealth(TARGET, 1)


# Restore All Health
class XXX_021:
	play = FullHeal(TARGET)


# Free Cards
class XXX_022:
	play = Buff(FRIENDLY_HERO, "XXX_022e")

class XXX_022e:
	update = Refresh(FRIENDLY_HAND, {GameTag.COST: SET(0)})


# Destroy All Heroes
class XXX_023:
	play = Destroy(ALL_HEROES)


# Damage Reflector
class XXX_024:
	events = Damage(SELF).on(Hit(ALL_CHARACTERS - SELF, 1))


# Do Nothing
class XXX_025:
	pass


# Server Crash
class XXX_027:
	def play(self):
		raise SystemError("Fool!")


# Opponent Concede
class XXX_029:
	play = Concede(OPPONENT)


# Become Hogger
class XXX_039:
	play = Summon(CONTROLLER, "XXX_040")


# Destroy Hero Power
class XXX_041:
	play = Destroy(HERO_POWER + CONTROLLED_BY(TARGET))


# Hand to Deck
class XXX_042:
	play = Shuffle(TARGET_PLAYER, IN_HAND + CONTROLLED_BY(TARGET))


# Mill 30
class XXX_043:
	play = Mill(TARGET_PLAYER, 30)


# Hand Swapper Minion
class XXX_044:
	play = Discard(RANDOM(FRIENDLY_HAND) * 3), Draw(CONTROLLER) * 3


# Steal Card
class XXX_045:
	play = Steal(RANDOM(ENEMY_HAND))


# Force AI to Use Hero Power
class XXX_046:
	play = SetTag(ENEMY_HERO_POWER, (GameTag.TAG_AI_MUST_PLAY, ))


# Destroy Deck
class XXX_047:
	play = Destroy(IN_DECK + CONTROLLED_BY(TARGET))


# -1 Durability
class XXX_048:
	play = Hit(ALL_WEAPONS + CONTROLLED_BY(TARGET), 1)


# Destroy All Mana
class XXX_049:
	def play(self):
		yield GainMana(-self.target.controller.max_mana)


# Destroy a Mana Crystal
class XXX_050:
	play = GainMana(TARGET_PLAYER, -1)


# Make Immune
class XXX_051:
	play = SetTag(TARGET, (GameTag.CANT_BE_DAMAGED, ))


# Grant Mega-Windfury
class XXX_052:
	play = SetTag(TARGET, {GameTag.WINDFURY: 3})


# Armor 100
class XXX_053:
	play = GainArmor(TARGET, 100)


# Weapon Buff
class XXX_054:
	play = Buff(FRIENDLY_WEAPON, "XXX_054e")

XXX_054e = buff(+100, +100)


# 1000 Stats
class XXX_055:
	play = Buff(TARGET, "XXX_055e")

XXX_055e = buff(+1000, +1000)


# Silence Destroy
class XXX_056:
	play = Silence(ALL_MINIONS), Destroy(ALL_MINIONS)


# Destroy Secrets
class XXX_057:
	play = Destroy(ALL_SECRETS + CONTROLLED_BY(TARGET))


# Weapon Nerf
class XXX_058:
	play = Buff(WEAPON + CONTROLLED_BY(TARGET), "XXX_058e")


# Destroy All
class XXX_059:
	play = (
		Destroy(CONTROLLED_BY(TARGET) + (HERO_POWER | IN_DECK)),
		Discard(IN_HAND + CONTROLLED_BY(TARGET)),
	)


# Damage All
class XXX_060:
	play = Hit(TARGET, CURRENT_HEALTH(TARGET))


# Armor 1
class XXX_061:
	play = GainArmor(TARGET, 1)


# Armor 5
class XXX_062:
	play = GainArmor(TARGET, 5)


# Destroy ALL Secrets
class XXX_063:
	play = Destroy(ALL_SECRETS)


# Remove All Immune
class XXX_065:
	play = UnsetTag(TARGET, (GameTag.CANT_BE_DAMAGED, ))
