from ..utils import *


# Damage 1
class XXX_001:
	action = [Hit(TARGET, 1)]


# Damage 5
class XXX_002:
	action = [Hit(TARGET, 5)]


# Restore 1
class XXX_003:
	action = [Heal(TARGET, 1)]


# Restore 5
class XXX_004:
	action = [Heal(TARGET, 5)]


# Destroy
class XXX_005:
	action = [Destroy(TARGET)]


# Break Weapon
class XXX_006:
	action = [Destroy(ENEMY_WEAPON)]


# Enable for Attack
class XXX_007:
	action = [GiveCharge(TARGET)]


# Freeze
class XXX_008:
	action = [Freeze(TARGET)]


# Enchant
class XXX_009:
	action = [Buff(TARGET, "XXX_009e")]


# Silence - debug
class XXX_010:
	action = [Silence(TARGET)]


# Summon a random Secret
class XXX_011:
	action = [ForcePlay(CONTROLLER, RANDOM(CONTROLLER_DECK + SECRET))]


# Bounce
class XXX_012:
	action = [Bounce(TARGET)]


# Discard
class XXX_013:
	action = [Discard(CONTROLLER_HAND)]


# Mill 10
class XXX_014:
	action = [Mill(CONTROLLER, 10)]


# Crash
class XXX_015:
	def action(self):
		assert False


# Snake Ball
class XXX_016:
	action = [Summon("EX1_554t") * 5]


# Draw 3 Cards
class XXX_017:
	action = [Draw(CONTROLLER, 3)]


# Destroy All Minions
class XXX_018:
	action = [Destroy(ALL_MINIONS)]


# Restore All Health
class XXX_021:
	action = [FullHeal(TARGET)]


# Destroy All Heroes
class XXX_023:
	action = [Destroy(ALL_HEROES)]


# Do Nothing
class XXX_025:
	pass


# Server Crash
class XXX_027:
	def action(self):
		raise SystemError


# Destroy Hero Power
class XXX_041:
	action = [Destroy(HERO_POWER + CONTROLLED_BY_TARGET)]


# -1 Durability
class XXX_048:
	action = [Hit(ALL_WEAPONS + CONTROLLED_BY_TARGET, 1)]


# Destroy All Mana
class XXX_049:
	def action(self, target):
		return [GiveMana(-target.controller.maxMana)]


# Destroy a Mana Crystal
class XXX_050:
	action = [GiveMana(PLAYER + CONTROLLED_BY_TARGET, -1)]


# Armor
class XXX_053:
	action = [GainArmor(CONTROLLER, 100)]


# Weapon Buff
class XXX_054:
	action = [Buff(FRIENDLY_WEAPON, "XXX_054e")]


# 1000 Stats
class XXX_055:
	action = [Buff(TARGET, "XXX_055e")]


# Silence Destroy
class XXX_056:
	action = [Silence(ALL_MINIONS), Destroy(ALL_MINIONS)]


# Destroy Secrets
class XXX_057:
	action = [Destroy(ALL_SECRETS + CONTROLLED_BY_TARGET)]
