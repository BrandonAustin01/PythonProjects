import re
from utils import logger

def convert_markdown_to_html(md: str) -> str:
    html_lines = []
    lines = md.splitlines()
    in_code_block = False
    code_language = ""
    in_list_block = False
    in_table_block = False
    table_header_parsed = False
    footnotes = {}

    for idx, line in enumerate(lines):
        stripped = line.strip()

        # Footnote definition
        if re.match(r"^\[\^(.+?)\]:", stripped):
            footnote_id = re.findall(r"\[\^(.+?)\]:", stripped)[0]
            footnote_text = stripped.split("]:", 1)[1].strip()
            footnotes[footnote_id] = footnote_text
            continue

        # Code block start/end
        if stripped.startswith("```"):
            if in_code_block:
                html_lines.append(f"</code></pre>")
                in_code_block = False
                code_language = ""
            else:
                lang_match = re.match(r"```(\w+)?", stripped)
                code_language = lang_match.group(1) if lang_match else ""
                class_attr = f' class="language-{code_language}"' if code_language else ""
                html_lines.append(f"<pre><code{class_attr}>")
                in_code_block = True
            continue

        if in_code_block:
            html_lines.append(line)
            continue

        # Horizontal rule
        if stripped in ("---", "***"):
            if in_list_block:
                html_lines.append("</ul>")
                in_list_block = False
            html_lines.append("<hr>")
            continue

        # Blockquote
        if stripped.startswith(">"):
            if in_list_block:
                html_lines.append("</ul>")
                in_list_block = False
            html_lines.append(f"<blockquote>{stripped[1:].strip()}</blockquote>")
            continue

        # Headings
        if stripped.startswith("#"):
            if in_list_block:
                html_lines.append("</ul>")
                in_list_block = False
            level = len(stripped) - len(stripped.lstrip("#"))
            html_lines.append(f"<h{level}>{stripped.lstrip('#').strip()}</h{level}>")
            continue

        # List item
        if stripped.startswith(("-", "*")):
            if not in_list_block:
                html_lines.append("<ul>")
                in_list_block = True
            html_lines.append(f"<li>{stripped[1:].strip()}</li>")
            continue
        elif in_list_block:
            html_lines.append("</ul>")
            in_list_block = False

        # Table row
        if "|" in stripped:
            cells = [cell.strip() for cell in stripped.strip("|").split("|")]
            next_line = lines[idx + 1].strip() if idx + 1 < len(lines) else ""
            if not in_table_block:
                html_lines.append("<table>")
                in_table_block = True

            if not table_header_parsed and re.match(r"^\|?[\s-]+\|[\s|\-]*$", next_line):
                html_lines.append("<tr>" + "".join(f"<th>{cell}</th>" for cell in cells) + "</tr>")
                table_header_parsed = True
                continue
            elif table_header_parsed and re.match(r"^\|?[\s-]+\|[\s|\-]*$", stripped):
                continue
            else:
                html_lines.append("<tr>" + "".join(f"<td>{cell}</td>" for cell in cells) + "</tr>")
            continue
        elif in_table_block:
            html_lines.append("</table>")
            in_table_block = False
            table_header_parsed = False

        # Footnote reference in text
        line = re.sub(r"\[\^(.+?)\]", r'<sup id="ref-\1"><a href="#note-\1">\1</a></sup>', line)

        # Blank line
        if not stripped:
            html_lines.append("<br>")
            continue

        # Inline formatting
        line = re.sub(r"`(.*?)`", r"<code>\1</code>", line)
        line = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", line)
        line = re.sub(r"_(.*?)_", r"<em>\1</em>", line)
        line = re.sub(r"!\[(.*?)\]\((.*?)\)", r'<img alt="\1" src="\2">', line)
        line = re.sub(r"\[(.*?)\]\((.*?)\)", r'<a href="\2">\1</a>', line)

        html_lines.append(f"<p>{line}</p>")

    # Close any open tags
    if in_list_block:
        html_lines.append("</ul>")
    if in_table_block:
        html_lines.append("</table>")

    # Append footnotes
    if footnotes:
        html_lines.append("<hr>")
        html_lines.append("<ol>")
        for fid, content in footnotes.items():
            html_lines.append(f'<li id="note-{fid}">{content} <a href="#ref-{fid}">↩</a></li>')
        html_lines.append("</ol>")

    logger.info("Converted Markdown to HTML successfully.")

    return "\n".join(html_lines)

def sanitize_html(html: str) -> str:
    # Remove script/style/object/embed/iframe tags completely
    tags_to_strip = ["script", "style", "iframe", "object", "embed"]
    for tag in tags_to_strip:
        html = re.sub(fr"<{tag}.*?>.*?</{tag}>", "", html, flags=re.DOTALL | re.IGNORECASE)
    return html
