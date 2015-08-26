#!/usr/bin/env python
import json
import logging
import random
import socketserver
import struct
import sys
from argparse import ArgumentParser
from fireplace.enums import CardType, GameTag, OptionType, Zone
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

	def action(self, type, args):
		pass

	def action_end(self, type, args):
		pass

	def add_to_state(self, entity):
		state = self.game_state[entity.entity_id] = {}
		for tag, value in entity.tags.items():
			if not value:
				continue
			if isinstance(value, str):
				continue
			state[tag] = int(value)

		zone_pos = self.get_zone_position(entity)
		if zone_pos:
			state[GameTag.ZONE_POSITION] = zone_pos

		# Don't have a way of getting entities by ID in fireplace yet
		state[GameTag.ENTITY_ID] = entity

	def refresh_state(self, entity_id):
		assert entity_id in self.game_state
		state = self.game_state[entity_id]
		entity = state[GameTag.ENTITY_ID]

		for tag, value in entity.tags.items():
			if isinstance(value, str):
				continue
			if not value:
				if state.get(tag, 0):
					self.tag_change(entity, tag, 0)
					del state[tag]
			elif int(value) != state.get(tag, 0):
				self.tag_change(entity, tag, int(value))
				state[tag] = int(value)

		zone_pos = self.get_zone_position(entity)
		if zone_pos != state.get(GameTag.ZONE_POSITION):
			if zone_pos:
				state[GameTag.ZONE_POSITION] = zone_pos
			else:
				del state[GameTag.ZONE_POSITION]
			self.tag_change(entity, GameTag.ZONE_POSITION, zone_pos)

	def refresh_options(self):
		self.options = [{"Type": OptionType.END_TURN}]
		payload = {
			"Type": "Options",
			"Options": self.options,
		}
		self.queued_data.append(payload)

	def get_zone_position(self, entity):
		if entity.zone == Zone.HAND:
			return entity.controller.hand.index(entity) + 1
		elif entity.zone == Zone.PLAY:
			if entity.type == CardType.MINION:
				return entity.controller.field.index(entity) + 1
			else:
				return 1

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

	def process_send_option(self, data):
		option = self.options[data["Index"]]
		if option["Type"] == OptionType.END_TURN:
			self.game.end_turn()
		else:
			raise NotImplementedError

	def tag_change(self, entity, tag, value):
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
			for entity in manager.game_state:
				manager.refresh_state(entity)
			manager.refresh_options()
			self.send_payload(manager)
			packet = self.read_packet()
			if packet is None:
				break

			if packet["Type"] == "SendOption":
				manager.process_send_option(packet["SendOption"])
			else:
				raise NotImplementedError

			self.send_payload(manager)

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

	def create_game(self, payload):
		# self.game_id = payload["GameID"]
		player_data = payload["Players"]
		players = []
		for player in player_data:
			p = Player(player["Name"])
			# Shuffle the cards to prevent information leaking
			cards = player["Cards"]
			random.shuffle(cards)
			p.prepare_deck(cards, player["Hero"])
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


def main():
	arguments = ArgumentParser(prog="kettle")
	arguments.add_argument("hostname", default="127.0.0.1", nargs="?")
	arguments.add_argument("port", type=int, default=9111, nargs="?")
	args = arguments.parse_args(sys.argv[1:])

	INFO("Listening on %s:%i..." % (args.hostname, args.port))
	socketserver.TCPServer.allow_reuse_address = True
	kettle = socketserver.TCPServer((args.hostname, args.port), Kettle)
	kettle.serve_forever()

	return 0


if __name__ == "__main__":
	exit(main())
