#!/usr/bin/env python
import json
import logging
import random
import socketserver
import struct
import sys
from argparse import ArgumentParser
from fireplace.game import Game
from fireplace.entity import Entity
from fireplace.player import Player


logging.basicConfig(level=logging.DEBUG)
KettleLogger = logging.getLogger("kettle")
KettleLogger.setLevel(logging.DEBUG)
INFO = KettleLogger.info
WARN = KettleLogger.warn
DEBUG = KettleLogger.debug


class KettleManager:
	def __init__(self, game):
		self.game = game
		self.queued_data = []

	def action(self, type, args):
		pass

	def action_end(self, type, args):
		pass

	def new_entity(self, entity):
		if isinstance(entity, Player):
			payload = self.player_entity(entity)
		else:
			payload = self.full_entity(entity)
		self.queued_data.append(payload)

	def start_game(self):
		self.queued_data.append(self.game_entity(self.game))

	def game_entity(self, game):
		return {
			"Type": "GameEntity",
			"GameEntity": {
				"EntityID": game.manager.id,
				"Tags": Kettle._serialize_tags(game.tags),
			}
		}

	def player_entity(self, player):
		return {
			"Type": "Player",
			"Player": {
				"EntityID": player.manager.id,
				"Tags": Kettle._serialize_tags(player.tags),
			}
		}

	def full_entity(self, entity):
		return {
			"Type": "FullEntity",
			"FullEntity": {
				"CardID": entity.id,
				"EntityID": entity.manager.id,
				"Tags": Kettle._serialize_tags(entity.tags),
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

		manager = self.create_game(payload)
		self.send_payload(manager)

		while True:
			data = self.read_packet()
			raise NotImplementedError
			self.send_payload(manager)

	def read_packet(self):
		header = self.request.recv(4)
		body_size, = struct.unpack("<i", header)
		data = self.request.recv(body_size)
		return json.loads(data.decode("utf-8"))

	def send_payload(self, manager):
		serialized = json.dumps(manager.queued_data).encode("utf-8")
		manager.queued_data = []
		response_payload = struct.pack("<i", len(serialized)) + serialized
		DEBUG("Sending %r" % (response_payload))
		self.request.sendall(response_payload)

	@staticmethod
	def _serialize_tags(tags):
		ret = {}
		for k, v in tags.items():
			if not v:
				# Do not send empty tags
				continue
			if isinstance(v, (Entity, bool)):
				v = int(v)
			elif isinstance(v, str):
				# Skip string tags
				continue
			elif not isinstance(v, int):
				WARN("Skipping serialization on tag %r = %r", k, v)
				continue
			ret[int(k)] = v
		return ret

	def create_game(self, payload):
		self.game_id = payload["GameID"]
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
		game.start()

		return manager


def main():
	arguments = ArgumentParser(prog="kettle")
	arguments.add_argument("hostname", default="127.0.0.1", nargs="?")
	arguments.add_argument("port", type=int, default=9111, nargs="?")
	args = arguments.parse_args(sys.argv[1:])

	INFO("Listening on %s:%i..." % (args.hostname, args.port))
	kettle = socketserver.TCPServer((args.hostname, args.port), Kettle)
	kettle.serve_forever()

	return 0


if __name__ == "__main__":
	exit(main())
