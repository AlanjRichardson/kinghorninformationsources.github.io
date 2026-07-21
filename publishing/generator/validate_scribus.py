#!/usr/bin/env python3
"""Geometry checks for the Abden Scribus v0.5.2 framework."""
from pathlib import Path
import sys
from lxml import etree

PT_PER_MM=72/25.4
TOL=0.02
INSIDE=25*PT_PER_MM
OUTSIDE=20*PT_PER_MM
EXPECTED_WIDTH=165*PT_PER_MM

def close(a,b): return abs(float(a)-float(b)) <= TOL

def main(path: Path) -> int:
    root=etree.parse(str(path)).getroot(); doc=root.find('DOCUMENT')
    errors=[]; warnings=[]
    pages=doc.findall('PAGE'); masters=doc.findall('MASTERPAGE')
    if len(pages)!=14: warnings.append(f'Expected 14 specimen pages; found {len(pages)}')
    names={m.get('NAM') for m in masters}
    expected={'A-Title','B-Copyright','C-Contents','D-Chapter Opening','E-Left Page','F-Right Page','G-Full Page Figure','H-Blank Page'}
    missing=expected-names
    if missing: errors.append('Missing master pages: '+', '.join(sorted(missing)))
    for kind, items in [('page',pages),('master',masters)]:
        for x in items:
            label=x.get('NAM') or x.get('NUM','?')
            if not close(x.get('BORDERLEFT'),INSIDE): errors.append(f'{kind} {label}: BORDERLEFT is not 25 mm (inside)')
            if not close(x.get('BORDERRIGHT'),OUTSIDE): errors.append(f'{kind} {label}: BORDERRIGHT is not 20 mm (outside)')
    page_xs=[float(p.get('PAGEXPOS')) for p in pages]; mid=(min(page_xs)+max(page_xs))/2
    for p in pages:
        is_left=float(p.get('PAGEXPOS'))<mid
        expected_left='1' if is_left else '0'
        if p.get('LEFT')!=expected_left: errors.append(f"Page {int(p.get('NUM'))+1}: LEFT={p.get('LEFT')} expected {expected_left}")
    # Main 165 mm frames should start 20 mm from a physical left edge and 25 mm from a physical right edge.
    page_by_num={p.get('NUM'):p for p in pages}
    for o in doc.findall('PAGEOBJECT'):
        if not close(o.get('WIDTH','0'),EXPECTED_WIDTH): continue
        p=page_by_num.get(o.get('OwnPage'))
        if p is None: continue
        local_x=float(o.get('XPOS'))-float(p.get('PAGEXPOS'))
        is_left=p.get('LEFT')=='1'; expected=OUTSIDE if is_left else INSIDE
        if not close(local_x,expected):
            warnings.append(f"{o.get('ANNAME','unnamed')} on page {int(p.get('NUM'))+1}: local X={local_x/PT_PER_MM:.2f} mm, expected {expected/PT_PER_MM:.2f} mm")
    print('Abden Scribus QA Report')
    print('========================')
    print(f'File: {path}')
    print(f'Pages: {len(pages)} | Master pages: {len(masters)}')
    if errors:
        print('\nERRORS')
        for e in errors: print('  ✗',e)
    if warnings:
        print('\nWARNINGS')
        for w in warnings: print('  !',w)
    if not errors:
        print('\n✓ Facing-page margin semantics are correct')
        print('✓ Page-side flags are consistent with spread positions')
        print('✓ Required master pages are present')
    print(f'\nResult: {len(errors)} error(s), {len(warnings)} warning(s)')
    return 1 if errors else 0

if __name__=='__main__':
    p=Path(sys.argv[1]) if len(sys.argv)>1 else Path('Abden_Master_Template_v0.5.2.sla')
    raise SystemExit(main(p))
