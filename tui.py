#!/usr/bin/env python3
"""
TUI Tree Viewer for parse_hir.py parse tree visualization.
Navigate with arrow keys, expand/collapse with Enter.
"""

import curses
from dataclasses import dataclass, field
from typing import List, Optional, Union
from parse_hir import parse_hir, BraceBlock, BracketBlock, ParenBlock


@dataclass
class TreeNode:
    """Represents a node in the visual tree."""
    label: str
    children: List['TreeNode'] = field(default_factory=list)
    expanded: bool = False
    depth: int = 0
    parent: Optional['TreeNode'] = None
    
    @property
    def is_leaf(self) -> bool:
        return len(self.children) == 0


def build_tree(node: Union[BraceBlock, BracketBlock, ParenBlock, str, list], 
               depth: int = 0, 
               parent: Optional[TreeNode] = None) -> TreeNode:
    """Convert parsed HIR structure to TreeNode structure."""
    if isinstance(node, list):
        root = TreeNode(label="root", depth=depth, parent=parent)
        for item in node:
            child = build_tree(item, depth + 1, root)
            root.children.append(child)
        return root
    elif isinstance(node, BraceBlock):
        tree_node = TreeNode(label="{...}", depth=depth, parent=parent)
        for item in node.content:
            child = build_tree(item, depth + 1, tree_node)
            tree_node.children.append(child)
        return tree_node
    elif isinstance(node, BracketBlock):
        tree_node = TreeNode(label="[...]", depth=depth, parent=parent)
        for item in node.content:
            child = build_tree(item, depth + 1, tree_node)
            tree_node.children.append(child)
        return tree_node
    elif isinstance(node, ParenBlock):
        tree_node = TreeNode(label="(...)", depth=depth, parent=parent)
        for item in node.content:
            child = build_tree(item, depth + 1, tree_node)
            tree_node.children.append(child)
        return tree_node
    else:
        # Text node
        text = str(node)
        if len(text) > 60:
            text = text[:57] + "..."
        return TreeNode(label=text, depth=depth, parent=parent)


def flatten_tree(node: TreeNode, visible_nodes: List[TreeNode]):
    """Flatten tree to list of visible nodes for rendering."""
    visible_nodes.append(node)
    if node.expanded:
        for child in node.children:
            flatten_tree(child, visible_nodes)


