<div align="center">
  <h1>PDF Outline Extractor</h1>
  <p>
    <img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python 3.10+">
    <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT License">
  </p>
  <p>A Python tool to extract structured outlines and titles from PDF documents using LLM-based text processing.</p>
</div>

---

## 🚀 Features

- Extracts document titles and hierarchical outlines from PDFs
- Supports multiple heading levels (H1, H2, H3)
- Cleans and normalizes text and punctuation
- Programmatic API and command-line interface
- Outputs in JSON format
- Batch processing: process all PDFs in a directory at once
- Automatically creates output directory for batch jobs

---

## 📦 Installation

1. **Clone this repository:**
   ```bash
   git clone https://github.com/yourusername/pdf-outline-extractor.git
   cd pdf-outline-extractor
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🛠 Requirements

- Python 3.10 or higher
- [PyMuPDF](https://pymupdf.readthedocs.io/)
- [adobe_part_1](https://github.com/vishal18713/adobe_part_1)

---

## ⚡ Usage

### Command Line Interface

#### Process all PDFs in batch:
```bash
python llm4_to_json.py -all
```
This will process all PDF files from the `input/` directory and save individual JSON files to the `output/` folder.

#### Save outline to JSON file:
```bash
python llm4_to_json.py -o adobe_outline.json input/Adobe_60pages.pdf
```

#### Print outline to stdout:
```bash
python llm4_to_json.py input/Adobe_60pages.pdf
```

#### Handle paths with spaces:
```bash
python llm4_to_json.py -o output.json "My Document With Spaces.pdf"
```

### Programmatic API

```python
from llm4_to_json import extract_outline_from_pdf

# Extract outline from PDF
result = extract_outline_from_pdf("path/to/your/document.pdf")

# The result contains:
# - title: Document title
# - outline: List of headings with level, text, and page number
print(result['title'])
for item in result['outline']:
    print(f"Page {item['page']}: {item['level']} - {item['text']}")
```

---

## 📝 Output Format

The tool generates JSON output with the following structure:

```json
{
  "title": "Document Title",
  "outline": [
    {
      "level": "H1",
      "text": "Chapter 1: Introduction",
      "page": 1
    },
    {
      "level": "H2", 
      "text": "Overview",
      "page": 2
    }
  ]
}
```

---

## 🏷 Command Line Options

- `-all, --all-pdfs`: Process all PDFs from `input/` directory and save to `output/` folder
- `-o, --output`: Specify output JSON file (default: stdout)
- `pdf_path`: Path to the PDF file (supports spaces without quotes)

---

## 📚 Examples

### Single File Processing
```bash
# Process a single PDF and print to stdout
python llm4_to_json.py input/1.pdf

# Process a single PDF and save to file
python llm4_to_json.py -o my_output.json input/1.pdf
```

### Batch Processing
```bash
# Process all PDFs in input/ directory
python llm4_to_json.py -all

# This will create:
# output/1.json
# output/2.json
# output/3.json
# output/4.json
# output/5.json
```

The `input/` directory contains sample PDF files for testing:
- Various numbered PDFs (1.pdf, 2.pdf, 3.pdf, 4.pdf, 5.pdf)

---

## 🤝 Contributing

Pull requests, issues, and suggestions are welcome! Please open an issue or PR to discuss changes or improvements.

---

## 📄 License

This project is licensed under the MIT License.

## Usage

### Command Line Interface

#### Process all PDFs in batch:
```bash
python3 llm4_to_json.py -all
```
This will process all PDF files from the `input/` directory and save individual JSON files to the `output/` folder.

#### Save outline to JSON file:
```bash
python llm4_to_json.py -o adobe_outline.json Pdfs/Adobe_60pages.pdf
```

#### Print outline to stdout:
```bash
python llm4_to_json.py Pdfs/Adobe_60pages.pdf
```

#### Handle paths with spaces:
```bash
python llm4_to_json.py -o output.json My Document With Spaces.pdf
```

### Programmatic API

```python
from llm4_to_json import extract_outline_from_pdf

# Extract outline from PDF
result = extract_outline_from_pdf("path/to/your/document.pdf")

# The result contains:
# - title: Document title
# - outline: List of headings with level, text, and page number
print(result['title'])
for item in result['outline']:
    print(f"Page {item['page']}: {item['level']} - {item['text']}")
```

## Output Format

The tool generates JSON output with the following structure:

```json
{
  "title": "Document Title",
  "outline": [
    {
      "level": "H1",
      "text": "Chapter 1: Introduction",
      "page": 1
    },
    {
      "level": "H2", 
      "text": "Overview",
      "page": 2
    }
  ]
}
```

## Command Line Options

- `-all, --all-pdfs`: Process all PDFs from `input/` directory and save to `output_json/` folder
- `-o, --output`: Specify output JSON file (default: stdout)
- `pdf_path`: Path to the PDF file (supports spaces without quotes)

## Examples

### Single File Processing
```bash
# Process a single PDF and print to stdout
python llm4_to_json.py input/1.pdf

# Process a single PDF and save to file
python llm4_to_json.py -o my_output.json input/1.pdf
```

### Batch Processing
```bash
# Process all PDFs in input/ directory
python llm4_to_json.py -all

# This will create:
# output_json/1.json
# output_json/2.json
# output_json/3.json
# output_json/4.json
# output_json/5.json
```

The `input/` directory contains sample PDF files for testing:
- Various numbered PDFs (1.pdf, 2.pdf, 3.pdf, 4.pdf, 5.pdf)
