from ..utils import *


class XXX_001:
	"""Damage 1"""
	play = Hit(TARGET, 1)


class XXX_002:
	"""Damage 5"""
	play = Hit(TARGET, 5)


class XXX_003:
	"""Restore 1"""
	play = Heal(TARGET, 1)


class XXX_004:
	"""Restore 5"""
	play = Heal(TARGET, 5)


class XXX_005:
	"""Destroy"""
	play = Destroy(TARGET)


class XXX_006:
	"""Break Weapon"""
	play = Destroy(ENEMY_WEAPON)


class XXX_007:
	"""Enable for Attack"""
	play = GiveCharge(TARGET)


class XXX_008:
	"""Freeze"""
	play = Freeze(TARGET)


class XXX_009:
	"""Enchant"""
	play = Buff(TARGET, "XXX_009e")


class XXX_009e:
	pass


class XXX_010:
	"""Silence - debug"""
	play = Silence(TARGET)


class XXX_011:
	"""Summon a random Secret"""
	play = Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + SECRET))


class XXX_012:
	"""Bounce"""
	play = Bounce(TARGET)


class XXX_013:
	"""Discard"""
	play = Discard(FRIENDLY_HAND)


class XXX_014:
	"""Mill 10"""
	play = Mill(CONTROLLER, 10)


class XXX_015:
	"""Crash"""
	def play(self):
		assert False


class XXX_016:
	"""Snake Ball"""
	play = Summon("EX1_554t") * 5


class XXX_017:
	"""Draw 3 Cards"""
	play = Draw(CONTROLLER) * 3


class XXX_018:
	"""Destroy All Minions"""
	play = Destroy(ALL_MINIONS)


class XXX_019:
	"""Molasses"""
	play = UnsetTag(CONTROLLER, (GameTag.TIMEOUT, ))


class XXX_020:
	"""Damage all but 1"""
	play = SetCurrentHealth(TARGET, 1)


class XXX_021:
	"""Restore All Health"""
	play = FullHeal(TARGET)


class XXX_022:
	"""Free Cards"""
	play = Buff(FRIENDLY_HERO, "XXX_022e")


class XXX_022e:
	update = Refresh(FRIENDLY_HAND, {GameTag.COST: SET(0)})


class XXX_023:
	"""Destroy All Heroes"""
	play = Destroy(ALL_HEROES)


class XXX_024:
	"""Damage Reflector"""
	events = Damage(SELF).on(Hit(ALL_CHARACTERS - SELF, 1))


class XXX_025:
	"""Do Nothing"""
	pass


class XXX_026:
	"""Enable Emotes"""
	pass


class XXX_027:
	"""Server Crash"""
	def play(self):
		raise SystemError("Fool!")


class XXX_029:
	"""Opponent Concede"""
	play = Concede(OPPONENT)


class XXX_030:
	"""Opponent Disconnect"""
	play = Disconnect(OPPONENT)


class XXX_039:
	"""Become Hogger"""
	play = Summon(CONTROLLER, "XXX_040")


class XXX_041:
	"""Destroy Hero Power"""
	play = Destroy(HERO_POWER + CONTROLLED_BY(TARGET))


class XXX_042:
	"""Hand to Deck"""
	play = Shuffle(TARGET_PLAYER, IN_HAND + CONTROLLED_BY(TARGET))


class XXX_043:
	"""Mill 30"""
	play = Mill(TARGET_PLAYER, 30)


class XXX_044:
	"""Hand Swapper Minion"""
	play = Discard(RANDOM(FRIENDLY_HAND) * 3), Draw(CONTROLLER) * 3


class XXX_045:
	"""Steal Card"""
	play = Steal(RANDOM(ENEMY_HAND))


class XXX_046:
	"""Force AI to Use Hero Power"""
	play = SetTag(ENEMY_HERO_POWER, (GameTag.TAG_AI_MUST_PLAY, ))


class XXX_047:
	"""Destroy Deck"""
	play = Destroy(IN_DECK + CONTROLLED_BY(TARGET))


class XXX_048:
	"""-1 Durability"""
	play = Hit(ALL_WEAPONS + CONTROLLED_BY(TARGET), 1)


class XXX_049:
	"""Destroy all Mana"""
	def play(self):
		yield GainMana(-self.target.controller.max_mana)


class XXX_050:
	"""Destroy a Mana Crystal"""
	play = GainMana(TARGET_PLAYER, -1)


class XXX_051:
	"""Make Immune"""
	play = SetTag(TARGET, (GameTag.CANT_BE_DAMAGED, ))


class XXX_052:
	"""Grant Mega-Windfury"""
	play = SetTag(TARGET, {GameTag.WINDFURY: 3})


class XXX_053:
	"""Armor 100"""
	play = GainArmor(TARGET, 100)


class XXX_054:
	"""Weapon Buff"""
	play = Buff(FRIENDLY_WEAPON, "XXX_054e")


XXX_054e = buff(+100, +100)


class XXX_055:
	"""1000 Stats"""
	play = Buff(TARGET, "XXX_055e")


XXX_055e = buff(+1000, +1000)


class XXX_056:
	"""Silence and Destroy All Minions"""
	play = Silence(ALL_MINIONS), Destroy(ALL_MINIONS)


class XXX_057:
	"""Destroy Target Secrets"""
	play = Destroy(ALL_SECRETS + CONTROLLED_BY(TARGET))


class XXX_058:
	"""Weapon Nerf"""
	play = Buff(WEAPON + CONTROLLED_BY(TARGET), "XXX_058e")


class XXX_058e:
	pass


class XXX_059:
	"""Destroy Hero's Stuff"""
	play = (
		Destroy(CONTROLLED_BY(TARGET) + (HERO_POWER | IN_DECK)),
		Discard(IN_HAND + CONTROLLED_BY(TARGET)),
	)


class XXX_060:
	"""Damage All"""
	play = Hit(TARGET, CURRENT_HEALTH(TARGET))


class XXX_061:
	"""Armor 1"""
	play = GainArmor(TARGET, 1)


class XXX_062:
	"""Armor 5"""
	play = GainArmor(TARGET, 5)


class XXX_063:
	"""Destroy ALL Secrets"""
	play = Destroy(ALL_SECRETS)


class XXX_065:
	"""Remove All Immune"""
	play = UnsetTag(TARGET, (GameTag.CANT_BE_DAMAGED, ))


class XXX_094:
	"""AI Buddy - Blank Slate"""
	play = (
		Destroy(ALL_MINIONS),
		Discard(IN_HAND | IN_DECK),
		GainMana(ALL_PLAYERS, -10),
		Destroy(ALL_SECRETS)
	)


class XXX_095:
	"""AI Buddy - All Charge!"""
	play = GiveCharge(ALL_MINIONS)


class XXX_096:
	"""AI Buddy - Damage Own Hero 5"""
	play = Hit(FRIENDLY_HERO, 5)


class XXX_097:
	"""AI Buddy - Destroy Minions"""
	play = Destroy(ALL_MINIONS)


class XXX_098:
	"""AI Buddy - No Deck/Hand"""
	play = Discard(ENEMY + (IN_HAND | IN_DECK))


class XXX_099:
	"""AI Helper Buddy"""
	pass


class XXX_999_Crash:
	"""Crash the server"""
	def play(self):
		raise SystemError("What have you done?")
