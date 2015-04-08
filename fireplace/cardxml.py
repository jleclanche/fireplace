import os
from xml.etree import ElementTree
from fireplace.enums import CardType, GameTag, PlayReq, Race, Rarity, Zone


class CardXML(object):
	def __init__(self, xml):
		self.xml = xml

	def __str__(self):
		return self.name

	def __repr__(self):
		return "<%s: %r>" % (self.id, self.name)

	def _getRequirements(self, reqs):
		return {PlayReq(int(tag.attrib["reqID"])): int(tag.attrib["param"] or 0) for tag in reqs}

	@property
	def id(self):
		return self.xml.attrib["CardID"]

	@property
	def name(self):
		return self.getTag(GameTag.CARDNAME)

	@property
	def description(self):
		return self.getTag(GameTag.CARDTEXT_INHAND) or ""

	@property
	def cardClass(self):
		return self.getTag(GameTag.CLASS)

	@property
	def collectible(self):
		return bool(self.getTag(GameTag.Collectible))

	@property
	def cost(self):
		return self.getTag(GameTag.COST)

	@property
	def race(self):
		return Race(self.getTag(GameTag.CARDRACE))

	@property
	def rarity(self):
		return Rarity(self.getTag(GameTag.RARITY))

	@property
	def type(self):
		return CardType(self.getTag(GameTag.CARDTYPE))

	@property
	def auras(self):
		cards = self.xml.findall("Aura")
		ret = []
		for tag in cards:
			aura = {"id": tag.attrib["cardID"]}
			aura["requirements"] = self._getRequirements(tag.findall("ActiveRequirement"))
			aura["player"] = tag.attrib.get("player", False)
			aura["zone"] = Zone(int(tag.attrib.get("zone", Zone.PLAY)))
			ret.append(aura)
		return ret

	@property
	def chooseCards(self):
		cards = self.xml.findall("ChooseCard")
		return [tag.attrib["cardID"] for tag in cards]

	@property
	def entourage(self):
		cards = self.xml.findall("EntourageCard")
		return [tag.attrib["cardID"] for tag in cards]

	@property
	def heroPower(self):
		e = self.xml.findall("HeroPower")
		if e:
			return e[0].attrib["cardID"]

	@property
	def requirements(self):
		reqs = self.xml.findall("Power[PlayRequirement]/PlayRequirement")
		return self._getRequirements(reqs)

	@property
	def powerUpRequirements(self):
		reqs = self.xml.findall("PowerUpRequirement")
		return [Race(int(tag.attrib["param"])) for tag in reqs]

	def _findTag(self, id):
		return self.xml.findall('./Tag[@enumID="%i"]' % (id))

	def _getTag(self, element):
		type = element.attrib.get("type", "Int")

		if type == "Card":
			return element.attrib["value"]

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

	@property
	def enrageTags(self):
		return {GameTag(int(e.attrib["enumID"])): self._getTag(e) for e in self.xml.findall("./EnrageDefinition/Tag")}


def load(path):
	db = {}
	with open(path, "r") as f:
		xml = ElementTree.parse(f)
		for carddata in xml.findall("Entity"):
			card = CardXML(carddata)
			db[card.id] = card
	return db, xml
