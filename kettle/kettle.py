#!/usr/bin/env python
import json
import logging
import random
import socketserver
import struct
import sys
from argparse import ArgumentParser
from hearthstone.enums import (
	CardType, ChoiceType, GameTag, OptionType, Step, Zone
)
from fireplace import actions, cards
from fireplace.exceptions import GameOver
from fireplace.game import BaseGame as Game
from fireplace.player import Player
from fireplace.utils import CardList


logging.basicConfig(level=logging.DEBUG)
KettleLogger = logging.getLogger("kettle")
KettleLogger.setLevel(logging.DEBUG)
INFO = KettleLogger.info
WARN = KettleLogger.warn
DEBUG = KettleLogger.debug


class KettleSerializer(json.JSONEncoder):
	def default(self, o):
		if isinstance(o, CardList):
			return len(o)
		return int(o)


class KettleManager:
	def __init__(self, game):
		self.game = game
		self.game_state = {}
		self.queued_data = []

	def action_start(self, type, source, index, target):
		DEBUG("Beginning new action %r (%r, %r, %r)", type, source, index, target)
		# prevent unprocessed updates appearing inside the block
		# this may happen if queued tag changes are outside of blocks
		self.refresh_full_state()
		packet = {
			"SubType": type,
			"EntityID": source.entity_id,
			"Index": index,
			"Target": target.entity_id if target else 0,
		}
		payload = {"Type": "ActionStart", "ActionStart": packet}
		self.queued_data.append(payload)

	def action_end(self, type, source):
		DEBUG("Ending action %r", type)
		self.refresh_full_state()
		payload = {"Type": "ActionEnd"}
		self.queued_data.append(payload)

	def game_step(self, step, next_step):
		DEBUG("Game.STEP changes to %r (next step is %r)", step, next_step)
		self.refresh_full_state()

	def add_to_state(self, entity):
		state = self.game_state[entity.entity_id] = {}
		for tag, value in entity.tags.items():
			if not value:
				continue
			if isinstance(value, str):
				continue
			state[tag] = int(value)

		# Don't have a way of getting entities by ID in fireplace yet
		state[GameTag.ENTITY_ID] = entity

	def refresh_tag(self, entity, tag):
		state = self.game_state[entity.entity_id]
		value = entity.tags.get(tag, 0)
		if isinstance(value, str):
			return
		if not value:
			if state.get(tag, 0):
				self.tag_change(entity, tag, 0)
				del state[tag]
		elif int(value) != state.get(tag, 0):
			self.tag_change(entity, tag, int(value))
			state[tag] = int(value)

	def refresh_full_state(self):
		if self.game.step < Step.BEGIN_MULLIGAN:
			return
		for entity in self.game:
			if entity.entity_id in self.game_state:
				self.refresh_state(entity.entity_id)

	def refresh_state(self, entity_id):
		assert entity_id in self.game_state
		entity = self.game_state[entity_id][GameTag.ENTITY_ID]
		state = self.game_state[entity.entity_id]

		for tag in entity.tags:
			self.refresh_tag(entity, tag)

	def get_options(self, entity):
		ret = []
		if entity.zone == Zone.HAND:
			if entity.type in (CardType.SPELL, CardType.MINION, CardType.WEAPON):
				if entity.is_playable():
					ret.append({
						"Type": OptionType.POWER,
						"MainOption": {
							"ID": entity,
							"Targets": entity.targets,
						},
					})

		elif entity.zone == Zone.PLAY:
			if entity.type == CardType.HERO_POWER:
				if entity.is_usable():
					ret.append({
						"Type": OptionType.POWER,
						"MainOption": {
							"ID": entity,
							"Targets": entity.targets,
						}
					})
			elif entity.type in (CardType.HERO, CardType.MINION):
				if entity.can_attack():
					ret.append({
						"Type": OptionType.POWER,
						"MainOption": {
							"ID": entity,
							"Targets": entity.attack_targets,
						}
					})

		return ret

	def refresh_choices(self):
		choice = self.game.current_player.choice
		DEBUG("Queuing choice %r (cards: %r)", choice, choice.cards)
		self.choices = {
			"ChoiceType": ChoiceType.GENERAL,
			"CountMin": choice.min_count,
			"CountMax": choice.max_count,
			"Entities": [e.entity_id for e in choice.cards],
			"Source": choice.source.entity_id,
			"PlayerId": 1,
		}
		for show_choice in choice.cards:
			self.refresh_state(show_choice.entity_id)
			self.queued_data.append(self.show_entity(show_choice))
		payload = {"Type": "EntityChoices", "EntityChoices": self.choices}
		self.queued_data.append(payload)

	def refresh_options(self):
		DEBUG("Refreshing options...")
		if self.game.current_player.choice:
			return self.refresh_choices()
		self.options = [{"Type": OptionType.END_TURN}]

		for entity in self.game.current_player.actionable_entities:
			for option in self.get_options(entity):
				self.options.append(option)

		payload = {
			"Type": "Options",
			"Options": self.options,
		}
		self.queued_data.append(payload)

	def new_entity(self, entity):
		self.add_to_state(entity)
		if isinstance(entity, Player):
			payload = self.player_entity(entity)
		else:
			payload = self.full_entity(entity)
		self.queued_data.append(payload)

	def start_game(self):
		self.add_to_state(self.game)
		self.queued_data.append(self.game_entity(self.game))

	def get_entity(self, id):
		if not id:
			return None
		return self.game_state[id][GameTag.ENTITY_ID]

	def process_send_option(self, data):
		DEBUG("Processing send option, data=%r", data)
		option = self.options[data["Index"]]
		if option["Type"] == OptionType.END_TURN:
			self.game.end_turn()
		elif option["Type"] == OptionType.POWER:
			entity = option["MainOption"]["ID"]
			kwargs = {
				"target": self.get_entity(data["Target"]),
			}
			DEBUG("Using POWER entity %r **%r", entity, kwargs)
			DEBUG("data=%r", data)
			if entity.zone == Zone.HAND:
				func = entity.play
				kwargs["index"] = data["Position"]
			elif entity.zone == Zone.PLAY:
				if entity.type == CardType.HERO_POWER:
					func = entity.use
				elif entity.type in (CardType.HERO, CardType.MINION):
					func = entity.attack
			func(**kwargs)
		else:
			raise NotImplementedError

	def process_choose_entities(self, data):
		DEBUG("Processing choose entities, data=%r", data)
		entities = []
		for entity_id in data:
			# No need to assert, fireplace will raise InvalidAction
			# assert entity_id in self.choices["Entities"]
			entities.append(self.get_entity(entity_id))
		self.game.current_player.choice.choose(*entities)

	def tag_change(self, entity, tag, value):
		if tag < 0:
			return
		DEBUG("Queueing a tag change for entity %r: %r -> %r", entity, tag, value)
		payload = {
			"Type": "TagChange",
			"TagChange": {
				"EntityID": entity.entity_id,
				"Tag": tag,
				"Value": value,
			}
		}
		self.queued_data.append(payload)

	def game_entity(self, game):
		return {
			"Type": "GameEntity",
			"GameEntity": {
				"EntityID": game.entity_id,
				"Tags": self.game_state[game.entity_id],
			}
		}

	def player_entity(self, player):
		return {
			"Type": "Player",
			"Player": {
				"EntityID": player.entity_id,
				"Tags": self.game_state[player.entity_id],
			}
		}

	def full_entity(self, entity):
		return {
			"Type": "FullEntity",
			"FullEntity": {
				"CardID": entity.id,
				"EntityID": entity.entity_id,
				"Tags": self.game_state[entity.entity_id],
			}
		}

	def show_entity(self, entity):
		return {
			"Type": "ShowEntity",
			"FullEntity": {
				"CardID": entity.id,
				"EntityID": entity.entity_id,
				"Tags": self.game_state[entity.entity_id],
			}
		}


