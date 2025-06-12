#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    parts = line.split('\t')
    if len(parts) != 3:
        continue
    node, pr, outlinks = parts
    pr = float(pr)
    links = outlinks.split(',') if outlinks else []

    # Phân phối PR cho các node liên kết
    if links:
        share_pr = pr / len(links)
        for target in links:
            print(f"{target}\t{share_pr}")
    
    # Giữ lại cấu trúc đồ thị
    print(f"{node}\tSTRUCT:{outlinks}")
