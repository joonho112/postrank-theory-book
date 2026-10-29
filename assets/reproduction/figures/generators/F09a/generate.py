#!/usr/bin/env python3
"""Original deterministic diagram of two reports and their disclosed pairs.

Only the public exact coordinate packet and shared style are runtime inputs.
No latent values, probability law, loss or optimized report is instantiated.
"""
from pathlib import Path
import sys, json, hashlib, datetime, platform, argparse
BASE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE))
import figstyle as fs
from matplotlib.patches import FancyBboxPatch, Rectangle

ROOT = fs.ROOT
HERE = Path(__file__).resolve()
DATA = BASE / 'data/f09-grade-pairs.json'
DEST = ROOT / 'evidence/figures/builds/F09a.json'
STEM = 'f09a-an-ordered-partition-as-disclosed-pairs'


def render(data, mobile):
    fig = fs.canvas(4.8 if mobile else 10, 10.2 if mobile else 6.8, mobile)
    ax = fs.diagram_axis(fig, (.035, .12, .93, .78))
    title = 'Two grades do not fix the number of disclosed pairs'
    fig.text(.035, .981, 'Two grades, different disclosure' if mobile else title,
             ha='left', va='top', fontsize=15.5 if mobile else 16,
             fontweight='semibold')
    fig.text(.035, .942, 'Same six unordered pairs; grade 1 is highest priority.',
             ha='left', va='top', fontsize=14 if mobile else 12,
             color=fs.PALETTE['muted'])
    if mobile:
        # Wrapping is chosen for a 332-pixel content column, not a shrunken desktop.
        fig.texts[-1].set_text('Same six unordered pairs.\nGrade 1 is highest priority.')
    fig.text(.035, .025,
             ('Filled cell: issued direction.  Dash: withheld.\n'
              'A>B denotes reported priority only.\n'
              'A shared grade does not assert latent equality.') if mobile else
             ('Filled cell: issued direction.  Dash: withheld.  A>B denotes reported priority only.\n'
              'A shared grade withholds comparison; latent values are unspecified.'),
             ha='left', va='bottom', fontsize=14 if mobile else 11.5,
             color=fs.PALETTE['muted'], linespacing=1.25)
    checks, containers, drawn = [], [], []
    size = 14 if mobile else 12

    def text(owner, name, x, y, content, font=size, weight='normal', color=None):
        artist = ax.text(x, y, content, ha='center', va='center', fontsize=font,
                         fontweight=weight, color=color or fs.PALETTE['ink'],
                         linespacing=1.18, zorder=4)
        drawn.append((owner, name, artist))
        return artist

    for number, (report, bottom) in enumerate(zip(data['reports'], [.525, .015]), 1):
        x, w, h = .005, .99, .455
        panel = FancyBboxPatch((x, bottom), w, h,
                              boxstyle='round,pad=0.003,rounding_size=0.008',
                              facecolor='white', edgecolor=fs.PALETTE['line'],
                              linewidth=1, zorder=1)
        ax.add_patch(panel)
        pid = report['id']
        containers.append((pid, panel))
        text(pid, 'report and vector', .5, bottom+h*.91,
             'Report '+str(number)+':  g = ('+', '.join(map(str,report['grades']))+')',
             15 if mobile else 13.5, 'semibold')
        text(pid, 'counts', .5, bottom+h*.79,
             f"G = {report['G']}     N = {report['N']}     M = {report['M']}"
             +f"     N/M = {report['disclosure_fraction']}", size)
        blocks = report['blocks_high_priority_first']
        for blocknum, (bx, bw, block) in enumerate(zip([.115, .575], [.31, .31], blocks), 1):
            rect = Rectangle((bx,bottom+h*.485),bw,h*.22,
                             facecolor=fs.PALETTE['light'],
                             edgecolor=fs.PALETTE['teal'], linewidth=1.2,zorder=2)
            ax.add_patch(rect)
            bid = pid+'-grade'+str(blocknum)
            containers.append((bid,rect))
            text(bid,'grade members',bx+bw/2,bottom+h*.595,
                 'Grade '+str(blocknum)+'\n'+'  '.join(block),size,'semibold')
        text(pid,'priority direction',.5,bottom+h*.595,'>',18,'semibold')
        left, width = .035, .93/6
        mask = []
        for k,pair in enumerate(report['pairs']):
            cx = left+(k+.5)*width
            text(pid,'pair '+pair['pair'],cx,bottom+h*.375,pair['pair'],size,'semibold')
            rect = Rectangle((left+k*width+.006,bottom+h*.075),width-.012,h*.22,
                             facecolor=fs.PALETTE['light'] if pair['disclosed'] else 'white',
                             edgecolor=fs.PALETTE['teal'] if pair['disclosed'] else fs.PALETTE['line'],
                             linewidth=1.4 if pair['disclosed'] else 1,zorder=2)
            ax.add_patch(rect)
            cid=pid+'-'+pair['pair']
            containers.append((cid,rect))
            label=pair['direction'] if pair['disclosed'] else '—'
            text(cid,'reported direction',cx,bottom+h*.185,label,size,
                 'semibold' if pair['disclosed'] else 'normal',
                 fs.PALETTE['teal'] if pair['disclosed'] else fs.PALETTE['muted'])
            mask.append({'pair':pair['pair'],'disclosed':pair['disclosed'],'label':label})
        checks.append({'report':pid,'pair_order':[p['pair'] for p in report['pairs']],
                       'shown_mask':mask,'G':report['G'],'N':report['N'],'M':report['M']})

    fig.canvas.draw()
    renderer=fig.canvas.get_renderer()
    boxes={key:patch.get_window_extent(renderer) for key,patch in containers}
    geometry=[]
    for owner,name,artist in drawn:
        bb=artist.get_window_extent(renderer); bounds=boxes[owner]
        inside=bool(bb.x0>=bounds.x0+1 and bb.x1<=bounds.x1-1 and
                    bb.y0>=bounds.y0+1 and bb.y1<=bounds.y1-1)
        geometry.append({'owner':owner,'label':name,'inside':inside,'font_pt':artist.get_fontsize()})
    # Every piece of text, including the explanatory header/footer, stays inside
    # the canvas; pairwise text non-overlap is checked in display coordinates.
    all_text=list(ax.texts)+list(fig.texts)
    for i,t in enumerate(all_text):
        bb=t.get_window_extent(renderer)
        if not (bb.x0>=1 and bb.y0>=1 and bb.x1<=fig.bbox.width-1 and bb.y1<=fig.bbox.height-1):
            raise RuntimeError('Text outside canvas: '+t.get_text())
        for t2 in all_text[i+1:]:
            if bb.overlaps(t2.get_window_extent(renderer)):
                raise RuntimeError('Overlapping text: '+t.get_text()+' / '+t2.get_text())
    if not all(x['inside'] for x in geometry):
        raise RuntimeError('Container clipping: '+str([x for x in geometry if not x['inside']]))
    return fs.export(fig,STEM,mobile),{'mobile':mobile,'canvas_inches':[4.8,10.2] if mobile else [10,6.8],
                'text_containment':geometry,'all_text_inside_canvas':True,
                'text_pairwise_nonoverlap':True,'reports':checks,
                'mobile_minimum_font_px_at332':14*96/72*332/(4.8*96) if mobile else None}


