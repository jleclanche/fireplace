import string
import sys
import re

if __name__ == "__main__":
	sys.path.append("..")

from implemented import resolve_implemented_cards
from fireplace import cards


def cleanhtml(raw_html):
	cleanr = re.compile('<.*?>')
	cleantext = re.sub(cleanr, '', raw_html)
	return cleantext


def clean_text(text):
	text = cleanhtml(text)
	text = text.replace('\n', ' ')
	text = text.replace('_', ' ')
	# text = text.replace('\'s', '')
	# text = text.replace('@', '')
	text = text.replace('\'', '')
	text = text.replace('\"', '')
	text = text.replace(']', ' ')
	# text = text.replace('\'re', '')

	text = text.translate(str.maketrans('', '', '@.,:;[]()!’-'))

	return text


def levenshtein(a, b):
	"Calculates the Levenshtein distance between a and b."
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


def main():
	helper = CardImplementationHelper()
	print("Some unimplemented cards: ", end="")
	print(list(filter(lambda x: x.card_set.is_standard, helper.unimplemented))[:10])
	card = helper.search_card()

	# script = get_script_definition(card.id)


	distances = sorted(helper.implemented, key=lambda x: levenshtein(clean_text(x.description), clean_text(card.description)))[:10]

	print(*["{}: {}".format(c.id, clean_text(c.description)) for c in distances], sep='\n')


	template = "class {id}:\n" \
			   "\t\"{name}\n\t{description}\"\n\tplay = None".format(id=card.id, name=card.name,
																	 description=card.description.replace("\n", ""))

	print(template)


if __name__ == '__main__':
	main()
