#!/usr/bin/env python3
import sys

d = 0.85  # damping factor
source_node = "P1"

current_node = None
total_pr = 0
outlinks = ""

for line in sys.stdin:
    line = line.strip()
    parts = line.split('\t')

    if len(parts) != 2:
        continue

    node, value = parts

    if current_node and node != current_node:
        base = 1.0 if current_node == source_node else 0.0
        new_pr = (1 - d) * base + d * total_pr
        print(f"{current_node}\t{new_pr:.6f}\t{outlinks}")
        total_pr = 0
        outlinks = ""

    current_node = node
    if value.startswith("STRUCT:"):
        outlinks = value[7:]
    else:
        total_pr += float(value)

if current_node:
    base = 1.0 if current_node == source_node else 0.0
    new_pr = (1 - d) * base + d * total_pr
    print(f"{current_node}\t{new_pr:.6f}\t{outlinks}")
