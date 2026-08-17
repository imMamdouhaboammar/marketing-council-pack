#!/usr/bin/env python3
"""Validate Marketing Council neural graph integrity without third-party dependencies."""
from __future__ import annotations
import argparse, json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {"belongs_to","informs","operationalizes","activates","routes_to","challenges","counterbalances","requires","measured_by","hands_off_to"}


def validate(root: Path) -> dict:
    errors=[]; warnings=[]
    path=root/'neural'/'graph.json'
    if not path.is_file():
        return {'valid':False,'errors':['missing neural/graph.json'],'warnings':[]}
    graph=json.loads(path.read_text(encoding='utf-8'))
    registry_path=root/'references'/'sources.yml'
    registry_text=registry_path.read_text(encoding='utf-8') if registry_path.is_file() else ''
    import re
    registered_sources=set(re.findall(r'^  ([a-z0-9-]+):$', registry_text, flags=re.M))
    nodes=graph.get('nodes',[]); edges=graph.get('edges',[])
    ids=[n.get('id') for n in nodes]
    if len(ids)!=len(set(ids)): errors.append('duplicate node ids')
    known=set(ids)
    for n in nodes:
        if not n.get('id') or not n.get('type') or not n.get('label'): errors.append(f'invalid node: {n}')
        if n.get('path') and not (root/n['path']).is_file(): errors.append(f"missing node path: {n['id']} -> {n['path']}")
    outgoing=defaultdict(list)
    for e in edges:
        if e.get('from') not in known or e.get('to') not in known: errors.append(f'dangling edge: {e}')
        if e.get('relation') not in ALLOWED: errors.append(f'unknown relation: {e}')
        outgoing[e.get('from')].append(e)
    for n in nodes:
        if n.get('type') in {'figure','theory'} and not outgoing[n['id']]: errors.append(f"unconnected {n['type']}: {n['id']}")
        if n.get('type') == 'evidence':
            if not str(n.get('as_of','')).startswith('2026-'): errors.append(f"evidence node missing 2026 as_of: {n['id']}")
            if not n.get('source_ids'): errors.append(f"evidence node missing source_ids: {n['id']}")
            unknown=set(n.get('source_ids',[]))-registered_sources
            if unknown: errors.append(f"evidence node has unknown source_ids: {n['id']} -> {sorted(unknown)}")
    counts=Counter(n.get('type') for n in nodes)
    for t,min_count in {'figure':24,'school':19,'principle':44,'theory':46,'signal':44,'agent':24,'skill':29,'hook':24,'evidence':6}.items():
        if counts[t] < min_count: errors.append(f'{t} count {counts[t]} < {min_count}')
    return {'valid':not errors,'counts':dict(counts),'edge_count':len(edges),'errors':errors,'warnings':warnings}


def main():
    p=argparse.ArgumentParser(); p.add_argument('root',nargs='?',type=Path,default=ROOT); p.add_argument('--json',action='store_true'); a=p.parse_args()
    r=validate(a.root.resolve())
    print(json.dumps(r,indent=2,sort_keys=True) if a.json else f"valid={r['valid']} nodes={sum(r.get('counts',{}).values())} edges={r.get('edge_count',0)}")
    raise SystemExit(0 if r['valid'] else 1)
if __name__=='__main__': main()
