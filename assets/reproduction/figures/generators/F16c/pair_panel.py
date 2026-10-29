"""T11 six-original-pair panel; read frozen coordinate CSVs, never run a solver.

draw_panel(ax, mobile=False, title=...) is reusable by the full F16c generator.
Executing this module writes staged panel assets only.
"""
from pathlib import Path
import csv,sys,hashlib,json,datetime
from fractions import Fraction as F
HERE=Path(__file__).resolve();FIGURES=HERE.parents[2];ROOT=FIGURES.parents[2]
sys.path.insert(0,str(FIGURES))
import figstyle as fs
from matplotlib.patches import Rectangle,FancyBboxPatch
DATA=FIGURES/'data';PAIRS=DATA/'t11-pairs.csv';ACTIONS=DATA/'t11-actions.csv'
C=fs.PALETTE

def load_coordinates():
    pairs=list(csv.DictReader(PAIRS.open()))
    actions={r['action_id']:r for r in csv.DictReader(ACTIONS.open())}
    assert [p['pair'] for p in pairs]==['AB','AC','AD','BC','BD','CD']
    assert [F(p['weighted_distinct_delta']) for p in pairs]==[F(0),F(1,4),F(1),F(1,4),F(1),F(1)]
    rows=[]
    for aid,key,blocks in [('T11_2211','CD_above_AB',[['C','D'],['A','B']]),('T11_2221','D_above_ABC',[['D'],['A','B','C']])]:
        row=actions[aid];mask=[bool(int(p['disclosed_'+key])) for p in pairs]
        assert sum(mask)==int(row['raw_disclosed_N'])
        assert sum((F(p['weighted_distinct_delta']) for p,on in zip(pairs,mask) if on),F(0))==F(row['distinct_disclosed_Q'])
        rows.append({'action_id':aid,'report':row['report'],'blocks':blocks,'mask':mask,'N':int(row['raw_disclosed_N']),'Q':row['distinct_disclosed_Q'],'pairs':[p['pair'] for p,on in zip(pairs,mask) if on]})
    assert rows[0]['pairs']==['AC','AD','BC','BD']
    assert rows[1]['pairs']==['AD','BD','CD']
    return pairs,rows

def _mass_text(value):
    return r'$1/4$' if F(value)==F(1,4) else str(F(value))

def _tile(ax,x,y,w,h,on,size):
    # Fill and check/dash distinguish reporting actions even without color.
    ax.add_patch(Rectangle((x,y),w,h,facecolor=C['ochre'] if on else C['white'],edgecolor=C['ochre'] if on else C['gray'],linewidth=1.1,zorder=2))
    ax.text(x+w/2,y+h/2,'✓' if on else '—',ha='center',va='center',fontsize=size,fontweight='bold' if on else 'normal',color=C['white'] if on else C['muted'],zorder=3)

def _ribbon(ax,center_y,blocks,x=.015,w=.24,size=12):
    # Commas and separate boxes denote within-grade ties, never a strict order.
    first,second=blocks
    widths=[w*.43,w*.43];positions=[x,x+w*.57]
    for xx,ww,group in zip(positions,widths,[first,second]):
        ax.add_patch(FancyBboxPatch((xx,center_y-.063),ww,.126,boxstyle='round,pad=0.005,rounding_size=.008',facecolor=C['light'],edgecolor=C['line'],linewidth=.9))
        ax.text(xx+ww/2,center_y,','.join(group),ha='center',va='center',fontsize=size,fontweight='bold')
    ax.text(x+w/2,center_y,'>',ha='center',va='center',fontsize=size+1,color=C['muted'])

