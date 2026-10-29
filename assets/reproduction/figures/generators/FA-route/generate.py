#!/usr/bin/env python3
"""Private stage export of the reusable FA proof-route panel only."""
from pathlib import Path
import sys,json,hashlib,datetime,argparse
HERE=Path(__file__).resolve();BASE=HERE.parents[2];sys.path.insert(0,str(BASE))
import figstyle as fs
from route_panel import draw_route_panel
ROOT=fs.ROOT;DEST=ROOT/'evidence/figures/builds/FA-route.json';STAGE=ROOT/'evidence/figures/staging/FA-proof-route'

def identity(p):return {'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}

def main(overwrite=False):
    targets=[Path(str(STAGE)+suffix+'.'+ext) for suffix in ['', '-mobile'] for ext in ['svg','png']]
    if not overwrite and (DEST.exists() or any(p.exists() for p in targets)):raise SystemExit('Existing stage outputs; --overwrite only for an observed repair.')
    old=json.loads(DEST.read_text()) if DEST.exists() else {};now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    attempt={'started_at_utc':now,'command':'python -B assets/reproduction/figures/generators/FA-route/generate.py'+(' --overwrite' if overwrite else ''),'status':'running','private_asset_writes':0,'layout_exports':0}
    record={'id':'FA-route','parent_figure':'FA','step':'7.14','author':'JoonHo Lee (jlee296@ua.edu)','status':'STAGING','at_utc':now,
      'scope':'Proof-route stage only; literal public symbolic labels and frozen public style. No final FA asset or numerical/scientific run.',
      'inputs':[identity(p) for p in [HERE,HERE.parent/'route_panel.py',BASE/'figstyle.py']],
      'execution_history':old.get('execution_history',[])+[attempt],'views':old.get('views',[]),'repairs':old.get('repairs',[]),
      'public_reuse_interface':'Import public FA-route/route_panel.py and call draw_route_panel(fig,rect,mobile). Private staging files are not final runtime inputs.',
      'publication_and_licenses':'Deferred'}
    STAGE.parent.mkdir(parents=True,exist_ok=True);DEST.parent.mkdir(parents=True,exist_ok=True)
    try:
        files=[];layouts=[]
        for mobile in [False,True]:
            fig=fs.canvas(4.8 if mobile else 10.8,15.5 if mobile else 7.6,mobile)
            layout=draw_route_panel(fig,mobile=mobile);layouts.append(layout)
            for ext in ['svg','png']:
                p=Path(str(STAGE)+('-mobile' if mobile else '')+'.'+ext)
                fig.savefig(p,dpi=160,metadata={'Date':None,'Creator':'JoonHo Lee (jlee296@ua.edu)'} if ext=='svg' else {'Author': 'JoonHo Lee (jlee296@ua.edu)', 'Software': 'Matplotlib'})
                files.append(identity(p));attempt['private_asset_writes']+=1
            fs.plt.close(fig);attempt['layout_exports']+=1
        record['outputs']=files;record['layouts']=layouts;attempt['status']='succeeded';record['status']='staged'
    except Exception as exc:attempt['status']='failed';attempt['error']=str(exc);record['status']='STAGE_FAILED';raise
    finally:
        attempt['finished_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
        hist=record['execution_history'];record['execution']={'producer_commands':len(hist),'complete_commands':sum(x['status']=='succeeded' for x in hist),'failed_commands':sum(x['status']=='failed' for x in hist),'private_asset_writes':sum(x['private_asset_writes'] for x in hist),'layout_exports':sum(x['layout_exports'] for x in hist),'final_public_asset_writes':0,'numerical_fixture_runs':0,'model_solver_simulation_runs':0}
        DEST.write_text(json.dumps(record,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'id':'FA-route','outputs':record.get('outputs'),'execution':record['execution']}))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--overwrite',action='store_true');main(p.parse_args().overwrite)
