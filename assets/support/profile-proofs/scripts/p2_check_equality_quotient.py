#!/usr/bin/env python3
"""Exact T10 grouping checks; no production package dependence."""
from pathlib import Path
from itertools import product,combinations
from fractions import Fraction as Q
import json
ROOT=Path(__file__).resolve().parents[1]
checks=cases=empty=0
def ck(x):
    global checks
    assert x
    checks+=1
def direct(theta,g,pairs):
    issued=[(i,j) if g[i]<g[j] else (j,i) for i,j in pairs if g[i]!=g[j]]
    return len(issued),sum(theta[i]<=theta[j] for i,j in issued)
def quotient(theta,g,classes,pairs):
    membership={i:c for c,block in enumerate(classes) for i in block}
    reps=[block[0] for block in classes]
    multiplicities={}
    for i,j in pairs:
        c,e=sorted((membership[i],membership[j]))
        if c!=e:multiplicities[(c,e)]=multiplicities.get((c,e),0)+1
    N=F=0
    for (c,e),m in multiplicities.items():
        i,j=reps[c],reps[e]
        if g[i]==g[j]:continue
        a,b=(i,j) if g[i]<g[j] else (j,i)
        N+=m;F+=m*int(theta[a]<=theta[b])
    return N,F
# Exhaustive coherent crossing-class examples.
classes=[[(0,1),(2,)],[(0,),(1,2)]]
class_maps=[(0,0,1),(0,1,1)]
class_grades=[(1,1),(1,2),(2,1)]
allpairs=list(combinations(range(3),2))
masks=[allpairs,[],[(0,1)],[(0,2)],[(1,2)],[(0,1),(1,2)]]
for a,b,c,d in product((-1,0,1),repeat=4):
    domains=[(a,a,b),(c,d,d)]
    for cg1,cg2 in product(class_grades,repeat=2):
        grades=[tuple(cg1[k] for k in class_maps[0]),tuple(cg2[k] for k in class_maps[1])]
        for k in range(2):
            for mask in masks:
                before=direct(domains[k],grades[k],mask)
                after=quotient(domains[k],grades[k],classes[k],mask)
                ck(before==after);cases+=1
                if before[0]==0:empty+=1;ck(before[1]==0)
            N,F=direct(domains[k],grades[k],allpairs)
            nc,fc=quotient(domains[k],grades[k],classes[k],allpairs)
            ck((Q(F)+Q(1,4)*(3-N))/3==(Q(fc)+Q(1,4)*(3-nc))/3)
# Unequal class-size example in the text.
theta=(3,3,1,2);g=(1,1,2,3);cc=[(0,1),(2,),(3,)]
orig=direct(theta,g,list(combinations(range(4),2)))
comp=quotient(theta,g,cc,list(combinations(range(4),2)))
naive=direct((3,1,2),(1,2,3),list(combinations(range(3),2)))
ck(orig==comp==(5,1));ck(naive==(3,1))
ck(not(orig[1]>Q(1,4)*orig[0]) and naive[1]>Q(1,4)*naive[0])
ck((Q(1)+Q(1,4))/6==Q(5,24))
# One-class domain: retain original M and full withholding cost.
for n in (2,3,4):
    pp=list(combinations(range(n),2));M=len(pp)
    n0,f0=quotient((0,)*n,(1,)*n,[tuple(range(n))],pp)
    ck((n0,f0)==(0,0) and (Q(f0)+Q(1,4)*(M-n0))/M==Q(1,4))
result={'status':'PASS','assertions':checks,'crossing_identity_scoped_count_cases':cases,
        'zero_disclosure_cases':empty,'unequal_class_original_N_F':orig,
        'unequal_class_naive_N_F':naive,'original_loss':'5/24','arithmetic':'exact integers and Fraction',
        'scope':'T10 algebraic replay, not input provenance validation or production solver'}
p=ROOT/'results/p2-v1/proofs/T10-equality-quotient.json';p.parent.mkdir(parents=True,exist_ok=True)
p.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
