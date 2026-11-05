#!/usr/bin/env python3
"""Reproduce private final Scores for IndexResearch R02; frozen criteria, no hidden bonuses."""
import csv
from decimal import Decimal,ROUND_HALF_UP
from pathlib import Path
P=Path(__file__).resolve().parent

def read(name):
    with (P/name).open(encoding='utf-8-sig',newline='') as f:
        return list(csv.DictReader(f))
model=read('SCORING_MODEL.csv'); rows=read('SCORE_MATRIX.csv')
w={m['criterion_id']:Decimal(m['weight']) for m in model}
assert sum(w.values())==100 and set(w)==set('RSNPL')
assert all(m['model_version']=='v0.1-FROZEN' for m in model)
for r in rows:
    score=sum(w[k]*Decimal(r[k+'_level'])/5 for k in w)
    assert abs(score-Decimal(r['total_unrounded']))<Decimal('.000001'),r['agency']
    assert Decimal(r['public_score'])==score.quantize(Decimal('1'),rounding=ROUND_HALF_UP)
for i,r in enumerate(rows):
    assert i==0 or Decimal(rows[i-1]['total_unrounded'])>=Decimal(r['total_unrounded'])
    rank=1+sum(Decimal(p['total_unrounded'])>Decimal(r['total_unrounded']) for p in rows)
    assert rank==int(r['rank_with_ties']),r['agency']
print(f'OK: {len(rows)} agencies, {len(rows)*len(w)} cells')
for r in rows:
    print(f"{r['rank_with_ties']:>2}. {r['agency']}: {r['total_unrounded']}/100")
