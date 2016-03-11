#!/usr/bin/env python

import os
import re
import sys; sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from xml.dom import minidom
from xml.etree import ElementTree
from hearthstone.enums import GameTag


def add_hero_power(card, id):
	e = ElementTree.Element("HeroPower")
	e.attrib["cardID"] = id
	card.xml.append(e)
	print("%s: Adding hero power %r" % (card, id))


def create_card(id, tags):
	print("%s: Creating card with %r" % (id, tags))
	e = ElementTree.Element("Entity")
	e.attrib["CardID"] = id
	for tag, value in tags.items():
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


def main():
	from hearthstone.cardxml import load
	from fireplace.utils import _custom_cards, get_script_definition

	if len(sys.argv) < 3:
		print("Usage: %s <in> <out/CardDefs.xml>" % (sys.argv[0]))
		exit(1)

	db, xml = load(os.path.join(sys.argv[1], "CardDefs.xml"))

	# xml = db[next(db.__iter__())].xml
	path = os.path.realpath(sys.argv[2])
	with open(path, "w", encoding="utf8") as f:
		root = ElementTree.Element("CardDefs")
		for e in xml.findall("Entity"):
			# We want to retain the order so we can't just use db.keys()
			id = e.attrib["CardID"]
			card = db[id]
			root.append(card.xml)

		# dummy call
		get_script_definition("")

		# Create all registered custom cards
		for id, cls in _custom_cards.items():
			e = create_card(id, cls.tags)
			root.append(e)

		outstr = ElementTree.tostring(root)
		# Reparse for clean indentation
		outstr = minidom.parseString(outstr).toprettyxml(indent="\t")
		outstr = "\n".join(line for line in outstr.split("\n") if line.strip())
		f.write(outstr)
		print("Written to", path)


if __name__ == "__main__":
	main()
