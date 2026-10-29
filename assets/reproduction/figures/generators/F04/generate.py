"""F04 exact deterministic transformation panels; public frozen coordinates only."""
from pathlib import Path
from fractions import Fraction as F
import argparse,datetime,hashlib,json,sys
HERE=Path(__file__).resolve();FIGURES=HERE.parents[2];ROOT=FIGURES.parents[2]
sys.path.insert(0,str(FIGURES))
import figstyle as fs
C=fs.PALETTE;STEM='f04-units-transformations-and-target-choice';DATA=FIGURES/'data/transformations-protections.json'
SCENARIOS=[
 ('original','(a) Original targets\nOriginal composite\n'+r'$a=(1/2,1/2)$','A > B = C'),
 ('rescaled_fixed_coefficients','(b) Positive rescaling\n'+r'$\theta_2/10$, fixed coefficients'+'\n'+r'$a=(1/2,1/2)$','C > B > A'),
 ('rescaled_compensated_coefficients','(c) Same rescaling\nCompensated '+r'$a=(1/2,5)$'+'\n(no normalization)','A > B = C'),
 ('absolute_second_target','(d) Absolute value\nof original criterion 2\nOriginal '+r'$a=(1/2,1/2)$','C > A > B')]

UNITS=[('A',C['teal'],'^'),('B',C['ochre'],'o'),('C',C['rust'],'s')]

def checked_coordinates():
 d=json.loads(DATA.read_text());rows=d['transformation_rows'];coeff=d['transformation_coefficients']
 assert [r['unit'] for r in rows]==['A','B','C']
 assert [r['targets'] for r in rows]==[[-2,4],[1,0],[2,-1]]
 assert coeff=={'original_a':['1/2','1/2'],'compensated_a':['1/2','5'],'directional_w':['1/2','1/2']}
 checks=[]
 for row in rows:
  x,y=map(F,row['targets']);vals=[(x+y)/2,(x+y/10)/2,x/2+5*(y/10),(x+abs(y))/2]
  for (key,_,_),value in zip(SCENARIOS,vals):
   assert value==F(row[key]);checks.append({'unit':row['unit'],'scenario':key,'value':str(value),'status':'PASS'})
 original={r['unit']:F(r['original']) for r in rows};fixed={r['unit']:F(r['rescaled_fixed_coefficients']) for r in rows}
 assert original['A']>original['B']==original['C'] and fixed['A']<fixed['B']<fixed['C']
 assert all(F(r['rescaled_compensated_coefficients'])==F(r['original']) for r in rows)
 assert F(coeff['compensated_a'][0])+F(coeff['compensated_a'][1])==F(11,2)
 # All three forward criterion directions are preserved by positive rescaling.
 targets=[r['targets'] for r in rows]
 for i,j in [(0,1),(0,2),(1,2)]:
  before=[int(targets[i][k]<=targets[j][k]) for k in range(2)]
  after=[int(F(targets[i][k])/(10 if k==1 else 1)<=F(targets[j][k])/(10 if k==1 else 1)) for k in range(2)]
  assert before==after==[1,0]
 assert [int(targets[1][0]<=targets[2][0]),int(abs(targets[1][1])<=abs(targets[2][1]))]==[1,1]
 return rows,coeff,checks

def draw(ax,rows,scenario,mobile=False):
 key,title,order=SCENARIOS[scenario]
 ax.set(xlim=(-1.05,1.85),ylim=(-.40,2.40))
 ax.set_yticks([2,1,0],['A','B','C']);ax.tick_params(axis='y',length=0,pad=8,labelsize=13.5 if mobile else 12)
 ax.set_xticks([-1,0,.5,1,1.5],['−1','0','1/2','1','3/2']);ax.tick_params(axis='x',labelsize=12.5 if mobile else 11)
 ax.set_xlabel('' if mobile else 'Composite value',fontsize=12.5 if mobile else 11.5,labelpad=7)
 ax.set_title(title,fontsize=13 if mobile else 12,loc='left',pad=19,linespacing=1.3)
 for spine in ['top','right','left']:ax.spines[spine].set_visible(False)
 ax.spines['bottom'].set_color(C['line']);ax.axvline(0,color=C['line'],linewidth=.85,zorder=0)
 for idx,(unit,color,marker) in enumerate(UNITS):
  row=rows[idx];value=F(row[key]);y=2-idx
  ax.hlines(y,-1.05,1.85,color=C['line'],linewidth=.55,alpha=.65,zorder=0)
  ax.scatter([float(value)],[y],s=80 if mobile else 66,marker=marker,facecolor='white',edgecolor=color,linewidth=1.6,zorder=3)
  label=str(value).replace('-','−')
  ax.annotate(label,xy=(float(value),y),xytext=(8,4),textcoords='offset points',ha='left',va='bottom',fontsize=12.5 if mobile else 11.5,color=C['ink'])
 # Same x coordinate for B/C ties; categorical y rows are unit identities, not numeric jitter.
 ax.text(.5,-.23 if mobile else -.45,('Order: ' if mobile else 'Composite order\n')+order,transform=ax.transAxes,ha='center',va='top',fontsize=12.5 if mobile else 11.5)
 return {'scenario':key,'values':{r['unit']:r[key] for r in rows},'same_x_scale':[-1.05,1.85],'categorical_unit_rows':['A','B','C'],'composite_order':order,'numeric_jitter':False}

