from pathlib import Path
import json,shutil,hashlib,importlib.util
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'V0.7.3_正式發布_2026-10-19';Q=R/'V0.7.3_歷練與夥伴背景_2026-10-19';W=R/'V0.7.3_獨立測試_2026-10-17/GitHub測試發布';D=W/'preview/v0.7.3';T=R/'V0.7.3_獨立測試_2026-10-17/Git測試分支'
state=json.loads((P/'official073-release-state.json').read_text('utf8'))
sources=[Q/n for n in ['歷練與夥伴背景驗收.json','戰鬥歷練驗收.json','背包郵箱固定格驗收.json','郵箱正常取得流程驗收.json']]+[O/'正式入口與舊版保留驗收.json']
new=0
for f in sources:
 d=json.loads(f.read_text('utf8'));assert not d['errors'] and all(r['pass'] for r in d['rows']),f;new+=len(d['rows']);shutil.copy2(f,D/('10-19F_'+f.name))
 if f.parent!=O:shutil.copy2(f,O/f.name)
offline=json.loads((O/'本機正式HTML驗收.json').read_text('utf8'));assert offline['pass'];new+=1;shutil.copy2(O/'本機正式HTML驗收.json',D/'10-19F_本機正式HTML驗收.json')
regressions=[('V0.7.3_24項修正_2026-10-19','介面與物品驗收.json'),('V0.7.3_24項修正_2026-10-19','戰鬥與嚴重BUG驗收.json'),('V0.7.3_24項修正_2026-10-19','問道18裝備特殊效果驗收.json'),('V0.7.3_24項修正_2026-10-19','配方成長存讀檔驗收.json'),('V0.7.3_物品與收禮修正_2026-10-19','連續野外戰鬥診斷.json'),('V0.7.3_物品與收禮修正_2026-10-19','主線連續戰鬥退出驗收.json'),('V0.7.3_裝備圖片修正_2026-10-19','裝備圖片實際驗收.json')]
reg=0
for folder,n in regressions:
 f=R/folder/n;d=json.loads(f.read_text('utf8'));assert not d['errors'] and all(r['pass'] for r in d['rows']),n;reg+=len(d['rows']);shutil.copy2(f,O/('回歸_'+n));shutil.copy2(f,D/('10-19F_回歸_'+n))
assert new==49 and reg==81
for n in ['先驅者感謝信與靈幣圖片','材料背包固定格與擴充','幫助切頁保留捲動']:
 shutil.copy2(Q/(n+'.webp'),D/('10-19F_'+n+'.webp'));shutil.copy2(Q/(n+'.webp'),O/(n+'.webp'))
f=D/'10-19F_正式發布與驗收報告.html';s=f.read_text('utf8').replace('../../../?build=','../../?build=').replace('../../../versions/','../../versions/').replace('本次新增40項驗收通過；','本次49項新增與發布驗收、81項回歸檢查，共130項通過；')
s+='<h2>正式入口、本機與回歸證據</h2><p><a href="10-19F_正式入口與舊版保留驗收.json">正式入口、存檔銜接與舊版8項</a> · <a href="10-19F_本機正式HTML驗收.json">本機HTML驗收</a></p><ul>'+''.join('<li><a href="10-19F_回歸_'+n+'">'+n.replace('.json','')+'</a></li>' for _,n in regressions)+'</ul>'
f.write_text(s,'utf8');(O/'正式發布與驗收報告.html').write_text(s.replace('../../?build=',state['url'].split('?')[0]+'?build=').replace('../../versions/',state['url'].split('?')[0]+'versions/').replace('10-19F_','').replace('inventory-assets/','../郵箱背包美術_2026-10-19/'),'utf8')
f=D/'閱讀我_先看這裡.html';s=f.read_text('utf8').replace('href="../../../"','href="../../"').replace('href="../../../versions/"','href="../../versions/"');f.write_text(s,'utf8')
f=D/'本輪交付清單.json';d=json.loads(f.read_text('utf8'));d.update(build=state['build'],version='0.7.3',phase='正式版',masterPromoted=True,formalUpdated=True,latestReport='10-19F_正式發布與驗收報告.html',newChecks=new,regressionChecks=reg)
if 'revision24' in d:d['revision24']=json.loads((D/'10-19E_逐項施工覆蓋表.json').read_text('utf8'))
f.write_text(json.dumps(d,ensure_ascii=False,indent=2),'utf8')
for f in [D/'10-19F_逐項施工覆蓋表.json',O/'逐項施工覆蓋表.json']:
 d=json.loads(f.read_text('utf8'));d.update(newChecks=new,regressionChecks=reg,totalChecks=new+reg);f.write_text(json.dumps(d,ensure_ascii=False,indent=2),'utf8')
for name in ['official073-test.cjs','finalize-official073.py']:
 for folder in [T/'test-source/v073',D/'test-source/v073',O/'施工來源']:shutil.copy2(P/name,folder/name)
archive=T/'official073/驗收';archive.mkdir(exist_ok=True)
for f in Q.iterdir():
 if f.is_file():shutil.copy2(f,archive/f.name)
for f in O.glob('*.json'):shutil.copy2(f,archive/f.name)
for name,old in json.loads((P/'baseline.json').read_text('utf8'))['protected'].items():assert hashlib.sha256((R/name).read_bytes()).hexdigest()==old['sha256'],name
state.update(newTests=new,regressionTests=reg,totalTests=new+reg,siteBytes=sum(f.stat().st_size for f in W.rglob('*') if f.is_file() and '.git' not in f.parts));assert state['siteBytes']<1073741824;assert state['rootSha256']==hashlib.sha256((W/'index.html').read_bytes()).hexdigest()
(P/'official073-release-state.json').write_text(json.dumps(state,ensure_ascii=False,indent=2),'utf8');print(json.dumps({'checks':new+reg,'new':new,'regression':reg,'siteBytes':state['siteBytes']},ensure_ascii=False))
