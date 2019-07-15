#!/usr/bin/env python3

import argparse
import graphviz
import json
import sys


def get_args():
	ap = argparse.ArgumentParser()
	ap.add_argument("input", type = str, metavar = "json",
		help = "input dependency tree to visualize in json format")
	ap.add_argument("-P", "--prefix", type = str,
		metavar = "prefix",
		help = "output prefix (default: <input>, relace 'json' with 'gv')")
	args = ap.parse_args()
	return args


class DependencyTree(list):
	class Node(object):
		def __init__(self, uid, disp = None, source = False, dep = None):
			self.uid = uid
			self.disp = self.uid if disp is None else disp
			self.source = source
			self.dep = dep
			return

	def __init__(self, nodes_cfg, *ka, **kw):
		super(DependencyTree, self).__init__(*ka, **kw)
		for cfg in nodes_cfg:
			self.add_node(**cfg)
		return

	def add_node(self, *ka, **kw):
		self.append(self.Node(*ka, **kw))
		return

	def save_graph(self, prefix = None, title = None):
		dot = graphviz.Digraph(title)
		for node in self:
			dot.node(node.uid, node.disp.replace(" ", "\n"),
				shape = "circle", fontsize = "20", style = "filled",
				color = ("#c2b7ff" if node.source else "#d0d0d0"))
		for node in self:
			if node.dep:
				for dep_node in node.dep:
					dot.edge(node.uid, dep_node, penwidth = "4.0",
						dir = "forward", arrowhead = "normal")
		dot.render(prefix, format = "png")
		return

	@classmethod
	def from_json(cls, file):
		with open(file, "r") as fp:
			new = cls(json.load(fp))
		return new


def main():
	args = get_args()
	graph = DependencyTree.from_json(args.input)
	prefix = args.input.replace(".json", ".gv") if args.prefix is None\
		else args.prefix
	graph.save_graph(prefix)
	return


if __name__ == "__main__":
	main()
