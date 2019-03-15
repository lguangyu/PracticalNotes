#!/usr/bin/env python3

import sys
import graphviz


NODES = [
	dict(uid = "libiconv", disp = "libiconv 1.15", source = False, dep = None),
	dict(uid = "readline", disp = "readline 7.0.3_1", source = False, dep = None),
	dict(uid = "libgpg-error", disp = "libgpg-error 1.35", source = True,
		dep = ["libiconv", "readline"]),
	dict(uid = "libassuan", disp = "libassuan 2.5.3", source = True,
		dep = ["libgpg-error"]),
	dict(uid = "libgcrypt", disp = "libgcrypt 1.8.4", source = True,
		dep = ["npth"]),
	dict(uid = "npth", disp = "npth 1.6", source = True, dep = None),
	dict(uid = "ntbtls", disp = "ntbtls 0.1.2", source = True,
		dep = ["libgpg-error", "libgcrypt", "libksba", "zlib"]),
	dict(uid = "libksba", disp = "libksba 1.3.5", source = True,
		dep = ["libgpg-error"]),
	dict(uid = "pinentry", disp = "pinentry 1.1.0", source = True,
		dep = ["libgpg-error", "libassuan", "ncurses", "libiconv", "qt5"]),
	dict(uid = "gnupg", disp = "gnupg 2.2.13", source = True,
		dep = ["pinentry", "libgpg-error", "libgcrypt", "libassuan", "libksba",
			"npth", "ntbtls", "libiconv", "zlib", "bzip2", "readline"]),
	dict(uid = "zlib", disp = "zlib 1.2.11", source = False, dep = None),
	dict(uid = "bzip2", disp = "bzip2 1.0.6_1", source = False, dep = None),
	dict(uid = "qt5", disp = "Qt5 5.12.1", source = False, dep = None),
	dict(uid = "ncurses", disp = "ncurses 6.1", source = False, dep = None),
]


def tree_graphviz(nodes_cfg, title = None, prefix = None):
	dot = graphviz.Digraph(title)
	for node in nodes_cfg:
		dot.node(node["uid"], node["disp"].replace(" ", "\n"),
			shape = "circle", fontsize = "20", style = "filled",
			color = ("#c2b7ff" if node["source"] else "#d0d0d0"))
	for node in nodes_cfg:
		if node["dep"]:
			for dep in node["dep"]:
				dot.edge(node["uid"], dep, penwidth = "4.0",
					dir = "forward", arrowhead = "normal")
	dot.render(prefix, format = "png")


if __name__ == "__main__":
	prefix = sys.argv[0][:-2] + "gv"
	tree_graphviz(NODES, "GPG dependency tree", prefix)
