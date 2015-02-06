import os
from xml.etree import ElementTree
from fireplace.enums import GameTag, PlayReq


class CardXML(object):
	def __init__(self, xml):
		self.xml = xml

	@property
	def id(self):
		return self.xml.attrib["CardID"]

	@property
	def entourage(self):
		cards = self.xml.findall("EntourageCard")
		return [tag.attrib["cardID"] for tag in cards]

	@property
	def requirements(self):
		reqs = self.xml.findall("Power[PlayRequirement]/PlayRequirement")
		return {PlayReq(int(tag.attrib["reqID"])): int(tag.attrib["param"] or 0) for tag in reqs}

	@property
	def name(self):
		return self.getTag(GameTag.CARDNAME)

	@property
	def description(self):
		return self.getTag(GameTag.CARDTEXT_INHAND) or ""

	def _findTag(self, id):
		return self.xml.findall('./Tag[@enumID="%i"]' % (id))

	def _getTag(self, element):
		type = element.attrib["type"]
		if type == "String":
			return element.text

		value = int(element.attrib["value"])
		if type == "Bool":
			return bool(value)
		return value

	def getTag(self, id):
		element = self._findTag(id)
		if not element:
			return 0
		return self._getTag(element[0])

	@property
	def tags(self):
		return {GameTag(int(e.attrib["enumID"])): self._getTag(e) for e in self.xml.findall("./Tag")}

	##
	# Requirement properties

	def _reqParam(self, req):
		tags = self.xml.findall("Power/PlayRequirement[@reqID='%i']" % (req))
		if tags:
			return int(tags[0].attrib["param"])
		return 0

	@property
	def minMinions(self):
		return self._reqParam(PlayReq.REQ_MINIMUM_TOTAL_MINIONS)

	@property
	def minTargets(self):
		return self._reqParam(PlayReq.REQ_MINIMUM_ENEMY_MINIONS)

	@property
	def targetMaxAttack(self):
		return self._reqParam(PlayReq.REQ_TARGET_MAX_ATTACK)

	@property
	def targetMinAttack(self):
		return self._reqParam(PlayReq.REQ_TARGET_MIN_ATTACK)

	@property
	def targetRace(self):
		race = self._reqParam(PlayReq.REQ_TARGET_WITH_RACE)
		if race:
			return Race(race)


def load(path):
	db = {}
	with open(path, "r") as f:
		xml = ElementTree.parse(f)
		for carddata in xml.findall("Entity"):
			card = CardXML(carddata)
			db[card.id] = card
	return db, xml
