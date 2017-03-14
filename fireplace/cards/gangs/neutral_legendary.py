from ..utils import *

##
# Minions

#class CFM_341:
#	"Sergeant Sally"

class CFM_344:
	"Finja, the Flying Star"
	events = Attack(SELF).after(
		Find(Attack.DEFENDER + MORTALLY_WOUNDED) & 
		Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MURLOC) * 2)
		)

#class CFM_621:
#	"Kazakus"

# class CFM_637:
# 	"Patches the Pirate"

#class CFM_670:
#	"Mayor Noggenfogger"
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

# class CFM_807:
# 	"Auctionmaster Beardo"

class CFM_808:
	"Genzo, the Shark"
	events = Attack(SELF).on(DrawUntil(ALL_PLAYERS, 3))

#class CFM_902:
#	"Aya Blackpaw"

