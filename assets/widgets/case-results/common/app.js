(function(root){'use strict';const model=root.PostrankSavedModel,data=root.PostrankSavedData,doc=root.document;if(!model||!data||!doc)return;
const byId=id=>doc.getElementById(id);const cell=(tag,text)=>{const el=doc.createElement(tag);el.textContent=String(text);return el;};
const controller=root.PostrankWidget.init({defaults:data.unitHighlight?{scenario:model.defaults.scenario,unit:model.defaults.unit}:{scenario:model.defaults.scenario},render(values){
 const view=model.readout(values.scenario,values.unit||'none');byId('scenario-title').textContent=view.label;
 const list=byId('metrics');list.replaceChildren();for(const m of view.metrics){const item=doc.createElement('div');item.className='metric';item.append(cell('span',m.label),cell('strong',m.display));if(m.detail)item.append(cell('small',m.detail));list.append(item);}
 const notes=byId('scenario-notes');notes.replaceChildren();for(const note of view.notes)notes.append(cell('p',note));
 const table=byId('unit-table');if(table){const options=byId('unit');const current=view.unit?view.unit.id:'none';const signature=view.rows.map(x=>x.id).join('|');if(data.unitControl!=='lookup'&&options.dataset.rows!==signature){options.replaceChildren(new Option('No highlight','none'));for(const row of view.rows)options.append(new Option(row.label,row.id));options.dataset.rows=signature;}if(data.unitControl!=='lookup')options.value=current;
  byId('unit-readout').textContent=view.unit?view.unit.label+': '+view.columns.map(c=>c.label+' '+view.unit[c.key]).join('; ')+'.':view.unitStatus;
  table.querySelector('caption').textContent=view.rowCaption;const head=table.querySelector('thead');head.replaceChildren();const tr=doc.createElement('tr');tr.append(cell('th',data.unitLabel||'Unit'));for(const col of view.columns)tr.append(cell('th',col.label));for(const th of tr.children)th.scope='col';head.append(tr);
  const body=table.querySelector('tbody');body.replaceChildren();for(const row of (data.rowDisplay==='selected'?(view.unit?[view.unit]:[]):view.rows)){const line=doc.createElement('tr');const th=cell('th',row.label);th.scope='row';line.append(th);for(const col of view.columns)line.append(cell('td',row[col.key]));if(view.unit&&row.id===view.unit.id){line.className='selected';const marker=cell('span',' — highlighted');marker.className='highlight-label';th.append(marker);}body.append(line);}
 }
 return view.label+'. '+(view.unit?view.unit.label+' highlighted.':'Stored results displayed.')+' No model fitting or optimization is performed.';
}});
if(data.unitControl==='lookup')byId('unit').addEventListener('input',()=>controller.update());
})(typeof window==='undefined'?globalThis:window);
