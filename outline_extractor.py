import re
from markdown_utils import normalize_punctuation, strip_inline_bold

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
    import pymupdf4llm
    md = pymupdf4llm.to_markdown(pdf_path, page_chunks=True)
    return extract_outline_and_title(md)
