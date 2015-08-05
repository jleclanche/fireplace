#!/usr/bin/env python

import os
import re
import sys; sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))
from xml.dom import minidom
from xml.etree import ElementTree
from fireplace.enums import AuraType, GameTag
import buffs
import chooseone
import enrage
import missing_cards
import powerups


italicize = [
	"EX1_345t",  # Shadow of Nothing
	"TU4c_005",  # Hidden Gnome
	"TU4c_007",  # Mukla's Big Brother
	"GAME_006",  # NOOOOOOOOOOOO
	"PlaceholderCard",  # Placeholder Card
]


def add_chooseone_tags(card, ids):
	for id in ids:
		e = ElementTree.Element("ChooseCard")
		e.attrib["cardID"] = id
		card.xml.append(e)
	print("%s: Adding Choose One cards: %r" % (card.name, ids))


def add_enrage_definition(card, tags):
	definition = ElementTree.Element("EnrageDefinition")
	for tag, value in tags.items():
		e = _create_tag(tag, value)
		definition.append(e)
	card.xml.append(definition)


def add_hero_power(card, id):
	e = ElementTree.Element("HeroPower")
	e.attrib["cardID"] = id
	card.xml.append(e)
	print("%s: Adding hero power %r" % (card, id))


def add_powerup_requirements(card, race):
	req = ElementTree.Element("PowerUpRequirement")
	req.attrib["reqID"] = "1"
	req.attrib["param"] = str(int(race))
	card.xml.append(req)
	print("%s: Adding POWERED_UP definition of %r" % (card.name, race))


def guess_spellpower(card):
	sre = re.search(r"Spell Damage \+(\d+)", card.description)
	dmg = int(sre.groups()[0])
	e = card._findTag(GameTag.SPELLPOWER)
	if not e:
		print("WARNING: No SPELLPOWER tag found on %r" % (card))
		return
	e[0].attrib["value"] = str(dmg)
	e[0].attrib["type"] = "Number"
	print("%s: Setting Spell Power to %i" % (card.name, dmg))


def guess_overload(card):
	sre = re.search(r"Overload[^(]+\((\d+)\)", card.description)
	amount = int(sre.groups()[0])
	e = card._findTag(GameTag.RECALL)
	if not e:
		print("WARNING: No RECALL tag found on %r" % (card))
		return
	e[0].attrib["value"] = str(amount)
	print("%s: Setting Overload to %i" % (card.name, amount))


def create_card(id, card):
	e = ElementTree.Element("Entity")
	e.attrib["CardID"] = id
	for tag, value in card.items():
		e.append(_create_tag(tag, value))
	return e

def _create_tag(tag, value):
	e = ElementTree.Element("Tag")
	if isinstance(value, bool):
		e.attrib["value"] = "1" if value else "0"
		e.attrib["type"] = "Bool"
	elif isinstance(value, int):
		e.attrib["value"] = str(int(value))
		e.attrib["type"] = "Int"
	elif isinstance(value, str):
		e.text = value
		e.attrib["type"] = "String"
	else:
		raise NotImplementedError(value)
	e.attrib["enumID"] = str(int(tag))
	return e


def set_tag(card, tag, value):
	e = _create_tag(tag, value)
	card.xml.append(e)
	print("%s: Setting %r = %r" % (card.name, tag, value))
	return e


def remove_tag(card, tag):
	e = card._findTag(tag)[0]
	card.xml.remove(e)
	print("%s: Removing %r tag" % (card.name, tag))


def load_dbf(path):
	db = {}
	hero_powers = {}
	with open(path, "r") as f:
		xml = ElementTree.parse(f)
		for record in xml.findall("Record"):
			id = int(record.find("./Field[@column='ID']").text)
			guid = record.find("./Field[@column='NOTE_MINI_GUID']").text
			hero_power_id = int(record.find("./Field[@column='HERO_POWER_ID']").text)

			db[id] = guid
			if hero_power_id:
				hero_powers[guid] = hero_power_id

	for k, v in hero_powers.items():
		hero_powers[k] = db[v]

	# Some hero powers are missing from the DBF, wtf :(
	missing = {
		"EX1_323h": "EX1_tk33",
	}

	for k, v in missing.items():
		assert k not in hero_powers
		hero_powers[k] = v

	return db, hero_powers


def main():
	from fireplace.cardxml import load

	if len(sys.argv) < 3:
		print("Usage: %s <in> <out/CardDefs.xml>")
		exit(1)

	db, xml = load(os.path.join(sys.argv[1], "CardDefs.xml"))
	dbf, hero_powers = load_dbf(os.path.join(sys.argv[1], "DBF", "CARD.xml"))
	for id, card in db.items():
		if hasattr(buffs, id):
			for tag, value in getattr(buffs, id).items():
				set_tag(card, tag, value)

		if hasattr(chooseone, id):
			add_chooseone_tags(card, getattr(chooseone, id))

		if hasattr(enrage, id):
			add_enrage_definition(card, getattr(enrage, id))

		if id in hero_powers:
			add_hero_power(card, hero_powers[id])

		if hasattr(powerups, id):
			add_powerup_requirements(card, getattr(powerups, id))

		if re.match(r"^PART_\d+$", id):
			# Hearthstone uses entourage data to identify Spare Parts
			# We're better than that.
			set_tag(card, GameTag.SPARE_PART, True)

		if card.tags.get(GameTag.SPELLPOWER):
			guess_spellpower(card)

		if card.tags.get(GameTag.RECALL):
			guess_overload(card)

		if "Can't Attack." in card.description:
			set_tag(card, GameTag.CANT_ATTACK, True)

		if "Can't be targeted by spells or Hero Powers." in card.description:
			set_tag(card, GameTag.CANT_BE_TARGETED_BY_ABILITIES, True)
			set_tag(card, GameTag.CANT_BE_TARGETED_BY_HERO_POWERS, True)

		if "Always wins Brawls." in card.description:
			set_tag(card, GameTag.ALWAYS_WINS_BRAWLS, True)

		if id in italicize:
			description = card.description
			assert description and not description.startswith("<i>")
			print("%s: Italicizing description %r" % (id, description))
			e = card._findTag(GameTag.CARDTEXT_INHAND)
			for tag in e[0]:
				tag.text = "<i>%s</i>" % (tag.text)
			else:
				print("WARNING: No CARDTEXT_INHAND tag found on %r" % (card))

	# xml = db[next(db.__iter__())].xml
	with open(sys.argv[2], "w", encoding="utf8") as f:
		root = ElementTree.Element("CardDefs")
		for e in xml.findall("Entity"):
			# We want to retain the order so we can't just use db.keys()
			id = e.attrib["CardID"]
			card = db[id]
			root.append(card.xml)

		for id, obj in missing_cards.__dict__.items():
			if id.startswith("_") or not isinstance(obj, dict):
				# skip the imports
				continue
			e = create_card(id, obj)
			root.append(e)

		outstr = ElementTree.tostring(root)
		# Reparse for clean indentation
		outstr = minidom.parseString(outstr).toprettyxml(indent="\t")
		outstr = "\n".join(line for line in outstr.split("\n") if line.strip())
		f.write(outstr)
		print("Written to", f.name)


if __name__ == "__main__":
	main()
