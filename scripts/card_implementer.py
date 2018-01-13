import sys

if __name__ == "__main__":
	sys.path.append("..")

from implemented import resolve_implemented_cards
from fireplace import cards


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
	print(list(filter(lambda x: x.card_set.is_standard, helper.unimplemented))[:])
	card = helper.search_card()

	# script = get_script_definition(card.id)
	# globalstrings = load_globalstrings()

	template = "class {id}:\n" \
			   "\t\"{name}\n\t{description}\"\n\tplay = None".format(id=card.id, name=card.name,
																	 description=card.description.replace("\n", ""))

	print(template)


if __name__ == '__main__':
	main()
