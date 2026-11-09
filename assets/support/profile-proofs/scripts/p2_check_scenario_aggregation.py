#!/usr/bin/env python3
"""Exact proof-example replay for T12, independent of the future R evaluator."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations
import json

ROOT = Path(__file__).resolve().parents[1]
checks = 0
def ck(x):
    global checks
    assert x
    checks += 1

def counts(theta, grades):
    n, D = len(theta), len(theta[0])
    F, N = [0]*D, [0]*D
    for d in range(D):
        for i,j in combinations(range(n),2):
            if grades[i][d] == grades[j][d]:
                continue
            a,b = (i,j) if grades[i][d] < grades[j][d] else (j,i)
            N[d] += 1
            F[d] += theta[a][d] <= theta[b][d]
    return tuple(F),tuple(N)

def signature(theta, bank, ts, weights, tau):
    result=[]
    for g in bank:
        F,N=counts(theta,g);M=Q(len(g)*(len(g)-1),2)
        loss=sum(w*(f+tau*(M-n)) for w,f,n in zip(weights,F,N))/M
        union=int(any(f>t*n for f,t,n in zip(F,ts,N)))
        result.append((loss,union))
    return tuple(result)

g1=((1,),(2,),(3,));w1=((1,),(1,),(1,))
a1=((3,),(2,),(1,));b1=((1,),(2,),(3,))
ck(signature(a1,[w1],[Q(0)],[Q(1)],Q(1,4)) ==
   signature(b1,[w1],[Q(0)],[Q(1)],Q(1,4)))
sa=signature(a1,[g1],[Q(0)],[Q(1)],Q(1,4))[0]
sb=signature(b1,[g1],[Q(0)],[Q(1)],Q(1,4))[0]
ck(sa==(Q(0),0) and sb==(Q(1),1))
ck(tuple((x+y)/2 for x,y in zip(sa,sb))==(Q(1,2),Q(1,2)))

a=((3,3),(2,1),(1,2));b=((3,3),(1,2),(2,1))
g=((1,1),(2,2),(3,3));w=((1,1),(1,1),(1,1))
weights=[Q(1,2)]*2;bank=[w,g]
old=[Q(1,2)]*2;new=[Q(0),Q(1,2)]
ck(counts(a,g)==((0,1),(3,3)) and counts(b,g)==((1,0),(3,3)))
s0=signature(a,bank,old,weights,Q(1,4))
ck(s0==signature(b,bank,old,weights,Q(1,4)))
ck(s0==((Q(1,4),0),(Q(1,6),0)))
sA=signature(a,bank,new,weights,Q(1,4))
sB=signature(b,bank,new,weights,Q(1,4))
ck(sA[1]==(Q(1,6),0) and sB[1]==(Q(1,6),1))
ck(Q(sA[1][1]+sB[1][1],2)==Q(1,2))
# General finite pushforward identity for a mixed rational law and repeated states.
states=[a,b,a,b,a];mass=[Q(1,10),Q(1,5),Q(3,10),Q(1,10),Q(3,10)]
ck(sum(mass)==1)
for thresholds in (old,new,[Q(0),Q(0)],[Q(1),Q(1)]):
    sigs=[signature(s,bank,thresholds,weights,Q(1,4)) for s in states]
    blocks={}
    for sig,p in zip(sigs,mass):blocks[sig]=blocks.get(sig,Q(0))+p
    ck(sum(blocks.values())==1)
    for candidate in range(2):
        for coord in range(2):
            direct=sum(p*sig[candidate][coord] for p,sig in zip(mass,sigs))
            compressed=sum(p*sig[candidate][coord] for sig,p in blocks.items())
            ck(direct==compressed)
out={'status':'PASS','assertions':checks,'arithmetic':'fractions.Fraction',
     'new_candidate_true_R_J':['1/2','1/2'],'new_candidate_old_representative_R_J':['0','0'],
     'changed_threshold_true_J':'1/2','changed_threshold_old_representative_J':'0',
     'scope':'T12 finite examples and pushforward replay, not an R implementation or sampling certificate'}
path=ROOT/'results/p2-v1/proofs/T12-scenario-aggregation.json'
path.parent.mkdir(parents=True,exist_ok=True)
path.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
