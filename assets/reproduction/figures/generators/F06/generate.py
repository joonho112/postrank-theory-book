"""F06 symbolic uncertainty objects; no calculated probabilities or interval endpoints.

Labels and native-object glyphs are original. Runtime inputs are public source
and style files only; geometry has no quantitative interpretation.
"""
from pathlib import Path
import argparse,datetime,hashlib,json,sys
HERE=Path(__file__).resolve();FIGURES=HERE.parents[2];ROOT=FIGURES.parents[2]
sys.path.insert(0,str(FIGURES))
import figstyle as fs
from matplotlib.patches import FancyBboxPatch
C=fs.PALETTE;STEM='f06-four-uncertainty-statements-about-the-same-units'
TITLES=['(a) Rank confidence set','(b) One posterior comparison','(c) A strict joint statement','(d) Future-observation buckets']
LAW=[r'Law: repeated sampling $P$',r'Law: posterior $\Pi_s(\cdot\mid y)$',r'Law: posterior $\Pi_s(\cdot\mid y)$','Law: NPI predictive probabilities']
VARIES=[r'Data vary; rank $r_j(P)$ is fixed','Latent state varies; data y are fixed','Latent state varies jointly; y is fixed','One future observation varies per group']

def header(ax,idx,mobile=False):
 ax.set(xlim=(0,1),ylim=(0,1));ax.axis('off')
 ax.add_patch(FancyBboxPatch((.005,.01),.99,.98,boxstyle='round,pad=.008,rounding_size=.02',facecolor='white',edgecolor=C['line'],linewidth=1,zorder=0))
 ax.text(.04,.95,TITLES[idx],ha='left',va='top',fontsize=14 if mobile else 13.5,fontweight='bold')
 fs.box(ax,.04,.80,.92,.085,LAW[idx],fc=C['light'],ec=C['light'],size=12.5 if mobile else 12)
 ax.text(.04,.748,VARIES[idx],ha='left',va='top',fontsize=12 if mobile else 11.5,color=C['muted'])

def connect(ax,a,b):
 aa=a.get_bbox();bb=b.get_bbox();fs.arrow(ax,(aa.x0+aa.width/2,aa.y0+aa.height/2),(bb.x0+bb.width/2,bb.y0+bb.height/2),patchA=a,patchB=b,color=C['muted'])

def draw_card(ax,idx,mobile=False):
 header(ax,idx,mobile);size=13 if mobile else 12.5
 if idx==0:
  fs.box(ax,.12,.485,.76,.17,r'$R_{n,j}(Y)$'+'\nData-dependent rank set',size=size)
  ax.text(.05,.365,'One j:',ha='left',va='center',fontsize=size)
  ax.text(.95,.365,r'$r_j(P)\in R_{n,j}(Y)$',ha='right',va='center',fontsize=size)
  ax.text(.05,.24,'All j:',ha='left',va='center',fontsize=size)
  ax.text(.95,.24,r'$\forall j:\ r_j(P)\in R_{n,j}(Y)$',ha='right',va='center',fontsize=size)
  ax.text(.05,.09,'Marginal and simultaneous coverage\nare distinct event scopes.',ha='left',va='center',fontsize=12 if mobile else 11.5,linespacing=1.3)
 elif idx==1:
  a=fs.box(ax,.12,.47,.24,.17,'A',size=16);b=fs.box(ax,.64,.47,.24,.17,'B',size=16);connect(ax,a,b)
  ax.text(.5,.64,'greater than',ha='center',va='bottom',fontsize=11.5,color=C['muted'])
  ax.text(.5,.335,r'$E_{AB}=\{\theta_A>\theta_B\}$',ha='center',va='center',fontsize=size)
  ax.text(.5,.205,r'$\Pi_s(E_{AB}\mid y)$',ha='center',va='center',fontsize=size+1)
  ax.text(.5,.075,'C is not compared.',ha='center',va='center',fontsize=12 if mobile else 11.5,color=C['muted'])
 elif idx==2:
  ax.add_patch(FancyBboxPatch((.07,.30),.86,.385,boxstyle='round,pad=.008,rounding_size=.015',facecolor='white',edgecolor=C['line'],linestyle='--',linewidth=.9,zorder=0))
  a=fs.box(ax,.38,.53,.24,.125,'A',size=15);b=fs.box(ax,.13,.32,.24,.125,'B',size=15);c=fs.box(ax,.63,.32,.24,.125,'C',size=15);connect(ax,a,b);connect(ax,a,c)
  ax.text(.5,.465,'AND',ha='center',va='center',fontsize=11.5,color=C['muted'],bbox={'facecolor':'white','edgecolor':'none','pad':1})
  ax.text(.5,.225,'B versus C unspecified',ha='center',va='center',fontsize=12 if mobile else 11.5,color=C['muted'])
  ax.text(.5,.12,r'$\Pi_s(E_{AB}\cap E_{AC}\mid y)$',ha='center',va='center',fontsize=size)
  ax.text(.5,.045,'Strict conjunction example',ha='center',va='center',fontsize=11.5,color=C['muted'])
 else:
  ax.text(.5,.675,'Earlier bucket: lower future values',ha='center',va='center',fontsize=12 if mobile else 11.5)
  a=fs.box(ax,.065,.445,.405,.17,'Bucket 1: A, B\n'+r'$X_A^f,\ X_B^f$',size=size)
  b=fs.box(ax,.60,.445,.335,.17,'Bucket 2: C\n'+r'$X_C^f$',size=size);connect(ax,a,b)
  ax.text(.535,.615,'<',ha='center',va='bottom',fontsize=16,color=C['muted'])
  ax.text(.5,.33,r'$\mathcal{A}=\{\max(X_A^f,X_B^f)<X_C^f\}$',ha='center',va='center',fontsize=12 if mobile else 11.5)
  ax.text(.5,.205,r'$P_{\rm low}(\mathcal{A}),\quad P_{\rm up}(\mathcal{A})$',ha='center',va='center',fontsize=size)
  ax.text(.5,.075,'Within a bucket: order unspecified',ha='center',va='center',fontsize=12 if mobile else 11.5,color=C['muted'])

