"""
A minimal implementation of Monte Carlo tree search (MCTS) in Python 3
Luke Harold Miles, July 2019, Public Domain Dedication
See also https://en.wikipedia.org/wiki/Monte_Carlo_tree_search
https://gist.github.com/qpwo/c538c6f73727e254fdc7fab81024f6e1
"""
from abc import ABC, abstractmethod
from collections import defaultdict
import math


class MCTS:
	"Monte Carlo tree searcher. First rollout the tree then choose a move."

	def __init__(self, exploration_weight=1):
		self.Q = defaultdict(int)  # total reward of each node
		self.N = defaultdict(int)  # total visit count for each node
		self.children = dict()  # children of each node
		self.exploration_weight = exploration_weight

	def choose(self, node): # works?
		"Choose the best successor of node. (Choose a move in the game)"
		if node.is_terminal():
			raise RuntimeError(f"choose called on terminal node {node}")

		if node not in self.children:
			return node.find_random_child()

		def score(n): # works?
			if self.N[n] == 0:
				return float("-inf")  # avoid unseen moves
			return self.Q[n] / self.N[n]  # average reward

		return max(self.children[node], key=score)

	def do_rollout(self, node): # has func calls that dont work
		"Make the tree one layer better. (Train for one iteration.)"
		path = self._select(node)
		leaf = path[-1]
		self._expand(leaf)
		reward = self._simulate(leaf)
		self._backpropagate(path, reward)

	def _select(self, node):
		"Find an unexplored descendent of `node`"
		path = []
		while True:
			path.append(node)
			if node not in self.children or not self.children[node]:
				# node is either unexplored or terminal
				return path
			unexplored = self.children[node] - self.children.keys()
			if unexplored:
				n = unexplored.pop()
				path.append(n)
				return path
			node = self._uct_select(node)  # descend a layer deeper

	def _expand(self, node):
		"Update the `children` dict with the children of `node`"
		if node in self.children:
			return  # already expanded
		self.children[node] = node.find_children()

	def _simulate(self, node):
		"Returns the reward for a random simulation (to completion) of `node`"
		if node.current_player.name == "Player1":
			invert_reward = False
		else:
			invert_reward = True
		while True:
			if node.is_terminal():
				reward = node.reward()
				return 1 - reward if invert_reward else reward
			node = node.find_random_child()
			invert_reward = not invert_reward

	def _backpropagate(self, path, reward):
		"Send the reward back up to the ancestors of the leaf"
		for node in reversed(path):
			self.N[node] += 1
			self.Q[node] += reward
			reward = 1 - reward  # 1 for me is 0 for my enemy, and vice versa

	def _uct_select(self, node):
		"Select a child of node, balancing exploration & exploitation"

		# All children of node should already be expanded:
		assert all(n in self.children for n in self.children[node])

		log_N_vertex = math.log(self.N[node])

		def uct(n):
			"Upper confidence bound for trees"
			return self.Q[n] / self.N[n] + self.exploration_weight * math.sqrt(
				log_N_vertex / self.N[n]
			)

		return max(self.children[node], key=uct)
