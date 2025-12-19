import os
from pathlib import Path
from markdown_to_html import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("no h1 found")

def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(f"Generating page from {from_path} using {template_path}")
    with open(from_path, 'r') as f:
        markdown_content = f.read()
    with open(template_path, 'r') as f:
        template_content = f.read()
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    title = extract_title(markdown_content)

    final_html = template_content.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)

    # Replace root paths with basepath for deployment
    final_html = final_html.replace('href="/', f'href="{basepath}')
    final_html = final_html.replace('src="/', f'src="{basepath}')

    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    with open(dest_path, 'w') as f:
        f.write(final_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    items = os.listdir(dir_path_content)
    for item in items:
        src_path = os.path.join(dir_path_content, item)
        if os.path.isfile(src_path):
            if item.endswith(".md"):
                dest_file = item.replace(".md", ".html")
                dest_path = os.path.join(dest_dir_path, dest_file)
                generate_page(src_path, template_path, dest_path, basepath)
        else:
            new_dest_dir = os.path.join(dest_dir_path, item)
            generate_pages_recursive(src_path, template_path, new_dest_dir, basepath)