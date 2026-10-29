"""F09b: two exact joint probability laws with identical marginals."""
from pathlib import Path
from fractions import Fraction as F
import argparse, csv, datetime, hashlib, json, sys

HERE=Path(__file__).resolve();FIGURES=HERE.parents[2];ROOT=FIGURES.parents[2]
sys.path.insert(0,str(FIGURES))
import figstyle as fs
from matplotlib.patches import Polygon

C=fs.PALETTE;STEM='f09b-equal-marginals-different-comparisons'
DATA=FIGURES/'data/f09-couplings.csv'
META=FIGURES/'data/f09-couplings-metadata.json'


def checked_coordinates():
    rows=list(csv.DictReader(DATA.open()))
    meta=json.loads(META.read_text())
    assert hashlib.sha256(DATA.read_bytes()).hexdigest()==meta['coordinate_sha256']
    assert len(rows)==18
    laws={};checks=[]
    for name in ['Q1','Q2']:
        block=[r for r in rows if r['law']==name]
        assert len(block)==9
        assert {(int(r['A']),int(r['B'])) for r in block}=={(a,b) for a in range(3) for b in range(3)}
        assert len({(r['A'],r['B']) for r in block})==9
        for row in block:
            a,b=int(row['A']),int(row['B']);p=F(row['probability'])
            assert p in [F(0),F(1,3)]
            assert [int(row[k]) for k in ['event_A_gt_B','event_A_eq_B','event_A_lt_B']]==[int(a>b),int(a==b),int(a<b)]
        total=sum(F(r['probability']) for r in block)
        assert total==1
        am={v:sum(F(r['probability']) for r in block if int(r['A'])==v) for v in range(3)}
        bm={v:sum(F(r['probability']) for r in block if int(r['B'])==v) for v in range(3)}
        assert all(p==F(1,3) for p in [*am.values(),*bm.values()])
        gt=sum(F(r['probability']) for r in block if int(r['A'])>int(r['B']))
        eq=sum(F(r['probability']) for r in block if int(r['A'])==int(r['B']))
        lt=sum(F(r['probability']) for r in block if int(r['A'])<int(r['B']))
        assert gt+eq+lt==1 and eq==0
        m=next(m for m in meta['laws'] if m['law']==name)
        assert gt==F(m['P_A_gt_B']) and lt==F(m['P_A_lt_B']) and eq==F(m['P_A_eq_B'])
        support=[{'A':int(r['A']),'B':int(r['B']),'probability':r['probability']} for r in block if F(r['probability'])]
        assert support==m['support']
        assert gt==F(1,3) if name=='Q1' else gt==F(2,3)
        laws[name]={'cells':block,'probability_A_gt_B':str(gt)}
        checks.append({'law':name,'cells':len(block),'explicit_zeros':sum(F(r['probability'])==0 for r in block),
                       'total_probability':str(total),'marginal_A':{v:str(p) for v,p in am.items()},
                       'marginal_B':{v:str(p) for v,p in bm.items()},'P_A_gt_B':str(gt),'P_A_eq_B':str(eq),
                       'P_A_lt_B':str(lt),'support':support,'status':'PASS'})
    return laws,checks


def joint_grid(ax,name,data,mobile=False):
    # A is horizontal and B vertical, so the strict event lies below y=x.
    ax.add_patch(Polygon([(-.5,-.5),(2.5,-.5),(2.5,2.5)],closed=True,
                         facecolor=C['light'],edgecolor='none',zorder=0))
    for t in [-.5,.5,1.5,2.5]:
        ax.axhline(t,color=C['line'],lw=.9,zorder=1)
        ax.axvline(t,color=C['line'],lw=.9,zorder=1)
    ax.plot([-.5,2.5],[-.5,2.5],color=C['gray'],lw=1.1,linestyle=(0,(4,3)),zorder=1)
    plotted=[]
    for row in data['cells']:
        a,b=int(row['A']),int(row['B']);p=F(row['probability']);inside=a>b
        if p:
            ax.scatter([a],[b],s=880 if mobile else 940,marker='o',
                       facecolor=C['teal'] if inside else 'white',edgecolor=C['ink'],lw=1.4,zorder=3)
            ax.text(a,b,row['probability'],ha='center',va='center',fontsize=13 if mobile else 13.5,
                    color='white' if inside else C['ink'],fontweight='bold',zorder=4)
        else:
            ax.text(a,b,'0',ha='center',va='center',fontsize=13.5 if mobile else 13,color=C['muted'],zorder=2,
                    bbox={'facecolor':'white','edgecolor':'none','pad':1})
        plotted.append({'A':a,'B':b,'probability':row['probability'],'inside_A_gt_B':inside})
    ax.set(xlim=(-.5,2.5),ylim=(-.5,2.5),aspect='equal')
    ax.set_xticks([0,1,2]);ax.set_yticks([0,1,2])
    ax.set_xlabel('Target A',labelpad=8);ax.set_ylabel('Target B',labelpad=8)
    ax.tick_params(axis='both',length=0,pad=6)
    for spine in ax.spines.values():spine.set_visible(False)
    q=r'$Q_1$' if name=='Q1' else r'$Q_2$'
    prob=data['probability_A_gt_B']
    ax.set_title('Joint law '+q+'\n'+r'$P(A>B)='+prob+'$',loc='left',pad=15,
                 fontsize=14 if mobile else 14.5,linespacing=1.25)
    return {'law':name,'coordinates':plotted,'x_axis':'A','y_axis':'B','limits':[-.5,2.5],
            'strict_event':'A>B below y=x','probability_A_gt_B':prob,'connections_between_supports':False}


