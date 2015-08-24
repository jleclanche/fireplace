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
from fireplace.enums import GameTag


logging.basicConfig(level=logging.DEBUG)
KettleLogger = logging.getLogger("kettle")
KettleLogger.setLevel(logging.DEBUG)
INFO = KettleLogger.info
WARN = KettleLogger.warn
DEBUG = KettleLogger.debug


class KettleManager:
	pass


class Kettle(socketserver.BaseRequestHandler):
	def handle(self):
		header = self.request.recv(4)
		body_size, = struct.unpack("<i", header)
		data = self.request.recv(body_size)
		data = json.loads(data.decode("utf-8"))
		data = data[0]
		query_type = data["Type"]
		payload = data[query_type]
		DEBUG("Got payload %r", payload)
		if query_type == "Init":
			response = self.init_game(payload)
		else:
			raise NotImplementedError

		serialized = json.dumps(response).encode("utf-8")
		response_payload = struct.pack("<i", len(serialized)) + serialized
		DEBUG("Sending %r" % (response_payload))
		self.request.sendall(response_payload)
		self.manager = KettleManager()

	def _serialize_tags(self, tags):
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

	def init_game(self, payload):
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
		self.game = Game(players=players)
		self.game.start()

		ret = []
		ret.append(self.game_entity(self.game))
		for player in self.game.players:
			ret.append(self.player_entity(player))

		for entity in self.game.all_entities:
			ret.append(self.full_entity(entity))

		return ret

	def game_entity(self, game):
		return {
			"Type": "GameEntity",
			"GameEntity": {
				"EntityID": game.manager.id,
				"Tags": self._serialize_tags(game.tags),
			}
		}

	def player_entity(self, player):
		return {
			"Type": "Player",
			"Player": {
				"EntityID": player.manager.id,
				"PlayerID": player.manager.id + 1,
				"Tags": self._serialize_tags(player.tags),
			}
		}

	def full_entity(self, card):
		return {
			"Type": "FullEntity",
			"FullEntity": {
				"EntityID": card.manager.id,
				"Tags": self._serialize_tags(card.tags),
			}
		}


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
