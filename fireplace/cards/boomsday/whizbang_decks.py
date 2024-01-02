from hearthstone.deckstrings import Deck

from .. import db


# Where can I find a list of all the current Whizbang decks?

# These decks are from
# https://www.hearthpwn.com/decks/1163078-all-whizbang-decks-for-your-decktracker

WHIZBANG_DECK_STRINGS = [
	"AAECAQcIqgbTwwKZxwLN7wKb8AKe+AKO+wKggAMLS5EDogT/B5vCAsrDAqLHAsrnAqrsArrsAvLxAgA=",
	"AAECAQcEze8Cm/ACkvgCoIADDZEGzM0CuuwCnfACl/MCn/UCpfUC5PcCjvgCg/sCqPsCs/wCzIEDAA==",
	"AAECAaoICooB7QXAB8/HApvLAsLOAqrsAqfuAoH2Ap79AgqBBPUE/gX/BcfBAvPnApbvAvbwAoqAA5eAAwA=",
	"AAECAaoIBMAH88ICofgCmfsCDb0B+QOGBvAHkwnrwgKw8AL28AKz9wLq+gKP+wKc/wKKgAMA",
	"AAECAaIHBLICgNMC6/ACqPcCDbQBywObBYYJgcIC68ICm8gC5dEC2+MC6vMCt/UCovcCx/gCAA==",
	"AAECAaIHCIwC7QX7BeXRAs/hAvDmAtjpAp/4Agu0AYHCAqvCAuvCAtvjAurmArT2At76Auz8Avb9AtGBAwA=",
	"AAECAZ8FBvoGucEC4fACzfQC6/cC/fsCDNwD9AXPBq8HsQizwQKIxwLZxwKbywK35wL27ALZ/gIA",
	"AAECAZ8FBvQFzwb6BrnBAvH+AqCAAwzcA48Js8EC48sCn/UCpfUC1v4C2f4C4f4CkYAD0YADzIEDAA==",
	"AAECAR8EhwTp0gKG0wLy6gINjQGoArUDyQSXCNsJ/gzd0gLf0gLj0gLh4wLq4wKH+wIA",
	"AAECAR8C4fUCoIADDo0Bigbh4wKf9QLg9QLi9QLv9QKZ9wK5+AKR+wKY+wKE/QL2/QLMgQMA",
	"AAECAZICBMnCAofOAsLOApnTAg1AX8QG5AiU0gKY0gKo0gKL4QKE5gKL5gL15wLf+wLo/AIA",
	"AAECAZICAiTF/QIO/QLtA/cD5gWxCIbBAqTCAuvCAtfvAsHzAt/7AuH7Ar/9AtWDAwA=",
	"AAECAf0GApfTApz4Ag6KAbYHxAjnywLy0AL40AKI0gL85QLq5gLo5wK38QLF8wL8+gKPgAMA",
	"AAECAf0GApfTAo+CAw4w9wTCCPYIm8sC980C8dAC8tAC9PcC0/gCqvkCt/0Cw/0C+v4CAA==",
	"AAECAf0EBNACvwib0wKj6wINTYoByQPsB/sMysMClscCx8cC29MC1eEC1+ECluQC1+sCAA==",
	"AAECAf0EAqLTAu72Ag67ApUDvwOrBLQElgW/wQL77AKS7wK89wKj/QKV/wK5/wLvgAMA",
	"AAECAa0GBMnCApbEAsv4Ao2CAw37AeUE0wryDKvCAubMAvDPAujQAovhAoL3AqH+AvX+AoiCAwA=",
	"AAECAa0GBKIJvsgC2OMCy/gCDfgC5QSNCNEK8gzRwQLYwQLL5gKC9wLl9wL1/gLxgAPeggMA",
]


def decode(deckstring: str):
	deck = Deck.from_deckstring(deckstring)
	hero_id = deck.heroes[0]
	hero_id = db.dbf[hero_id]
	cards = []
	for card_id, num in deck.cards:
		card_id = db.dbf[card_id]
		cards += [card_id] * num
	return hero_id, cards


if "WHIZBANG_DECKS" not in globals():
	WHIZBANG_DECKS = [decode(code) for code in WHIZBANG_DECK_STRINGS]
