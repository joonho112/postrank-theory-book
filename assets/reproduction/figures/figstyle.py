"""Shared deterministic figure primitives for the P1 monograph.
Original figure source; licensing decision is deferred with the manuscript.
"""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch,FancyArrowPatch
import textwrap, json, hashlib
ROOT=Path(__file__).resolve().parents[3]
PALETTE={'ink':'#20333B','muted':'#5C6B73','teal':'#126D76','ochre':'#A1731D','rust':'#A54732','light':'#EDF3F2','line':'#CAD5D7','gray':'#859398','white':'#FFFFFF'}
def setup(mobile=False):
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':13.5 if mobile else 12,'axes.titlesize':14 if mobile else 14,'axes.labelsize':13 if mobile else 12,'xtick.labelsize':12.5 if mobile else 11,'ytick.labelsize':12.5 if mobile else 11,'legend.fontsize':12 if mobile else 10.5,'text.color':PALETTE['ink'],'axes.labelcolor':PALETTE['ink'],'xtick.color':PALETTE['muted'],'ytick.color':PALETTE['muted'],'axes.edgecolor':PALETTE['line'],'axes.spines.top':False,'axes.spines.right':False,'axes.grid':False,'figure.facecolor':'white','axes.facecolor':'white','savefig.facecolor':'white','svg.fonttype':'path','svg.hashsalt':'P1-figure-program-v1','pdf.fonttype':42,'mathtext.fontset':'dejavusans'})
def canvas(width=10,height=6,mobile=False):
 setup(mobile);fig=plt.figure(figsize=(width,height));return fig

def clean(ax,grid='y'):
 ax.spines[['top','right']].set_visible(False)
 if grid:ax.grid(axis=grid,color=PALETTE['line'],linewidth=.6,alpha=.65);ax.set_axisbelow(True)
 return ax

def box(ax,x,y,w,h,text,fc=None,ec=None,size=12,weight='normal',align='center',wrap=None):
 rect=FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.012,rounding_size=0.012',facecolor=fc or PALETTE['light'],edgecolor=ec or PALETTE['line'],linewidth=1,zorder=2)
 ax.add_patch(rect)
 if wrap:text='\n'.join(textwrap.fill(line,wrap) for line in text.split('\n'))
 ax.text(x+w/2 if align=='center' else x+.025,y+h/2,text,ha=align,va='center',fontsize=size,fontweight=weight,color=PALETTE['ink'],zorder=3,linespacing=1.25)
 return rect

def arrow(ax,start,end,color=None,style='-',label=None,size=11,rad=0,patchA=None,patchB=None):
 # Clip connectors against supplied actual node patches, above box backgrounds.
 ax.add_patch(FancyArrowPatch(start,end,patchA=patchA,patchB=patchB,shrinkA=2,shrinkB=3,arrowstyle='-|>',mutation_scale=13,linewidth=1.3,color=color or PALETTE['muted'],linestyle=style,connectionstyle=f'arc3,rad={rad}',zorder=4))
 if label:ax.text((start[0]+end[0])/2,(start[1]+end[1])/2,label,ha='center',va='center',fontsize=size,color=color or PALETTE['muted'],bbox={'facecolor':'white','edgecolor':'none','pad':2})

def diagram_axis(fig,rect=(.02,.02,.96,.96)):
 ax=fig.add_axes(rect);ax.set(xlim=(0,1),ylim=(0,1));ax.axis('off');return ax

def export(fig,stem,mobile=False):
 p=ROOT/'assets/figures'/stem;p.parent.mkdir(parents=True,exist_ok=True)
 if mobile:p=p.with_name(p.name+'-mobile')
 out=[]
 for ext in ['svg','pdf','png']:
  q=p.with_suffix('.'+ext)
  metadata={'Date':None,'Creator':'JoonHo Lee (jlee296@ua.edu)'} if ext=='svg' else {'CreationDate': None, 'ModDate': None, 'Creator': 'JoonHo Lee (jlee296@ua.edu)', 'Author': 'JoonHo Lee (jlee296@ua.edu)'} if ext=='pdf' else {'Author': 'JoonHo Lee (jlee296@ua.edu)', 'Software': 'Matplotlib'}
  fig.savefig(q,dpi=160,metadata=metadata,bbox_inches=None);out.append({'path':str(q.relative_to(ROOT)),'sha256':hashlib.sha256(q.read_bytes()).hexdigest(),'bytes':q.stat().st_size})
 plt.close(fig);return out

def record(fid,files,inputs=None,notes=None):
 p=ROOT/'evidence/figures/builds'/f'{fid}.json';p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps({'id':fid,'scope':'Figure rendering from declared source/coordinates; not a package or empirical model run','outputs':files,'inputs':inputs or [],'notes':notes or []},indent=2)+'\n')
