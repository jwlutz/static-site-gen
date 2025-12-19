from htmlnode import ParentNode, LeafNode, text_node_to_html_node
from split_delim import markdown_to_blocks, block_to_block_type, BlockType, text_to_textnodes

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def paragraph_to_html_node(block):
    lines = block.split("\n")
    text = " ".join(lines)
    children = text_to_children(text)
    return ParentNode("p", children)

def heading_to_html_node(block):
    count = 0
    for char in block:
        if char == "#":
            count += 1
        else:
            break
    text = block[count + 1:]
    tag = f"h{count}"
    children = text_to_children(text)
    return ParentNode(tag, children)

def code_to_html_node(block):
    # Remove ``` from start and end, strip leading newline only
    text = block[3:-3].lstrip("\n")
    code_node = LeafNode("code", text)
    return ParentNode("pre", [code_node])

def quote_to_html_node(block):
    lines = block.split("\n")
    stripped_lines = []
    for line in lines:
        if line.startswith("> "):
            stripped_lines.append(line[2:])
        elif line.startswith(">"):
            stripped_lines.append(line[1:])
    text = "\n".join(stripped_lines)
    children = text_to_children(text)
    return ParentNode("blockquote", children)

def unordered_list_to_html_node(block):
    lines = block.split("\n")
    li_nodes = []
    for line in lines:
        text = line[2:]
        children = text_to_children(text)
        li_node = ParentNode("li", children)
        li_nodes.append(li_node)
    return ParentNode("ul", li_nodes)

def ordered_list_to_html_node(block):
    lines = block.split("\n")
    li_nodes = []
    for i, line in enumerate(lines):
        space_index = line.index(". ") + 2
        text = line[space_index:]
        children = text_to_children(text)
        li_node = ParentNode("li", children)
        li_nodes.append(li_node)
    return ParentNode("ol", li_nodes)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            children.append(paragraph_to_html_node(block))
        elif block_type == BlockType.HEADING:
            children.append(heading_to_html_node(block))
        elif block_type == BlockType.CODE:
            children.append(code_to_html_node(block))
        elif block_type == BlockType.QUOTE:
            children.append(quote_to_html_node(block))
        elif block_type == BlockType.UNORDERED_LIST:
            children.append(unordered_list_to_html_node(block))
        elif block_type == BlockType.ORDERED_LIST:
            children.append(ordered_list_to_html_node(block))
    return ParentNode("div", children)