def draw(laws,mobile=False):
    if mobile:
        fig=fs.canvas(4.8,13.4,True)
        fig.text(.06,.985,'Equal marginals,\ndifferent comparisons',ha='left',va='top',fontsize=16,fontweight='bold',linespacing=1.2)
        fig.text(.06,.918,'A and B are each uniform on {0, 1, 2}.\nEach occupied cell has mass 1/3.',ha='left',va='top',fontsize=12,linespacing=1.3)
        semantics=[joint_grid(fig.add_axes([.18,.57,.73,.26]),'Q1',laws['Q1'],True),
                   joint_grid(fig.add_axes([.18,.15,.73,.26]),'Q2',laws['Q2'],True)]
        fig.text(.07,.505,'Every row and column totals 1/3\nin both laws.',ha='left',va='top',fontsize=12,linespacing=1.3)
        fig.text(.06,.068,'Shaded half-plane and filled supports: A > B.\nDashed diagonal: A = B. Other cells have mass 0.',ha='left',va='top',fontsize=11.5,linespacing=1.35)
        fig.text(.06,.023,'Stipulated laws; independence is not assumed.',ha='left',va='top',fontsize=11.2)
    else:
        fig=fs.canvas(10.6,8.2,False)
        fig.text(.06,.965,'Equal marginals, different comparisons',ha='left',va='top',fontsize=17,fontweight='bold')
        fig.text(.06,.91,'Same marginals: A and B are each uniform on {0, 1, 2}.',ha='left',va='top',fontsize=12.5)
        fig.text(.06,.86,'Each occupied cell has probability 1/3; all remaining cells have probability 0.',ha='left',va='top',fontsize=12)
        semantics=[joint_grid(fig.add_axes([.08,.28,.36,.465]),'Q1',laws['Q1']),
                   joint_grid(fig.add_axes([.56,.28,.36,.465]),'Q2',laws['Q2'])]
        fig.text(.06,.20,'Each column and each row sums to 1/3 under both laws. Only the coupling changes.',ha='left',va='top',fontsize=12.5)
        fig.text(.06,.135,'Shaded half-plane and filled supports: A > B.  Dashed diagonal: A = B.',ha='left',va='top',fontsize=12)
        fig.text(.06,.075,'These are stipulated joint laws. Independence would supply a third law.',ha='left',va='top',fontsize=12,color=C['muted'])
    return fig,semantics


def generate(overwrite=False):
    dest=ROOT/'evidence/figures/builds/F09b.json'
    paths=[ROOT/'assets/figures'/(STEM+s+'.'+ext) for s in ['', '-mobile'] for ext in ['svg','pdf','png']]
    if not overwrite and (dest.exists() or any(p.exists() for p in paths)):
        raise SystemExit('Existing F09b outputs: --overwrite is for an authorized observed repair.')
    # The renderer reads no private scientific input or prior build receipt.
    laws,checks=checked_coordinates();now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    record={'id':'F09b','fig_label':'fig-vis-f09b','step':'4.8','author':'JoonHo Lee (jlee296@ua.edu)',
            'created_at_utc':now,'status':'rendering','actual_render_invocations':1,'actual_PNG_views':0,'views':[],'repairs':[],
            'execution_history':[{'started_at_utc':now,'status':'running','command':'python3 -B assets/reproduction/figures/generators/F09b/generate.py'+(' --overwrite' if overwrite else '')}],
            'input_policy':'Only public CSV, public metadata and shared public style are read. The private receipt is written, never read by the renderer. If an observed repair requires another invocation, author bookkeeping must preserve the previous history separately.',
            'inputs':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [HERE,FIGURES/'figstyle.py',DATA,META]],
            'exact_checks':checks,'scope':'Original rendering of two stipulated finite joint laws, not empirical data. No report selection, model, simulation, posterior draws, package or optimizer execution.',
            
            'publication_and_licenses':'Deferred'}
    dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(record,indent=2)+'\n')
    try:
        outputs=[];all_semantics=[]
        for mobile in [False,True]:
            fig,semantics=draw(laws,mobile);all_semantics.append(semantics)
            outputs.extend(fs.export(fig,STEM,mobile))
        assert all_semantics[0]==all_semantics[1]
        record['outputs']=outputs;record['displayed_semantics']=all_semantics[0]
        record['status']='rendered'
        record['execution_history'][0].update({'status':'succeeded','output_count':6,'finished_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
    except Exception as exc:
        record['execution_history'][0].update({'status':'failed','error':str(exc)})
        record['status']='render_failed';dest.write_text(json.dumps(record,indent=2)+'\n');raise
    dest.write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({'receipt':str(dest.relative_to(ROOT)),'outputs':outputs},indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--overwrite',action='store_true')
    generate(parser.parse_args().overwrite)
