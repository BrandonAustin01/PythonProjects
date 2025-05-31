import argparse
import webbrowser
import time
from converter.parser import convert_markdown_to_html, sanitize_html
from converter.themes import load_theme_css
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from utils import logger

class MarkdownChangeHandler(FileSystemEventHandler):
    def __init__(self, args):
        self.args = args

    def on_modified(self, event):
        if event.src_path.endswith(self.args.input):
            print("🔁 Detected change — Rebuilding...")
            run_conversion(self.args)
            logger.info(f"Rebuilt due to change in {event.src_path}")

def run_conversion(args):
    # Read Markdown input
    with open(args.input, "r", encoding="utf-8") as f:
        md_content = f.read()

    html_body = convert_markdown_to_html(md_content)
    html_body = sanitize_html(html_body)  # 🧼 sanitize dangerous tags

    # Load theme or custom CSS
    theme_css = ""
    if args.css:
        try:
            with open(args.css, "r", encoding="utf-8") as f:
                theme_css = f.read()
        except FileNotFoundError:
            print(f"⚠️ Warning: Custom CSS file '{args.css}' not found. Falling back to theme '{args.theme}'.")
            theme_css = load_theme_css(args.theme)
            logger.warning(f"Custom CSS file '{args.css}' not found. Using theme '{args.theme}' instead.")
    else:
        theme_css = load_theme_css(args.theme)
        logger.info(f"Using theme '{args.theme}' for CSS.")

    # Build HTML
    full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{args.title}</title>
    <style>{theme_css}</style>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/themes/prism.min.css" />
    <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/prism.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/prism-python.min.js"></script>
</head>
<body>
{html_body}
</body>
</html>"""

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(full_html)

    print(f"✅ Rebuilt: {args.input} → {args.output}")

    if args.open:
        webbrowser.open(args.output)

def main():
    parser = argparse.ArgumentParser(description="Markdown to HTML Converter")
    parser.add_argument("--input", "-i", required=True, help="Path to input .md file")
    parser.add_argument("--output", "-o", required=True, help="Path to output .html file")
    parser.add_argument("--title", "-t", default="Document", help="HTML page title")
    parser.add_argument("--theme", choices=["light", "dark", "minimal", "modern"], default="light")
    parser.add_argument("--css", help="Path to custom CSS file (overrides theme)")
    parser.add_argument("--open", action="store_true", help="Open the output HTML in your default browser")
    parser.add_argument("--watch", action="store_true", help="Watch input file and auto-rebuild on change")

    args = parser.parse_args()

    run_conversion(args)

    if args.watch:
        print("👀 Watch mode active. Listening for file changes...")

        logger.info("Starting file watcher for changes...")

        event_handler = MarkdownChangeHandler(args)
        observer = Observer()
        observer.schedule(event_handler, path='.', recursive=False)
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            logger.info("File watcher stopped.")
        observer.join()

if __name__ == "__main__":
    main()