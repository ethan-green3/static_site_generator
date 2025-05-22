import os
from pathlib import Path
from htmlnode import *
from textnode import *
from directory import *
from blocks import *

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Step 1: Read Markdown
    try:
        with open(from_path, "r") as f:
            md_content = f.read()
        print("✔️ Markdown loaded.")
    except Exception as e:
        print(f"❌ Failed to read markdown: {e}")
        return

    # Step 2: Read Template
    try:
        with open(template_path, "r") as f:
            template = f.read()
        print("✔️ Template loaded.")
    except Exception as e:
        print(f"❌ Failed to read template: {e}")
        return

    # Step 3: Convert Markdown
    try:
        title = extract_title(md_content)
        print(f"✔️ Title extracted: {title}")
        html_content = markdown_to_html_node(md_content).to_html()
        print(html_content)
        print("✔️ HTML generated.")
    except Exception as e:
        print(f"❌ Error processing markdown: {e}")
        return

    # Step 4: Fill Template
    try:
        full_page = template.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
        print("✔️ Full HTML page constructed.")
    except Exception as e:
        print(f"❌ Error formatting HTML page: {e}")
        return

    # Step 5: Write Output
    try:
        dest_dir = os.path.dirname(dest_path)
        if not os.path.exists(dest_dir):
            print(f"Creating destination directory: {dest_dir}")
            os.makedirs(dest_dir)

        with open(dest_path, "w") as f:
            f.write(full_page)
        print(f"✅ Successfully wrote: {dest_path}")
    except Exception as e:
        print(f"❌ Failed to write HTML file: {e}")



def main():
    copy_static()
    generate_page("content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
    main()
