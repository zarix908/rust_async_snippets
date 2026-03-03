#!/usr/bin/env python3
"""
HIR Parser - Parses HIR content into a tree of {}, [], () objects
"""

import parse_hir
import tui

def main():
    # Read HIR file
    with open('HIR', 'r') as f:
        hir_content = f.read()
    
    # Parse the content
    tree = parse_hir.parse_hir(hir_content)
    tui.show(tree)


if __name__ == "__main__":
    main()