class Kettle(socketserver.BaseRequestHandler):
	def handle(self):
		data = self.read_packet()
		data = data[0]
		query_type = data["Type"]
		payload = data[query_type]
		DEBUG("Got payload %r", payload)
		assert query_type == "CreateGame"

		self.serializer = KettleSerializer()
		manager = self.create_game(payload)

		while True:
			manager.refresh_full_state()
			manager.refresh_options()
			self.send_payload(manager)
			packet = self.read_packet()
			if packet is None:
				break
			try:
				self.process_packet(packet, manager)
			except GameOver:
				break

		# send final power history delta
		manager.refresh_full_state()
		self.send_payload(manager)
		self.request.close()

	def read_packet(self):
		header = self.request.recv(4)
		if not header:
			return None
		body_size, = struct.unpack("<i", header)
		data = self.request.recv(body_size)
		DEBUG("Got data %r", data)
		return json.loads(data.decode("utf-8"))

	def send_payload(self, manager):
		serialized = self.serializer.encode(manager.queued_data).encode("utf-8")
		manager.queued_data = []
		response_payload = struct.pack("<i", len(serialized)) + serialized
		DEBUG("Sending %r" % (response_payload))
		self.request.sendall(response_payload)

	def process_packet(self, packet, manager):
		if packet["Type"] == "SendOption":
			# throws GameOver when game ends
			manager.process_send_option(packet["SendOption"])
		elif packet["Type"] == "ChooseEntities":
			manager.process_choose_entities(packet["ChooseEntities"])
		elif packet["Type"] == "Concede":
			player = manager.game.players[packet["Concede"] - 1]
			player.concede()
			manager.refresh_full_state()
		else:
			raise NotImplementedError
		self.send_payload(manager)

	def create_game(self, payload):
		# self.game_id = payload["GameID"]
		player_data = payload["Players"]
		players = []
		for player in player_data:
			# Shuffle the cards to prevent information leaking
			cards = player["Cards"]
			random.shuffle(cards)
			p = Player(player["Name"], cards, player["Hero"])
			players.append(p)

		INFO("Initializing a Kettle game with players=%r", players)
		game = Game(players=players)
		manager = KettleManager(game)
		game.manager.register(manager)
		game.current_player = game.players[0]  # Dumb.
		game.start()

		# Skip mulligan
		for player in game.players:
			player.choice = None

		return manager


class KettleServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
	daemon_threads = True
	allow_reuse_address = True


def main():
	arguments = ArgumentParser(prog="kettle")
	arguments.add_argument("hostname", default="127.0.0.1", nargs="?")
	arguments.add_argument("port", type=int, default=9111, nargs="?")
	args = arguments.parse_args(sys.argv[1:])

	cards.db.initialize()

	INFO("Listening on %s:%i..." % (args.hostname, args.port))
	kettle = KettleServer((args.hostname, args.port), Kettle)
	try:
		kettle.serve_forever()
	except KeyboardInterrupt:
		sys.exit(0)

	return 0


if __name__ == "__main__":
	exit(main())
