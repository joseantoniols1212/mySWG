import os
import shutil
import logging
import re
from pathlib import Path

from block_markdown_funcs import markdown_to_html_node

logger = logging.getLogger(__name__)


def copy_directory(src, dst):
    # Delete content of src directory
    for elem in os.listdir(dst):
        elem_path = os.path.join(dst, elem)
        if os.path.isfile(elem_path):
            os.remove(elem_path)
        else:
            shutil.rmtree(elem_path)
    logger.info("source file %s deleted", dst)

    # Recursively copy src into dst
    for elem in os.listdir(src):
        elem_path = os.path.join(src, elem)
        if os.path.isfile(elem_path):
            logger.info("%s file copied in %s", elem_path, dst)
            shutil.copy(elem_path, dst)
        else:
            new_dir_path = os.path.join(dst, elem)
            logger.info("%s dir created", new_dir_path)
            os.mkdir(new_dir_path)
            logger.info("recursively copying %s in %s", elem_path, new_dir_path)
            copy_directory(elem_path, new_dir_path)


def extract_title(markdown):
    matches = re.match(r"^\# ([\w ]*)", markdown)
    if not matches:
        raise ValueError("markdown input should contain first level header")
    h1 = matches[1].strip()
    return h1


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r", encoding="utf8") as file:
        markdown = file.read()
    with open(template_path, "r", encoding="utf8") as file:
        template = file.read()
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    dest_dir_path = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)
    with open(dest_path, "w", encoding="utf8") as file:
        file.write(template)


def generate_pages_recursively(dir_path_content, template_path, dest_dir_path):
    for elem in os.listdir(dir_path_content):
        if os.path.isfile(dir_path_content + elem):
            elem_html_name = Path(elem).stem + ".html"
            generate_page(
                dir_path_content + elem, template_path, dest_dir_path + elem_html_name
            )
        else:
            generate_pages_recursively(
                dir_path_content + elem + "/", template_path, dest_dir_path + elem + "/"
            )


def main():
    logging.basicConfig(filename="main.log", level=logging.INFO)
    copy_directory("static/", "public/")
    generate_pages_recursively("content/", "template.html", "public/")


if __name__ == "__main__":
    main()
