from pathlib import Path
import importlib.util,re,shutil,json,html
P=Path(__file__).resolve().parent;R=P.parents[1];BUILD='20261019-official073-5';sp=importlib.util.spec_from_file_location('pub',P/'publish-preview.py');pub=importlib.util.module_from_spec(sp);sp.loader.exec_module(pub);sp=importlib.util.spec_from_file_location('rel',P/'release-official073.py');rel=importlib.util.module_from_spec(sp);sp.loader.exec_module(rel);T=pub.O/'Git測試分支';D=pub.DEST;names=['town-clinic1019','risk-tail1019','random-book1019','pet-battle1019','wendao-auto1019'];O=R/'V0.7.3_材料容量與主線置頂_2026-10-19'
qas=[json.loads((O/f).read_text('utf8')) for f in ['驗收.json','醫館尾巴合成寵物驗收.json','問道自動與64點驗收.json']];rows=sum([q['rows'] for q in qas],[]);assert len(rows)==26 and all(r['pass'] for r in rows) and not any(q['errors'] for q in qas)
for folder in [T,D]:
 f=folder/'index.html';s=f.read_text('utf8')
 for name in names:
  assert 'id="jz073-'+name+'"' not in s;s+='\n<script id="jz073-'+name+'">'+(P/(name+'.js')).read_text('utf8')+'</script>';shutil.copy2(P/(name+'.js'),folder/'test-source/v073'/(name+'.js'))
 f.write_text(s,'utf8')
s=rel.official((D/'index.html').read_text('utf8'));(pub.W/'index.html').write_text(s,'utf8');(T/'official073/index.html').write_text(s,'utf8')
f=P/'build.py';s=f.read_text('utf8')
for name in names:s=s.replace(' return text+code'," code+='<script id=\"jz073-"+name+"\">'+(P/'"+name+".js').read_text('utf8')+'</script>\\n'\n return text+code")
f.write_text(s,'utf8');f=R/'九州修仙錄_正式母檔_0.7.3.html';s=f.read_text('utf8')
for name in names:
 assert 'id="jz073-'+name+'"' not in s;s+='\n<script id="jz073-'+name+'">'+(P/(name+'.js')).read_text('utf8')+'</script>'
f.write_text(s,'utf8')
f=pub.W/'定案規則_0.7.3.json';rules=json.loads(f.read_text('utf8'))
rules['townClinics']={'towns':['青陽鎮','天海港','碧潮鎮','東嶺鎮'],'service':'沿用主城醫館治療、異常、病房與費用；沈玄川劇情病人留主城'}
rules['highRiskTail']='高危種及高危種（特）裝飾尾巴置於戰位框外，保留角與叉'
rules['randomBookRecipe']={'output':'［特殊］隨機功法書','ingredients':{'功法殘卷':10},'count':'跨背包分頁累加實際持有數','excluded':'獸技殘頁'}
rules['petAutoBattle']={'waveEntry':'沿用進場自動設定','recovery':'夥伴／寵物共用開關、門檻、藥水優先與輔助目標','numberDisplay':'戰位氣血與靈力顯示整數，實際值保留'}
rules['wendaoUpdate1019']={'crossBasePoints':64,'streakBonus':'沿用連勝加成，最高+5','entryAuto':'逐步挑戰、境界相符、跨境界三模式遵守進場自動設定','restrictions':'跨境與同境禁物品、戰前效果與逃跑不變'}
for name in names:rules['sourceModules'].append({'name':name+'.js','sha256':pub.digest(P/(name+'.js'))})
f.write_text(json.dumps(rules,ensure_ascii=False,indent=2),'utf8');shutil.copy2(f,T/'official073/定案規則_0.7.3.json')
f=R/'最新定案母檔_0.7.3.json';master=json.loads(f.read_text('utf8'));master['official073']=rules;f.write_text(json.dumps(master,ensure_ascii=False,indent=2),'utf8')
qa={'build':BUILD,'rows':rows,'errors':[]};(D/'10-19J_材料容量與主線置頂驗收.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),'utf8')
report='<!doctype html><meta charset="utf-8"><title>0.7.3本輪修正與驗收</title><style>body{max-width:1000px;margin:40px auto;padding:20px;background:#0b1924;color:#e1e9ed;font:18px/1.8 sans-serif}a{color:#efcd86}</style><h1>0.7.3本輪修正</h1><h2>新增</h2><p>四個東州城鎮新增醫館，沿用主城的服務與費用。自動恢復設定新增寵物，與夥伴共用門檻、優先順序與輔助目標。</p><h2>改動</h2><p>材料初始100格，舊角色原容量加50格一次，保留擴充；郵箱舊附件可領回。跨境界戰基礎勝利獎勵64問道點數，保留原有連勝加成。</p><h2>BUG修復</h2><p>主線未接取或未釘選仍固定左側置頂；高危種裝飾尾巴移到框外；合成功法書正確計入特殊分頁殘卷；萬妖陣與問道檯遵守進場自動設定；寵物氣血靈力過長小數改為整數顯示，保留實際數值。</p><h2>26項測試通過</h2><ul>'+''.join('<li>'+html.escape(r['name'])+'</li>' for r in rows)+'</ul><p><a href="../../../?build='+BUILD+'">開啟最新版</a> · <a href="10-19J_材料容量與主線置頂驗收.json">完整驗收</a></p>'
(D/'10-19J_材料容量與主線置頂.html').write_text(report,'utf8');(O/'修正與驗收.html').write_text(report,'utf8')
for folder in [T/'test-source/v073',D/'test-source/v073']:
 for name in ['package-batch5.py','build.py','extras-batch5-test.cjs','wendao-auto1019-test.cjs']:shutil.copy2(P/name,folder/name)
old=pub.git(pub.W,'show','HEAD:preview/v0.7.3/index.html');new=(D/'index.html').read_text('utf8');scripts=lambda s:{m[1]:m[2] for m in re.finditer(r'<script id="([^"]+)">(.*?)</script>',s,re.S)};a,b=scripts(old),scripts(new);assert all(b[k]==v for k,v in a.items())
f=P/'capacity-sidebar-state.json';state=json.loads(f.read_text('utf8'));state['tests']=26;state['siteBytes']=sum(f.stat().st_size for f in pub.W.rglob('*') if f.is_file() and '.git' not in f.parts);assert state['siteBytes']<1073741824;f.write_text(json.dumps(state,ensure_ascii=False,indent=2),'utf8');print(json.dumps(state,ensure_ascii=False))