class TreeViewer:
    """TUI Tree Viewer with keyboard navigation."""
    
    def __init__(self, root: TreeNode):
        self.root = root
        self.cursor_index = 0
        self.scroll_offset = 0
        self.visible_nodes: List[TreeNode] = []
        self._refresh_visible()
    
    def _refresh_visible(self):
        """Rebuild the list of visible nodes."""
        self.visible_nodes = []
        flatten_tree(self.root, self.visible_nodes)
        # Clamp cursor
        if self.cursor_index >= len(self.visible_nodes):
            self.cursor_index = max(0, len(self.visible_nodes) - 1)
    
    def move_up(self):
        """Move cursor up."""
        if self.cursor_index > 0:
            self.cursor_index -= 1
    
    def move_down(self):
        """Move cursor down."""
        if self.cursor_index < len(self.visible_nodes) - 1:
            self.cursor_index += 1
    
    def move_left(self):
        """Collapse current node or move to parent."""
        if self.cursor_index < len(self.visible_nodes):
            node = self.visible_nodes[self.cursor_index]
            if node.expanded and not node.is_leaf:
                node.expanded = False
                self._refresh_visible()
            elif node.parent:
                # Move to parent
                try:
                    parent_idx = self.visible_nodes.index(node.parent)
                    self.cursor_index = parent_idx
                except ValueError:
                    pass
    
    def move_right(self):
        """Expand current node or move to first child."""
        if self.cursor_index < len(self.visible_nodes):
            node = self.visible_nodes[self.cursor_index]
            if not node.expanded and not node.is_leaf:
                node.expanded = True
                self._refresh_visible()
            elif node.expanded and node.children:
                # Move to first child
                self.cursor_index += 1
    
    def toggle_expand(self):
        """Toggle expand/collapse of current node."""
        if self.cursor_index < len(self.visible_nodes):
            node = self.visible_nodes[self.cursor_index]
            if not node.is_leaf:
                node.expanded = not node.expanded
                self._refresh_visible()
    
    def run(self, stdscr):
        """Main TUI loop."""
        curses.curs_set(0)  # Hide cursor
        curses.use_default_colors()
        
        # Initialize color pairs
        curses.init_pair(1, curses.COLOR_CYAN, -1)    # Brace blocks
        curses.init_pair(2, curses.COLOR_GREEN, -1)   # Bracket blocks
        curses.init_pair(3, curses.COLOR_YELLOW, -1)  # Paren blocks
        curses.init_pair(4, curses.COLOR_WHITE, -1)   # Text
        curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Selected
        
        while True:
            stdscr.clear()
            height, width = stdscr.getmaxyx()
            
            # Adjust scroll to keep cursor visible
            view_height = height - 2  # Leave room for header and footer
            if self.cursor_index < self.scroll_offset:
                self.scroll_offset = self.cursor_index
            elif self.cursor_index >= self.scroll_offset + view_height:
                self.scroll_offset = self.cursor_index - view_height + 1
            
            # Header
            header = " HIR Tree Viewer | ↑↓←→: Navigate | Enter: Expand/Collapse | q: Quit "
            stdscr.attron(curses.A_REVERSE)
            stdscr.addstr(0, 0, header.center(width)[:width-1])
            stdscr.attroff(curses.A_REVERSE)
            
            # Draw visible nodes
            for i, node in enumerate(self.visible_nodes[self.scroll_offset:self.scroll_offset + view_height]):
                actual_idx = i + self.scroll_offset
                y = i + 1
                
                if y >= height - 1:
                    break
                
                # Build line
                indent = "  " * node.depth
                
                # Expand/collapse indicator
                if node.is_leaf:
                    indicator = "  "
                elif node.expanded:
                    indicator = "▼ "
                else:
                    indicator = "▶ "
                
                line = f"{indent}{indicator}{node.label}"
                
                # Truncate if too long
                if len(line) > width - 1:
                    line = line[:width - 4] + "..."
                
                # Determine color
                if "{" in node.label:
                    color = curses.color_pair(1)
                elif "[" in node.label:
                    color = curses.color_pair(2)
                elif "(" in node.label:
                    color = curses.color_pair(3)
                else:
                    color = curses.color_pair(4)
                
                # Highlight selected
                if actual_idx == self.cursor_index:
                    stdscr.attron(curses.A_REVERSE)
                    stdscr.addstr(y, 0, line.ljust(width - 1)[:width-1])
                    stdscr.attroff(curses.A_REVERSE)
                else:
                    stdscr.addstr(y, 0, line[:width-1], color)
            
            # Footer with position info
            footer = f" Node {self.cursor_index + 1}/{len(self.visible_nodes)} "
            stdscr.attron(curses.A_REVERSE)
            stdscr.addstr(height - 1, 0, footer.ljust(width)[:width-1])
            stdscr.attroff(curses.A_REVERSE)
            
            stdscr.refresh()
            
            # Handle input
            key = stdscr.getch()
            
            if key == ord('q') or key == ord('Q'):
                break
            elif key == curses.KEY_UP or key == ord('k'):
                self.move_up()
            elif key == curses.KEY_DOWN or key == ord('j'):
                self.move_down()
            elif key == curses.KEY_LEFT or key == ord('h'):
                self.move_left()
            elif key == curses.KEY_RIGHT or key == ord('l'):
                self.move_right()
            elif key == ord('\n') or key == ord(' '):
                self.toggle_expand()


def show(parsed):    
    # Build tree structure
    tree = build_tree(parsed)
    
    # Run TUI
    viewer = TreeViewer(tree)
    curses.wrapper(viewer.run)
