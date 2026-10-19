from pathlib import Path
import importlib.util,json,shutil
P=Path(__file__).resolve().parent;R=P.parents[1];sp=importlib.util.spec_from_file_location('pub',P/'publish-preview.py');pub=importlib.util.module_from_spec(sp);sp.loader.exec_module(pub);sp=importlib.util.spec_from_file_location('rel',P/'release-official073.py');rel=importlib.util.module_from_spec(sp);sp.loader.exec_module(rel);T=pub.O/'Git測試分支';D=pub.DEST;name='wave-vitals1019';O=R/'V0.7.3_材料容量與主線置頂_2026-10-19'
qa=json.loads((O/'萬妖陣醫館同步與結算驗收.json').read_text('utf8'));assert len(qa['rows'])==3 and all(r['pass'] for r in qa['rows']) and not qa['errors']
for f in [T/'index.html',D/'index.html',R/'九州修仙錄_正式母檔_0.7.3.html']:
 s=f.read_text('utf8');assert 'id="jz073-'+name+'"' not in s;f.write_text(s+'\n<script id="jz073-'+name+'">'+(P/(name+'.js')).read_text('utf8')+'</script>','utf8')
s=rel.official((D/'index.html').read_text('utf8'));(pub.W/'index.html').write_text(s,'utf8');(T/'official073/index.html').write_text(s,'utf8')
f=P/'build.py';s=f.read_text('utf8');s=s.replace(' return text+code'," code+='<script id=\"jz073-"+name+"\">'+(P/'"+name+".js').read_text('utf8')+'</script>\\n'\n return text+code");f.write_text(s,'utf8')
for folder in [T/'test-source/v073',D/'test-source/v073']:
 for n in [name+'.js',name+'-test.cjs','package-wave-vitals1019.py','build.py']:shutil.copy2(P/n,folder/n)
f=pub.W/'定案規則_0.7.3.json';rules=json.loads(f.read_text('utf8'));rules['petAutoBattle']['waveVitals']='儲存退出同步寵物傷勢；返回採用醫館治療後氣血靈力，結算後參戰寵物免費補滿';rules['sourceModules'].append({'name':name+'.js','sha256':pub.digest(P/(name+'.js'))});f.write_text(json.dumps(rules,ensure_ascii=False,indent=2),'utf8');shutil.copy2(f,T/'official073/定案規則_0.7.3.json')
f=R/'最新定案母檔_0.7.3.json';master=json.loads(f.read_text('utf8'));master['official073']=rules;f.write_text(json.dumps(master,ensure_ascii=False,indent=2),'utf8')
f=D/'10-19J_材料容量與主線置頂驗收.json';combined=json.loads(f.read_text('utf8'));combined['rows']+=qa['rows'];f.write_text(json.dumps(combined,ensure_ascii=False,indent=2),'utf8')
for f in [D/'10-19J_材料容量與主線置頂.html',O/'修正與驗收.html']:
 s=f.read_text('utf8').replace('26項測試通過','29項測試通過').replace('<h2>29項測試通過</h2>','<p>萬妖陣儲存離場與醫館治療同步，返回不再被舊數值覆蓋；退出結算後免費補滿參戰寵物氣血與靈力。</p><h2>29項測試通過</h2>');s=s.replace('</ul>',''.join('<li>'+r['name']+'</li>' for r in qa['rows'])+'</ul>');f.write_text(s,'utf8')
f=P/'capacity-sidebar-state.json';state=json.loads(f.read_text('utf8'));state['tests']=29;state['siteBytes']=sum(f.stat().st_size for f in pub.W.rglob('*') if f.is_file() and '.git' not in f.parts);assert state['siteBytes']<1073741824;f.write_text(json.dumps(state,ensure_ascii=False,indent=2),'utf8');print(json.dumps(state,ensure_ascii=False))
