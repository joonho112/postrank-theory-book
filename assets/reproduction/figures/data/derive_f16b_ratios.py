#!/usr/bin/env python3
"""Derive Chapter16's three-case denominator example using exact arithmetic.
This creates a small public coordinate packet, not a simulation or figure.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
ROOT=Path(__file__).resolve().parents[4]
OUT=Path(__file__).with_name('f16b-disclosed-error-ratios.json')
SOURCE=ROOT/'chapters/16-evaluation-frontiers.qmd'

def derive():
    cases=[]
    for y,theta,g in [(1,[0,2,1],[1,2,2]),(2,[3,2,1],[1,2,3]),(3,[3,2,1],[1,1,1])]:
        pairs=[];N=A=0
        for i in range(3):
            for j in range(i+1,3):
                direction=None;wrong=None
                if g[i]!=g[j]:
                    above,below=(i,j) if g[i]<g[j] else (j,i)
                    direction=f'{above+1}>{below+1}';wrong=theta[above]<=theta[below]
                    N+=1;A+=int(wrong)
                pairs.append({'unordered_pair':[i+1,j+1],'disclosed':direction is not None,'reported_direction':direction,'weak_direction_error':wrong})
        cases.append({'Y':y,'probability':'1/3','theta':theta,'g':g,'pairs':pairs,'N':N,'A':A,
                      'disclosed_error_fraction':str(F(A,N)) if N else None,
                      'disclosure_fraction':str(F(N,3))})
    assert [(c['A'],c['N']) for c in cases]==[(2,2),(0,3),(0,0)]
    p=F(1,3);EA=sum(p*c['A'] for c in cases);EN=sum(p*c['N'] for c in cases)
    positive=sum(p for c in cases if c['N']);pooled=EA/EN
    conditional=sum(p*F(c['A'],c['N']) for c in cases if c['N'])/positive
    imputed=sum(p*(F(c['A'],c['N']) if c['N'] else F(0)) for c in cases)
    weights=[p*c['N']/EN for c in cases]
    assert sum(w*F(c['A'],c['N']) for w,c in zip(weights,cases) if c['N'])==pooled==F(2,5)
    assert conditional==F(1,2) and imputed==F(1,3)==positive*conditional
    assert positive==F(2,3) and EN/3==F(5,9)
    assert cases[2]['disclosed_error_fraction'] is None
    return {'id':'F16b-three-case-ratio-example','source':'chapters/16-evaluation-frontiers.qmd#sec-disclosed-error-example',
        'source_sha256_at_derivation':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        'scope':'Stipulated joint evaluation law P: Y has three equally probable values,with deterministic target and report conditional on each. These are exact population-case calculations,not Monte Carlo replications or a fixed-dataset posterior mixture.',
        'n':3,'unit_labels':[1,2,3],'K':1,'criterion_weight':'1','M':3,'cases':cases,
        'aggregation':{
            'pooled':{'definition':'E_P[A]/E_P[N]','expected_wrong_count':str(EA),'expected_disclosure_count':str(EN),'value':str(pooled),'nonsilent_outcome_rate_weights':list(map(str,weights))},
            'nonsilent_mean':{'definition':'E_P[A/N | N>0]','conditioning_probability':str(positive),'value':str(conditional),'conditional_case_weights':['1/2','1/2','0']},
            'zero_imputed_mean':{'definition':'E_P[Z],where Z=A/N for N>0 and Z=0 for N=0 by explicit convention','value':str(imputed),'convention_specific_values':['1','0','0'],'identity':'P(N>0)*E_P[A/N | N>0]'},
            'positive_disclosure_probability':str(positive),'mean_disclosure_fraction':str(EN/3)},
        'boundaries':['The silent case has an undefined individual fraction,not zero accuracy or zero observed error rate.','The zero-imputed statistic is separate; it does not change the case record NA.','The three summary values concern different estimands and weighting conventions,not rival estimates of one target.','A is the realized weak-error wrong count in this K1 construction,not the equality-neutral distinct-mass numerator.','No withholding cost,optimization,confidence level,independent-pair sampling or application data is introduced.']}

if __name__=='__main__':
    if OUT.exists():raise SystemExit('Refuse overwrite of accepted public coordinates.')
    data=derive();OUT.write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({'path':str(OUT.relative_to(ROOT)),'sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'case_counts':[[r['A'],r['N']] for r in data['cases']],'values':[data['aggregation'][k]['value'] for k in ['pooled','nonsilent_mean','zero_imputed_mean']]},indent=2))
