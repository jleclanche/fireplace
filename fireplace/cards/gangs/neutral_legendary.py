from ..utils import *

##
# Minions

class CFM_341:
	"Sergeant Sally"
	def deathrattle(self):
		if self.dead:
			count = self.preatk
		else:
			count = self.atk
		yield Hit(ENEMY_MINIONS, count)

class CFM_344:
	"Finja, the Flying Star"
	events = Attack(SELF).after(
		Dead(Attack.DEFENDER + ALL_MINIONS) &
		Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MURLOC) * 2)
	)

class CFM_621:
	"Kazakus"
	powered_up = -FindDuplicates(FRIENDLY_DECK)
	play = powered_up & Kazakus(CONTROLLER)

class CFM_637:
	"Patches the Pirate"
	class Deck:
		events = Summon(CONTROLLER, FRIENDLY + MINION + PIRATE).after(Summon(CONTROLLER, SELF))

class CFM_670:
	"Mayor Noggenfogger"
	update = Refresh(ALL_PLAYERS, {GameTag.ALL_TARGETS_RANDOM: True})
#	TODO: Requires implementation of GameTag.ALL_TARGETS_RANDOM: 477

class CFM_672:
	"Madam Goya"
	def play(self):
		targets = self.controller.deck.filter(type=CardType.MINION)
		if targets:
			yield Shuffle(CONTROLLER, TARGET)
			yield Summon(CONTROLLER, random.sample(targets, 1))

class CFM_685:
	"Don Han'Cho"
	play = Buff(RANDOM(FRIENDLY_HAND + MINION), "CFM_685e")

CFM_685e = buff(+5, +5)

class CFM_806:
	"Wrathion"
	def play(self):
		while True:
			current_handsize = len(self.controller.hand)
			yield Draw(self.controller)
			if len(self.controller.hand) == current_handsize:
				#Unable to draw card due to fatigue or max hand size
				break
			card = self.controller.hand[-1]
			if card.type == CardType.MINION and card.race == Race.DRAGON:
				continue
			else:
				break

class CFM_807:
	"Auctionmaster Beardo"
	events = OWN_SPELL_PLAY.after(Buff(FRIENDLY_HERO_POWER, "CFM_807e"))

CFM_807e = buff()
@custom_card
class CFM_807e:
	tags = {
		GameTag.CARDNAME: "Auctionmaster Beardo Buff",
		GameTag.CARDTYPE: CardType.ENCHANTMENT,
		GameTag.HEROPOWER_ADDITIONAL_ACTIVATIONS: 1,
		GameTag.TAG_ONE_TURN_EFFECT: 1
	}


class CFM_808:
	"Genzo, the Shark"
	events = Attack(SELF).on(DrawUntil(ALL_PLAYERS, 3))

class CFM_902:
	"Aya Blackpaw"
	play = SummonJadeGolem(CONTROLLER)
	deathrattle = SummonJadeGolem(CONTROLLER)
