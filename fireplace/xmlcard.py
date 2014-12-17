import os
from xml.etree import ElementTree
from .enums import GameTag, PlayReq, Race


_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir, "data", "TextAsset")


class XMLCard(object):
	_tags = {
		"charge": GameTag.CHARGE,
		"windfury": GameTag.WINDFURY,
	}

	_definitions = {
		"Atk": GameTag.ATK,
		"Health": GameTag.HEALTH,
		"Charge": GameTag.CHARGE,
		"Durability": GameTag.DURABILITY,
		"Recall": GameTag.RECALL,
		"Taunt": GameTag.TAUNT,
		"Deathrattle": GameTag.DEATH_RATTLE,
	}

	cantAttack = False

	def action(self):
		pass

	@classmethod
	def get(cls, id):
		from . import carddata
		if not hasattr(carddata, id):
			return cls(id)
		return getattr(carddata, id)(id)

	def __init__(self, id):
		self.file = os.path.join(_path, "%s.xml" % (id))
		self.xml = ElementTree.parse(self.file)

	def __getattribute__(self, name):
		parent = super()
		if name != "_tags" and name in self._tags:
			if hasattr(parent.__self_class__, name):
				return parent.__getattribute__(name)
			return self.getTag(self._tags[name])
		return parent.__getattribute__(name)

	def _reqParam(self, req):
		tags = self.xml.findall("Power/PlayRequirement[@reqID='%i']" % (req))
		if tags:
			return int(tags[0].attrib["param"])
		return 0

	def _getTag(self, element, locale="enUS"):
		type = element.attrib["type"]
		if type == "String":
			return element.find(locale).text

		value = int(element.attrib["value"])
		if type == "Bool":
			return bool(value)
		return value

	def getTag(self, id):
		element = self.xml.findall('./Tag[@enumID="%i"]' % (id))
		if not element:
			return 0
		return self._getTag(element[0])

	@property
	def tags(self):
		ret = {GameTag(int(e.attrib["enumID"])): self._getTag(e) for e in self.xml.findall("./Tag")}
		for attr, tag in self._definitions.items():
			if hasattr(self, attr):
				ret[tag] = getattr(self, attr)
		return ret

	@property
	def spellpower(self):
		# Game treats as a bool. We default to 1 if present.
		return int(getTag("Spellpower"))

	@property
	def name(self):
		return self.xml.findall("./Tag[@name='CardName']/enUS")[0].text

	@property
	def entourage(self):
		cards = self.xml.findall("EntourageCard")
		return [tag.attrib["cardID"] for tag in cards]

	@property
	def requirements(self):
		reqs = self.xml.findall("Power[PlayRequirement]/PlayRequirement")
		return {PlayReq(int(tag.attrib["reqID"])): tag.attrib["param"] for tag in reqs}

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
