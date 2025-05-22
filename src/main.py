import os
import sys
from htmlnode import *
from textnode import *
from directory import *
from blocks import *

def generate_page(from_path, template_path, dest_path, base_path="/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Step 1: Read Markdown
    try:
        with open(from_path, "r") as f:
            md_content = f.read()
        print("Markdown loaded.")
    except Exception as e:
        print(f"Failed to read markdown: {e}")
        return

    # Step 2: Read Template
    try:
        with open(template_path, "r") as f:
            template = f.read()
        print("Template loaded.")
    except Exception as e:
        print(f"Failed to read template: {e}")
        return

    # Step 3: Convert Markdown
    try:
        title = extract_title(md_content)
        print(f"Title extracted: {title}")
        html_content = markdown_to_html_node(md_content).to_html()
        print("HTML generated.")
    except Exception as e:
        print(f"Error processing markdown: {e}")
        return

    # Step 4: Fill Template
    try:
        full_page = template.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
        full_page = full_page.replace('href="/', f'href="{base_path}')
        full_page = full_page.replace('src="/', f'src="{base_path}')
        print("Full HTML page constructed.")
    except Exception as e:
        print(f"Error formatting HTML page: {e}")
        return

    # Step 5: Write Output
    try:
        dest_dir = os.path.dirname(dest_path)
        if not os.path.exists(dest_dir):
            print(f"Creating destination directory: {dest_dir}")
            os.makedirs(dest_dir)

        with open(dest_path, "w") as f:
            f.write(full_page)
        print(f"Successfully wrote: {dest_path}")
    except Exception as e:
        print(f"Failed to write HTML file: {e}")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path="/"):
    for entry in os.listdir(dir_path_content):
        entry_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)

        if os.path.isfile(entry_path) and entry.endswith(".md"):
            dest_file_path = os.path.splitext(dest_path)[0] + ".html"
            print(f"Generating page: {entry_path} -> {dest_file_path}")
            generate_page(entry_path, template_path, dest_file_path, base_path)

        elif os.path.isdir(entry_path):
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)
            generate_pages_recursive(entry_path, template_path, dest_path, base_path)

def main():
    base_path = sys.argv[1] if len(sys.argv) > 1 else "/"
    print(f"Using base path: {base_path}")
    copy_static("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", base_path)

if __name__ == "__main__":
    main()
