#!/usr/bin/env python3
import os
import sys
import json
import argparse
import glob
from outline_extractor import extract_outline_from_pdf

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
        os.makedirs(output_dir, exist_ok=True)
        pdf_files = glob.glob(os.path.join(pdfs_dir, '*.pdf'))
        if not pdf_files:
            print(f"Error: No PDF files found in '{pdfs_dir}'", file=sys.stderr)
            sys.exit(1)
        print(f"Processing {len(pdf_files)} PDF files...")
        for pdf_file in pdf_files:
            try:
                result = extract_outline_from_pdf(pdf_file)
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
