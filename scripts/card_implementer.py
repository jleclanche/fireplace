import inspect
import random
import re
import sys

from hearthstone.enums import CardSet
from hearthstone.stringsfile import load_globalstrings

if __name__ == "__main__":
	sys.path.append("..")

from implemented import resolve_implemented_cards
from fireplace import cards
from fireplace.utils import get_script_definition


def clean_text(text):
	"""
	Cleans the description of a card
	:param text: Description as taken from CardDefs.xml
	:return: Description no longer containing tags, newlines and other non-typical characters
	"""
	text = re.sub('<.*?>', '', text)
	text = text.replace('\n', ' ')
	text = text.replace('_', ' ')
	text = text.replace('\'', '')
	text = text.replace('\"', '')
	text = text.replace(']', ' ')
	text = text.translate(str.maketrans('', '', '@.,:;[]()!’-'))

	return text


def levenshtein(a, b):
	"""
	Calculates the Levenshtein distance between a and b.
	"""
	n, m = len(a), len(b)
	if n > m:
		# Make sure n <= m, to use O(min(n,m)) space
		a, b = b, a
		n, m = m, n

	current = range(n + 1)
	for i in range(1, m + 1):
		previous, current = current, [i] + [0] * n
		for j in range(1, n + 1):
			add, delete = previous[j] + 1, current[j - 1] + 1
			change = previous[j - 1]
			if a[j - 1] != b[i - 1]:
				change = change + 1
			current[j] = min(add, delete, change)

	return current[n]


class CardImplementationHelper():
	"""
	This class helps with implementing cards by autogenerating boiler code
	"""

	def __init__(self):
		self.implemented, self.unimplemented = resolve_implemented_cards()
		self.implemented = set(filter(lambda x: x.card_set.is_standard or x.card_set.craftable, self.implemented))

		self.levenshtein_cache = {}
		self.levenshtein_cache_full_cards = set()

	def increase_levenshtein_cache(self, n=10, filt = None):

		new_cards = list(filter(filt, self.unimplemented)) if filt is not None else self.unimplemented
		new_cards = list(filter(lambda x: x not in self.levenshtein_cache_full_cards, new_cards))
		new_cards = random.sample(new_cards, n)

		for u in new_cards:
			for i in self.implemented | self.unimplemented:
				self.get_similarity(u, i)

		self.levenshtein_cache_full_cards.update(new_cards)

	def search_card(self):

		while True:
			matching_cards = []
			searchstr = input("Enter a card ID: ")
			try:
				return cards.db[searchstr]
			except KeyError:
				print("Card not found. Please try again")

	def get_similar_descriptions(self, card, best_n=5):
		similar = sorted(self.implemented, key=lambda x: self.get_similarity(card, x))
		return similar[:best_n]

	def get_similarity(self, card1, card2):
		cards = list(sorted([card1, card2], key=lambda c: c.id))

		key = (cards[0], cards[1])
		if key in self.levenshtein_cache:
			return self.levenshtein_cache[key]
		else:
			self.levenshtein_cache[key] = levenshtein(clean_text(cards[0].description),
													  clean_text(cards[1].description))
			return self.levenshtein_cache[key]

	def recommend_easy_cards(self, card_set, best_n=5):

		cards_in_set_filter = lambda x: x.card_set == card_set
		self.increase_levenshtein_cache(10, cards_in_set_filter)

		cards = list(filter(cards_in_set_filter, self.levenshtein_cache_full_cards))
		print(cards)
		best_cards = sorted(cards,
							key=lambda x: max([self.get_similarity(x, t) for t in self.implemented])
							)[:best_n]

		return best_cards


def main():
	helper = CardImplementationHelper()
	globalstrings = load_globalstrings()

	print("Interested in implementing some cards?\nTry some of these standard card sets:")
	standard_card_sets = list(filter(lambda x: x.is_standard, list(CardSet)))

	for i, cardset in enumerate(standard_card_sets):
		print("{} - {}".format(i + 1, globalstrings[cardset.name_global]['TEXT']))

	cardset_selection = int(input("Select a Card Set (1-{}): ".format(len(list(standard_card_sets)))))

	card_set = standard_card_sets[cardset_selection - 1]

	best_cards = helper.recommend_easy_cards(card_set)

	print("The following card might be easy to implement due to high similarity with existing implementations:")

	for card in best_cards:
		print("{}: {}".format(card.id, clean_text(card.description)))

	card = helper.search_card()

	similar = helper.get_similar_descriptions(card)

	for c in similar:
		print("{}: {}".format(c.id, clean_text(c.description)))
		script = get_script_definition(c.id)
		lines = inspect.getsourcelines(script)
		print("".join(lines[0]))

	template = "\nclass {id}:\n\t\"{name}\"\n\tplay = None".format(id=card.id, name=card.name)

	print(template)


if __name__ == '__main__':
	main()