def generate(overwrite=False):
 dest=ROOT/'evidence/figures/builds/F06.json';prior=json.loads(dest.read_text()) if dest.exists() else None
 existing=[ROOT/'assets/figures'/(STEM+suffix+'.'+ext) for suffix in ['', '-mobile'] for ext in ['svg','pdf','png']]
 if not overwrite and (dest.exists() or any(p.exists() for p in existing)):raise SystemExit('Existing F06 outputs: --overwrite is only for an authorized observed repair.')
 outputs=[]
 for mobile in [False,True]:
  if mobile:
   fig=fs.canvas(4.8,18.4,True);fig.text(.055,.992,'Four uncertainty objects',ha='left',va='top',fontsize=15,fontweight='bold');fig.text(.055,.969,'Same groups; different targets and laws',ha='left',va='top',fontsize=11.5,color=C['muted'])
   rects=[(.025,y,.95,.22) for y in [.72,.485,.25,.015]]
  else:
   fig=fs.canvas(10.8,10.4,False);fig.text(.04,.985,'Four uncertainty objects',ha='left',va='top',fontsize=16,fontweight='bold');fig.text(.04,.945,'The group labels are shared; events, targets and probability laws retain their own meanings.',ha='left',va='top',fontsize=12,color=C['muted'])
   rects=[(.035,.505,.445,.405),(.52,.505,.445,.405),(.035,.05,.445,.405),(.52,.05,.445,.405)]
  for idx,rect in enumerate(rects):draw_card(fig.add_axes(rect),idx,mobile)
  outputs.extend(fs.export(fig,STEM,mobile))
 inputs=[HERE,FIGURES/'figstyle.py']
 semantic=[{'object':'Rank set','random_target':'Set varies with data; fixed populationrank under P','law':'Repeated sampling P','event_scope':'One j coverage versus all-j coverage; no automatic finitelevel guarantee.'},{'object':'Elementary posterior comparison','target':'Latent theta_A versus theta_B','law':'Supplied joint posterior at y','event':'E_AB={theta_A>theta_B}; C unspecified.'},{'object':'Strict joint posterior comparison','target':'Latent state jointly','law':'Same supplied joint posterior at y','event':'E_AB intersect E_AC; B:C remains unspecified; no multiplication/independence substitution.'},{'object':'Predictive buckets','target':'One nextobservation from each group','law':'NPI lower/upper predictive probabilities under source assumptions','event':'max(X_A^f,X_B^f)<X_C^f; earlierbucket haslowerfuturevalues; withinbucketorder unspecified.'}]
 record={'id':'F06','fig_label':'fig-vis-f06','step':'3.10','created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'rendered','command':'python3 -B assets/reproduction/figures/generators/F06/generate.py'+(' --overwrite' if overwrite else ''),'inputs':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in inputs],'source_refs':['chapters/06-uncertainty-ordering.qmd'],'outputs':outputs,'semantic_objects':semantic,'source_scope':'Read canonicalrankconfidence/posteriorevent andpredictivebucketsections; no neworiginalpaperreading or empiricalnumericalanalysis.','probability_notation':'P_low andP_up are declared symbolic NPIlower/upper probabilities; no numericvalues orintervalendpoints are calculated orplotted.','geometry':'Card sizes,tokenpositions andarrowlengths are nonquantitative. Comparison arrows indicate strictgreater-than events; futurebucketarrowfollows explicitlylabelled lower-to-higher orientation.','actual_render_invocations':1,'actual_PNG_views':0,'views':[],'repairs':[],'publication_and_licenses':'Deferred','executions':{'probability_calculations':0,'numeric_intervals':0,'posterior_samples':0,'optimizer':0,'model_fit':0}}
 if prior:
  for key in ['views','repairs','actual_PNG_views','personal_view_limits']:
   if key in prior:record[key]=prior[key]
  record['actual_render_invocations']=prior.get('actual_render_invocations',1)+1;record['previous_export_history']=prior.get('previous_export_history',[])+[{'created_at_utc':prior['created_at_utc'],'outputs':prior['outputs']}]
 dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({'receipt':str(dest.relative_to(ROOT)),'outputs':outputs},indent=2))
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--overwrite',action='store_true');generate(parser.parse_args().overwrite)