def generate(overwrite=False):
 dest=ROOT/'evidence/figures/builds/F04.json';prior=json.loads(dest.read_text()) if dest.exists() else None
 existing=[ROOT/'assets/figures'/(STEM+suffix+'.'+ext) for suffix in ['', '-mobile'] for ext in ['svg','pdf','png']]
 if not overwrite and (dest.exists() or any(p.exists() for p in existing)):raise SystemExit('Existing F04 outputs: --overwrite is only for an authorized observed repair.')
 rows,coeff,checks=checked_coordinates();outputs=[];layouts=[]
 for mobile in [False,True]:
  semantics=[]
  if mobile:
   fig=fs.canvas(4.8,16.5,True)
   fig.text(.06,.99,'Units, transformations\nand target choice',ha='left',va='top',fontsize=15,fontweight='bold',linespacing=1.2)
   fig.text(.06,.943,'Exact targets: A = (−2, 4),\nB = (1, 0), C = (2, −1)',ha='left',va='top',fontsize=12.5,linespacing=1.3)
   for idx,y in enumerate([.75,.55,.35,.15]):semantics.append(draw(fig.add_axes([.16,y,.79,.105]),rows,idx,True))
   fig.text(.06,.065,'All panels share the composite-value scale.\nPositive rescaling preserves criterion directions.\nAbsolute value changes the signed target.\nCardinal a combines magnitudes;\nw = (1/2, 1/2) weights directional mistakes.',ha='left',va='top',fontsize=11.5,linespacing=1.35)
  else:
   fig=fs.canvas(10.8,7.2,False)
   fig.text(.055,.98,'Units, transformations and target choice',ha='left',va='top',fontsize=16,fontweight='bold')
   fig.text(.055,.915,'Exact synthetic targets: A = (−2, 4), B = (1, 0), C = (2, −1)',ha='left',va='top',fontsize=12.5)
   for idx in range(4):semantics.append(draw(fig.add_axes([.055+idx*.24,.37,.205,.35]),rows,idx,False))
   fig.text(.055,.11,'Positive rescaling preserves criterion directions; absolute value changes the signed target.',ha='left',va='top',fontsize=12)
   fig.text(.055,.055,'Cardinal a combines magnitudes; w = (1/2, 1/2) weights directional mistakes.',ha='left',va='top',fontsize=12)
  layouts.append(semantics);outputs.extend(fs.export(fig,STEM,mobile))
 assert layouts[0]==layouts[1]
 inputs=[HERE,FIGURES/'figstyle.py',DATA]
 record={'id':'F04','fig_label':'fig-vis-f04','step':'3.8','created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'rendered','command':'python3 -B assets/reproduction/figures/generators/F04/generate.py'+(' --overwrite' if overwrite else ''),'inputs':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in inputs],'source_refs':['chapters/04-measurement-values.qmd'],'outputs':outputs,'coordinate_selector':'Only transformation_coefficients and transformation_rows from public JSON; no protection fields used.','exact_coordinate_checks':checks,'exact_coordinate_check_count':len(checks),'semantic_checks':['Original B/C tie at1/2 preserved without numeric jitter.','Positive second-criterion rescaling reverses A/B composite order only with fixed a.','Unnormalized compensated a=(1/2,5),sum11/2,restores original values exactly.','Absolute value applied to original signed secondcriterion changes the target.','Criterion directional indicators preserved by positive rescaling; absolute secondcriterion changes B>C errorvector to(1,1).'],'displayed_coordinates':layouts[0],'encoding':'Stable unit rows and labeledmarker shapes: Atriangle/teal,Bcircle/ochre,Csquare/rust; allpanels sharexlimitsandnumericunits. No uncertaintybands or noisydata.','actual_render_invocations':1,'actual_PNG_views':0,'views':[],'repairs':[],'publication_and_licenses':'Deferred','scope':'Matplotlib rendering and small exact Fraction checks; no model,optimizer,posterior draws or original scientific main-program execution.'}
 if prior:
  for key in ['views','repairs','actual_PNG_views','personal_view_limits']:
   if key in prior:record[key]=prior[key]
  record['actual_render_invocations']=prior.get('actual_render_invocations',1)+1
  record['previous_export_history']=prior.get('previous_export_history',[])+[{'created_at_utc':prior['created_at_utc'],'outputs':prior['outputs']}]
 dest.parent.mkdir(exist_ok=True,parents=True);dest.write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({'receipt':str(dest.relative_to(ROOT)),'outputs':outputs,'exact_coordinates_checked':len(checks)},indent=2))
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--overwrite',action='store_true');generate(parser.parse_args().overwrite)
