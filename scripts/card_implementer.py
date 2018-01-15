import re
import sys

if __name__ == "__main__":
	sys.path.append("..")

from implemented import resolve_implemented_cards
from fireplace import cards


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

	def search_card(self):

		while True:
			matching_cards = []
			searchstr = input("Enter a card ID: ")
			try:
				return cards.db[searchstr]
			except KeyError:
				print("Card not found. Please try again")

	def get_similar_descriptions(self, card, best_n=5):
		similar = sorted(self.implemented,
						 key=lambda x: levenshtein(clean_text(x.description), clean_text(card.description)))

		return similar[:best_n]


def main():
	helper = CardImplementationHelper()
	print("Some unimplemented cards: ", end="")
	print(list(filter(lambda x: x.card_set.is_standard, helper.unimplemented))[:10])
	card = helper.search_card()

	similar = helper.get_similar_descriptions(card)
	print(*["{}: {}".format(c.id, clean_text(c.description)) for c in similar], sep='\n')


	template = "\nclass {id}:\n" \
			   "\t\"{name}\n\t{description}\"\n\tplay = None".format(id=card.id, name=card.name,
																	 description=card.description.replace("\n", ""))

	print(template)


if __name__ == '__main__':
	main()