def generate(overwrite=False):
    paths=[ROOT/'assets/figures'/(STEM+s+'.'+e) for s in ['', '-mobile'] for e in ['svg','pdf','png']]
    if not overwrite and (DEST.exists() or any(p.exists() for p in paths)):
        raise SystemExit('Existing outputs; --overwrite is for an authorized recorded repair.')
    old=json.loads(DEST.read_text()) if DEST.exists() else None
    data=json.loads(DATA.read_text())
    assert data['pair_order']==['AB','AC','AD','BC','BD','CD']
    assert [(r['G'],r['N'],r['M']) for r in data['reports']]==[(2,3,6),(2,4,6)]
    outputs=[]; geometry=[]
    for mobile in [False,True]:
        result,check=render(data,mobile);outputs.extend(result);geometry.append(check)
    assert [o['path'] for o in outputs]==[str(p.relative_to(ROOT)) for p in paths]
    h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    record={'id':'F09a','step':'4.7','status':'rendered',
            'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'author':'JoonHo Lee (jlee296@ua.edu)',
            'command':'python -B assets/reproduction/figures/generators/F09a/generate.py'+(' --overwrite' if overwrite else ''),
            'scope':'Deterministic reporting diagram from the public exact coordinate packet; no risk,latent truth or optimum.',
            'inputs':[{'path':str(p.relative_to(ROOT)),'sha256':h(p)} for p in [DATA,BASE/'figstyle.py',HERE]],
            'outputs':outputs,'geometry_checks':geometry,'actual_image_views':[],
            'execution':{'python':platform.python_version(),'renderer_invocations_total':1 if old is None else old['execution']['renderer_invocations_total']+1,
                         'last_command_invocations':1,'last_command_layout_exports':2,'last_command_asset_exports':6,
                         'coordinate_generation_runs':0,'model_runs':0,'optimizer_runs':0,'canonical_edits':0,'register_edits':0},
            'scientific_boundaries':['Each unordered pair is shown once in the same order for both reports.',
                                     'Smaller grade labels indicate higher reported priority.',
                                     'Shared grades withhold directions and do not assert latent equality.',
                                     'Counts quantify disclosure,not truth,risk or optimality.'],
            'limits':[
                      'Generator reads public coordinate/style/source only; no private contract,registry or evidence input is required.'],
            'required_repairs_remaining':[]}
    if old:record['previous_execution_history']=old.get('previous_execution_history',[])+[{'outputs':old['outputs'],'execution':old['execution'],'actual_image_views':old.get('actual_image_views',[])}]
    DEST.parent.mkdir(parents=True,exist_ok=True);DEST.write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({'id':'F09a','outputs':outputs,'geometry':'PASS'},indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--overwrite',action='store_true')
    generate(parser.parse_args().overwrite)