def draw_panel(ax,mobile=False,title='Count the same six original pairs'):
    """Draw the panel into an existing axis and return its exact semantic rows."""
    pairs,rows=load_coordinates();ax.set(xlim=(0,1),ylim=(0,1));ax.axis('off')
    ax.text(.015,.98,title,ha='left',va='top',fontsize=14,fontweight='bold')
    if mobile:
        ax.text(.015,.925,'Weighted distinct mass per pair',ha='left',va='top',fontsize=12.5,color=C['muted'])
        x0=.035;step=.155;tile_w=.130
        for col,p in enumerate(pairs):
            x=x0+col*step
            ax.text(x+tile_w/2,.855,p['pair'],ha='center',va='center',fontsize=13.5,fontweight='bold')
            ax.text(x+tile_w/2,.80,_mass_text(p['weighted_distinct_delta']),ha='center',va='center',fontsize=13.5)
        for row,y,label_y in zip(rows,[.61,.355],[.705,.45]):
            group_label=','.join(row['blocks'][0])+' > '+','.join(row['blocks'][1])
            ax.text(.015,label_y,group_label,ha='left',va='center',fontsize=13.5,fontweight='bold')
            ax.text(.985,label_y,f"N = {row['N']},  Q = {row['Q']}",ha='right',va='center',fontsize=13)
            for col,on in enumerate(row['mask']):_tile(ax,x0+col*step,y-.043,tile_w,.086,on,17)
        ax.text(.015,.235,'Lose AC and BC: mass 1/2.\nGain CD: mass 1.',ha='left',va='top',fontsize=13.5,linespacing=1.35)
        ax.text(.015,.105,'✓ disclosed     — withheld',ha='left',va='center',fontsize=12.5)
        ax.text(.015,.04,'Higher-priority grade first; commas\njoin units in the same grade.',ha='left',va='center',fontsize=11.5,color=C['muted'],linespacing=1.3)
    else:
        ax.text(.015,.895,'Grades: higher first',ha='left',va='center',fontsize=11.5,color=C['muted'])
        x0=.305;step=.0875;tile_w=.067
        for col,p in enumerate(pairs):
            x=x0+col*step
            ax.text(x+tile_w/2,.80,p['pair'],ha='center',va='center',fontsize=12.5,fontweight='bold')
            ax.text(x+tile_w/2,.69,_mass_text(p['weighted_distinct_delta']),ha='center',va='center',fontsize=12.5)
        ax.text(.305,.895,'Original pair',ha='left',va='center',fontsize=11.5,color=C['muted'])
        ax.text(.015,.69,'Weighted distinct mass',ha='left',va='center',fontsize=11.5,color=C['muted'])
        for row,y in zip(rows,[.48,.255]):
            _ribbon(ax,y,row['blocks'],size=12.5)
            for col,on in enumerate(row['mask']):_tile(ax,x0+col*step,y-.075,tile_w,.15,on,17)
            ax.text(.885,y,f"N = {row['N']}\nQ = {row['Q']}",ha='left',va='center',fontsize=12.5,linespacing=1.4)
        ax.text(.015,.055,'✓ disclosed    — withheld',ha='left',va='center',fontsize=11.5)
        ax.text(.985,.055,'Lose AC and BC (mass 1/2); gain CD (mass 1).',ha='right',va='center',fontsize=11.5)
    return {'pairs':[p['pair'] for p in pairs],'pair_masses':[p['weighted_distinct_delta'] for p in pairs],'rows':rows,'conservation':'All six original unordered pairs retained; AB has zero distinct mass and remains explicitly visible.'}

def build_staged():
    out=ROOT/'evidence/figures/staging';out.mkdir(parents=True,exist_ok=True);files=[];semantic=[]
    for mobile,width,height in [(False,10,4.4),(True,4.8,7.2)]:
        fig=fs.canvas(width,height,mobile);ax=fig.add_axes([.025,.025,.95,.95]);semantic.append(draw_panel(ax,mobile))
        stem='F16c-pairs'+('-mobile' if mobile else '')
        for ext in ['svg','png']:
            p=out/(stem+'.'+ext);md={'Date':None,'Creator':'JoonHo Lee (jlee296@ua.edu)'} if ext=='svg' else {'Author': 'JoonHo Lee (jlee296@ua.edu)', 'Software': 'Matplotlib'}
            fig.savefig(p,dpi=160,metadata=md,bbox_inches=None);files.append({'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size})
        fs.plt.close(fig)
    assert semantic[0]==semantic[1]
    inputs=[PAIRS,ACTIONS,FIGURES/'figstyle.py',HERE]
    # Public coordinates suffice; a local private audit contract is optional.
    contract=ROOT/'evidence/figures/contracts/F16c.json'
    if contract.exists(): inputs.append(contract)
    record={'step':'2.8','id':'F16c-pairs','created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'rendered','command':'python3 assets/reproduction/figures/generators/F16c/pair_panel.py','scope':'Staged reusable pair/grade panel only; no final full F16c or canonical insertion. No package, solver, scientific main-program or model execution.','inputs':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in inputs],'outputs':files,'semantic_coordinates':semantic[0],'encoding':'Ochre-filled square plus whitecheck = disclosed; outlined white square plusdash = withheld. Commasjoin unitswithin one grade. The same sixpair columns appear for both actions.','views':[],'limits':['This staged panel omits the normalized-risk curves used in the final figure.','These are the two highlighted reports, not a plot of the entire feasiblefamily or riskpath.'],'required_repairs_remaining':[]}
    dest=ROOT/'evidence/figures/builds/F16c-pairs.json';dest.write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({'receipt':str(dest.relative_to(ROOT)),'outputs':files},indent=2))

if __name__=='__main__':build_staged()
