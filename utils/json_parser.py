import re


def parse_markdown_sections(text):

    sections = {}

    matches = re.findall(
        r"##\s*(.*?)\n(.*?)(?=\n##|\Z)",
        text,
        re.DOTALL
    )

    for title, body in matches:
        sections[title.strip()] = body.strip()

    return sections