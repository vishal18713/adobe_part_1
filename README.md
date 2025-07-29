<div align="center">
  <h1>PDF Outline Extractor</h1>
  <p>
    <img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python 3.10+">
    <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT License">
  </p>
  <p>Extract structured outlines and titles from PDF documents with ease using this Python-based tool powered by advanced text processing.</p>
</div>

---

## 🚀 Overview

**PDF Outline Extractor** is a lightweight Python utility that leverages PyMuPDF and LLM-based text normalization to pull document titles and hierarchical headings (H1, H2, H3) from PDF files. Whether you need to index chapters, generate tables of contents, or prepare structured metadata, this tool automates the process and delivers JSON-ready output.

---

## ⚡ Features

* **Title Extraction**: Automatically detects and returns the main title of your PDF.
* **Hierarchical Headings**: Captures up to three levels of headings with page numbers.
* **Text Cleaning**: Normalizes punctuation, trims whitespace, and removes noise.
* **CLI & API**: Use via command-line or import as a library in your Python projects.
* **Batch Mode**: Process all PDFs in a folder in one go.
* **JSON Output**: Structured JSON format for easy integration.

---

## 📦 Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/vishal18713/adobe_part_1
   cd pdf-outline-extractor
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

---

## 🐳 Docker

> **Note:** Docker commands unchanged from original.

Build and run the extractor inside a container:

```bash
# Build the Docker image
docker build -t pdf-outline-extractor .

# Run against a single file
docker run --rm -v "$(pwd)/input":/app/input -v "$(pwd)/output":/app/output pdf-outline-extractor Pdfs/Adobe_60pages.pdf

# Batch process all PDFs
docker run --rm -v "$(pwd)/input":/app/input -v "$(pwd)/output":/app/output pdf-outline-extractor -all
```

---

## ⚙️ Usage

### Command-Line Interface

```bash
# Print outline to stdout
python llm4_to_json.py input/YourDoc.pdf

# Save outline to JSON file
python llm4_to_json.py -o outline.json "My Document With Spaces.pdf"

# Batch process all PDFs in 'input/'
python llm4_to_json.py -all
```

### Programmatic API

```python
from llm4_to_json import extract_outline_from_pdf

result = extract_outline_from_pdf("path/to/document.pdf")
print(f"Title: {result['title']}")
for item in result['outline']:
    print(f"{item['level']} (Page {item['page']}): {item['text']}")
```

---

## 📝 Output Format

The extractor produces a JSON object:

```json
{
  "title": "Document Title",
  "outline": [
    {"level": "H1", "text": "Chapter 1: Intro", "page": 1},
    {"level": "H2", "text": "Background",     "page": 2}
  ]
}
```

---

## 🤝 Contributing

Contributions are welcome! Please submit issues or pull requests for bug fixes, enhancements, or new features.

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE.md) for details.
