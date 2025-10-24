from pathlib import Path
from typing import List

MARKER = '<!-- MARKER FOR MAPPER SCRIPT -->'

def search_recipes(parent: Path) -> List[Path]:
    found: List[Path] = []
    for p in parent.rglob('*.md'):
        try:
            text = p.read_text(encoding='utf-8')
        except Exception as e:
            print(f"Could not read {p}: {e}")
            continue
        lines = text.splitlines()
        if lines and lines[-1].strip() == MARKER:
            found.append(p)
    
    return found

def read_lines(path: Path) -> List[str]:
    return path.read_text(encoding='utf-8').splitlines()