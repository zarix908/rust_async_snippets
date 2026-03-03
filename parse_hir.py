from dataclasses import dataclass
from typing import Union, List


@dataclass
class BraceBlock:
    """Represents a {} block"""
    content: List[Union['BraceBlock', 'BracketBlock', 'ParenBlock', str]]
    
    def __repr__(self):
        return f"Brace{{{self.content}}}"


@dataclass
class BracketBlock:
    """Represents a [] block"""
    content: List[Union['BraceBlock', 'BracketBlock', 'ParenBlock', str]]
    
    def __repr__(self):
        return f"Bracket[{self.content}]"


@dataclass
class ParenBlock:
    """Represents a () block"""
    content: List[Union['BraceBlock', 'BracketBlock', 'ParenBlock', str]]
    
    def __repr__(self):
        return f"Paren({self.content})"


def parse_hir(text: str) -> List[Union[BraceBlock, BracketBlock, ParenBlock, str]]:
    """
    Parse HIR text into a tree of nested bracket structures.
    Returns a list of top-level elements (blocks and text between them).
    """
    result = []
    pos = 0
    length = len(text)
    
    def parse_block(start_pos: int, end_char: str, block_class):
        """Parse a block starting after the opening bracket."""
        nonlocal pos
        pos = start_pos
        content = []
        text_start = pos
        
        while pos < length:
            char = text[pos]
            
            if char == end_char:
                # End of this block
                if text_start < pos:
                    txt = text[text_start:pos].strip()
                    if txt:
                        content.append(txt)
                pos += 1  # Skip closing bracket
                return block_class(content)
            
            elif char == '{':
                # Save text before this block
                if text_start < pos:
                    txt = text[text_start:pos].strip()
                    if txt:
                        content.append(txt)
                pos += 1  # Skip opening bracket
                block = parse_block(pos, '}', BraceBlock)
                content.append(block)
                text_start = pos
                
            elif char == '[':
                # Save text before this block
                if text_start < pos:
                    txt = text[text_start:pos].strip()
                    if txt:
                        content.append(txt)
                pos += 1  # Skip opening bracket
                block = parse_block(pos, ']', BracketBlock)
                content.append(block)
                text_start = pos
                
            elif char == '(':
                # Save text before this block
                if text_start < pos:
                    txt = text[text_start:pos].strip()
                    if txt:
                        content.append(txt)
                pos += 1  # Skip opening bracket
                block = parse_block(pos, ')', ParenBlock)
                content.append(block)
                text_start = pos
                
            else:
                pos += 1
        
        # Reached end without finding closing bracket
        if text_start < pos:
            txt = text[text_start:pos].strip()
            if txt:
                content.append(txt)
        return block_class(content)
    
    # Parse top level
    text_start = 0
    while pos < length:
        char = text[pos]
        
        if char == '{':
            if text_start < pos:
                txt = text[text_start:pos].strip()
                if txt:
                    result.append(txt)
            pos += 1
            block = parse_block(pos, '}', BraceBlock)
            result.append(block)
            text_start = pos
            
        elif char == '[':
            if text_start < pos:
                txt = text[text_start:pos].strip()
                if txt:
                    result.append(txt)
            pos += 1
            block = parse_block(pos, ']', BracketBlock)
            result.append(block)
            text_start = pos
            
        elif char == '(':
            if text_start < pos:
                txt = text[text_start:pos].strip()
                if txt:
                    result.append(txt)
            pos += 1
            block = parse_block(pos, ')', ParenBlock)
            result.append(block)
            text_start = pos
            
        else:
            pos += 1
    
    # Remaining text
    if text_start < length:
        txt = text[text_start:length].strip()
        if txt:
            result.append(txt)
    
    return result


def print_tree(node: list, indent: int = 0):
    """Pretty print the parsed tree structure."""
    prefix = "  " * indent
    if isinstance(node, list): 
        for item in node:
            print_tree(item)
    elif isinstance(node, BraceBlock):
        print(f"{prefix}{{")
        print_tree(node.content, indent + 1)
        print(f"{prefix}}}")
    elif isinstance(node, BracketBlock):
        print(f"{prefix}[")
        print_tree(node.content, indent + 1)
        print(f"{prefix}]")
    elif isinstance(node, ParenBlock):
        print(f"{prefix}(")
        print_tree(node.content, indent + 1)
        print(f"{prefix})")
    else:
        # Text content - truncate if too long
        text = str(node)
        if len(text) > 80:
            text = text[:77] + "..."
        print(f"{prefix}{text}")
