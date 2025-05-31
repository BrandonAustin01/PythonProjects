# 📝 Markdown to HTML Converter

A powerful and extendable CLI tool that converts Markdown (`.md`) files into styled HTML documents, with support for:

- Headings, lists, bold/italic, links, images
- Code blocks with syntax highlighting
- Blockquotes and horizontal rules
- Tables, footnotes
- CSS themes and custom styles
- Watch mode (auto-rebuild on change)
- HTML sanitization to prevent unsafe output

---

## 🚀 Getting Started

### 📦 Installation

Clone this repo and install dependencies:

```bash
git clone https://github.com/your-username/md-to-html-converter.git
cd md-to-html-converter
pip install -r requirements.txt
```

You’ll need:

- Python 3.7+
- `watchdog` for watch mode
- `chronilog` for logging

  ```bash
  pip install watchdog
  pip install chronilog
  ```

---

## 🧰 Usage

Basic conversion:

```bash
python main.py --input example.md --output output.html
```

With theme and browser preview:

```bash
python main.py -i example.md -o output.html --theme dark --open
```

Watch mode (auto-regenerates on changes):

```bash
python main.py -i example.md -o output.html --watch
```

Custom CSS override:

```bash
python main.py -i input.md -o output.html --css themes/custom.css
```

---

## 🎨 Themes

Available built-in themes:
- `light`
- `dark`
- `minimal`
- `modern`

Or provide your own CSS file via `--css path/to/style.css`.

---

## 🔍 Supported Markdown Features

| Feature        | Supported |
|----------------|-----------|
| Headings (`#`) | ✅         |
| Bold/Italic    | ✅         |
| Inline Code    | ✅         |
| Code Blocks    | ✅         |
| Blockquotes    | ✅         |
| Horizontal Rule (`---`) | ✅ |
| Lists          | ✅         |
| Tables         | ✅         |
| Links / Images | ✅         |
| Footnotes      | ✅         |
| Watch Mode     | ✅         |
| HTML Sanitization | ✅     |

---

## 🔐 HTML Sanitization

To prevent XSS or malicious scripts, the converter strips:
- `<script>`, `<style>`, `<iframe>`, `<embed>`, and `<object>` tags

This keeps your output safe when rendering Markdown from unknown sources.

---

## 🌈 Syntax Highlighting

Code blocks use language detection:

```markdown
```python
print("Hello World")
```

Results in:

```html
<pre><code class="language-python">...</code></pre>
```

Use with a CDN like [Prism.js](https://prismjs.com/) or [Highlight.js](https://highlightjs.org/):

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/prismjs/themes/prism.css">
<script src="https://cdn.jsdelivr.net/npm/prismjs/prism.js"></script>
```

---

## 📁 Example

Example Markdown:

```markdown
# Hello

Here is a list:

- One
- Two
```

Here is some code:

```python
print("hello")
```

Here’s a footnote. [^1]

```markdown
[^1]: A simple note.
```

---

## 🙌 Credits

Created by [Brandon McKinney](https://github.com/BrandonAustin01). Inspired by static site tools and Markdown parsers.

