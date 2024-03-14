from ..utils import *


##
# Minions

class DAL_087:
	"""Hench-Clan Hag"""
	# <b>Battlecry:</b> Summon two 1/1 Amalgams with all minion types.
	play = Summon(CONTROLLER, "DAL_087t") * 2


class DAL_538:
	"""Unseen Saboteur"""
	# <b>Battlecry:</b> Your opponent casts a random spell from their hand <i>(targets
	# chosen randomly)</i>.
	# TODO need test
	play = CastSpell(RANDOM(ENEMY_HAND + SPELL))


class DAL_548:
	"""Azerite Elemental"""
	# At the start of your turn, gain <b>Spell Damage +2</b>.
	events = OWN_TURN_BEGIN.on(Buff(SELF, "DAL_548e"))


DAL_548e = buff(spellpower=2)


class DAL_553:
	"""Big Bad Archmage"""
	# At the end of your turn, summon a random 6-Cost minion.
	events = OWN_TURN_END.on(Summon(CONTROLLER, RandomMinion(cost=6)))


class DAL_565:
	"""Portal Overfiend"""
	# [x]<b>Battlecry:</b> Shuffle 3 Portals into your deck. When drawn, summon a 2/2 Demon
	# with <b>Rush</b>.
	play = Shuffle(CONTROLLER, "DAL_582t") * 3


class DAL_592:
	"""Batterhead"""
	# <b>Rush</b>. After this attacks and kills a minion, it may_attack again.
	events = Attack(SELF, ALL_MINIONS).after(
		Dead(ALL_MINIONS + Attack.DEFENDER) & ExtraAttack(SELF)
	)


class DAL_742:
	"""Whirlwind Tempest"""
	# Your minions with <b>Windfury</b> have <b>Mega-Windfury</b>.
	update = Refresh(FRIENDLY_MINIONS + WINDFURY, {GameTag.MEGA_WINDFURY: True})


class DAL_773:
	"""Magic Carpet"""
	# After you play a 1-Cost minion, give it +1 Attack and <b>Rush</b>.
	events = Play(CONTROLLER, MINION + (COST == 1)).after(Buff(Play.CARD, "DAL_773e"))


DAL_773e = buff(atk=1, rush=True)
