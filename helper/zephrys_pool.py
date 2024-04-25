from fireplace.cards import db
from hearthstone.enums import CardSet

db.initialize()

ids = db.filter(card_set=[CardSet.BASIC, CardSet.EXPERT1], collectible=True)
cards = []
for id in ids:
    cards.append(db[id])
cards.sort(key=lambda card: card.cost)
for card in cards:
    print(
        card.id,
        card.name,
        (card.cost, card.atk, card.health),
        card.description.replace("\n", ""),
    )
