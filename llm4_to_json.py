#!/usr/bin/env python3
import re
import os
import sys
import json
import argparse
import pymupdf4llm
import glob

def normalize_punctuation(text: str) -> str:
    """
    Replace common unicode punctuation with ASCII equivalents.
    """
    punct_map = {
        "‘": "'",
        "’": "'",
        "“": '"',
        "”": '"',
        "–": '-',
        "—": '-',
        "…": '...'
    }
    for k, v in punct_map.items():
        text = text.replace(k, v)
    return text

def strip_inline_bold(text: str) -> str:
    """
    Remove inline formatting, bold markers, trailing numbers, repeated punctuation, and normalize whitespace.
    """
    text = normalize_punctuation(text)
    text = re.sub(r'`([^`]+)`', r"\1", text)  # Remove code backticks
    text = text.replace('`', '')                # Remove stray backticks
    text = re.sub(r'_?\*\*(.*?)\*\*_?', r"\1", text)  # Remove bold
    text = re.sub(r'(?:\b)(\d+)$', '', text)  # Remove trailing numbers
    text = re.sub(r'[\.\-\,\"\=]{2,}', '', text)  # Remove repeated punctuation
    return ' '.join(text.split()).strip()

def parse_markdown_outline(md: str, page_num: int):
    result = []
    for ln in md.splitlines():
        if re.fullmatch(r"^[\.\-\*,=\"']{2,}\s*$", ln.strip()):
            continue
        cleaned = normalize_punctuation(ln.strip())
        lvl = None
        txt = None
        if cleaned.startswith('# '):
            lvl = 'H1'
            txt = strip_inline_bold(cleaned[2:].strip())
        elif cleaned.startswith('## '):
            lvl = 'H1'
            txt = strip_inline_bold(cleaned[3:].strip())
        elif cleaned.startswith('### '):
            lvl = 'H2'
            txt = strip_inline_bold(cleaned[4:].strip())
        elif cleaned.startswith('#### '):
            lvl = 'H3'
            txt = strip_inline_bold(cleaned[5:].strip())
        elif re.fullmatch(r'_?\*\*(.*?)\*\*_?', cleaned):
            lvl = 'H3'
            txt = strip_inline_bold(cleaned)
        if txt and re.match(r'^[a-z]', txt):
            continue
        if lvl and txt:
            result.append({'level': lvl, 'text': txt, 'page': page_num + 1})
    return result

def extract_outline_and_title(md_pages):
    doc_title = 'Untitled'
    # Find first H1 not starting with lowercase as title
    for pg in md_pages:
        for ln in pg.get('text', '').splitlines():
            cleaned = normalize_punctuation(ln.strip())
            if cleaned.startswith('# '):
                possible = strip_inline_bold(cleaned[2:].strip())
                if not re.match(r'^[a-z]', possible):
                    doc_title = possible
                    break
        if doc_title != 'Untitled':
            break
    output = {'title': doc_title, 'outline': []}
    for idx, pg in enumerate(md_pages):
        outline_items = parse_markdown_outline(pg.get('text', ''), idx)
        for toc in pg.get('toc_items', []):
            if isinstance(toc, (list, tuple)) and len(toc) >= 2:
                toc_lvl, toc_txt = toc[0], strip_inline_bold(toc[1])
                if not re.match(r'^[a-z]', toc_txt) and toc_txt not in {e['text'] for e in outline_items}:
                    lvl_str = f'H{toc_lvl if 1 <= toc_lvl <= 3 else 3}'
                    outline_items.append({'level': lvl_str, 'text': toc_txt, 'page': idx + 1})
        output['outline'].extend(outline_items)
    return output

def extract_outline_from_pdf(pdf_path):
    md = pymupdf4llm.to_markdown(pdf_path, page_chunks=True)
    return extract_outline_and_title(md)

def main():
    parser = argparse.ArgumentParser(
        description="Extract title and outline from a single PDF (handles spaces in path)"
    )
    parser.add_argument(
        '-o', '--output',
        help='Output JSON file (default: stdout)',
        default=None
    )
    parser.add_argument(
        '-all', '--all-pdfs',
        action='store_true',
        help='Process all PDFs from Pdfs directory and save to output folder'
    )
    # Capture all remaining args as the PDF path (allows unquoted spaces)
    parser.add_argument(
        'pdf_path',
        nargs='*',  # Changed from REMAINDER to * to make it optional
        help='Path to the PDF file (can include spaces without quoting)'
    )
    args = parser.parse_args()

    if args.all_pdfs:
        # Process all PDFs from Pdfs directory
        pdfs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input')
        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
        
        if not os.path.exists(pdfs_dir):
            print(f"Error: Pdfs directory '{pdfs_dir}' not found", file=sys.stderr)
            sys.exit(1)
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Find all PDF files
        pdf_files = glob.glob(os.path.join(pdfs_dir, '*.pdf'))
        
        if not pdf_files:
            print(f"Error: No PDF files found in '{pdfs_dir}'", file=sys.stderr)
            sys.exit(1)
        
        print(f"Processing {len(pdf_files)} PDF files...")
        
        for pdf_file in pdf_files:
            try:
                result = extract_outline_from_pdf(pdf_file)
                
                # Create output filename based on PDF filename
                pdf_basename = os.path.splitext(os.path.basename(pdf_file))[0]
                output_file = os.path.join(output_dir, f"{pdf_basename}.json")
                
                with open(output_file, 'w') as out_f:
                    json.dump(result, out_f, indent=2)
                
                print(f"Processed: {os.path.basename(pdf_file)} ➔ {output_file}")
                
            except Exception as e:
                print(f"Error processing '{pdf_file}': {e}", file=sys.stderr)
        
        print(f"All JSON files saved to: {output_dir}")
        return

    if not args.pdf_path:
        print("Error: no PDF path provided", file=sys.stderr)
        sys.exit(1)
    pdf_path = ' '.join(args.pdf_path)

    try:
        result = extract_outline_from_pdf(pdf_path)
        # no longer adding result['source']
    except Exception as e:
        print(f"Error processing '{pdf_path}': {e}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        with open(args.output, 'w') as out_f:
            json.dump(result, out_f, indent=2)
        print(f"Saved JSON ➔ {args.output}")
    else:
        json.dump(result, sys.stdout, indent=2)

if __name__ == '__main__':
    main()
