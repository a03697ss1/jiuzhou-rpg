from pathlib import Path
import importlib.util,re,shutil,json,ast,html,hashlib,datetime
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'V0.7.3_正式發布_2026-10-19';BUILD='20261019-official073-2'
spec=importlib.util.spec_from_file_location('pub',P/'publish-preview.py');pub=importlib.util.module_from_spec(spec);spec.loader.exec_module(pub)
spec=importlib.util.spec_from_file_location('rel',P/'release-official073.py');rel=importlib.util.module_from_spec(spec);spec.loader.exec_module(rel)
T=pub.O/'Git測試分支';D=pub.DEST
cases=[]
for path in [O/'修正8項驗收.json',R/'V0.7.3_24項修正_2026-10-19/配方成長存讀檔驗收.json',R/'V0.7.3_歷練與夥伴背景_2026-10-19/郵箱正常取得流程驗收.json']:
 d=json.loads(path.read_text('utf8'));assert not d['errors'] and all(r['pass'] for r in d['rows']),path;cases+=d['rows'];shutil.copy2(path,D/('10-19G_'+path.name))
assert len(cases)==20
# Remove only the now-unwanted public playable archives; local historical sources stay.
target=(pub.W/'versions').resolve();assert target.parent==pub.W.resolve() and target.name=='versions'
if target.exists():shutil.rmtree(target)
for name in ['README.md','preview/v0.7.3/閱讀我_先看這裡.html','preview/v0.7.3/10-19F_正式發布與驗收報告.html']:
 f=pub.W/name;s=f.read_text('utf8');s=re.sub(r'<a\b[^>]*href="[^"\n]*versions/[^"\n]*"[^>]*>.*?</a>', '歷代更新紀錄請見遊戲內「更新內容」',s,flags=re.S)
 s=re.sub(r'^歷史版本：https://[^\n]+\n','',s,flags=re.M);s=s.replace('0.7.0、0.7.1、0.7.2原始發布程式與規則保留，各有獨立存檔副本入口。','0.7.0、0.7.1、0.7.2的更新內容保留於遊戲內；已移除歷史遊玩入口。');f.write_text(s,'utf8')
f=pub.W/'定案規則_0.7.3.json';rules=json.loads(f.read_text('utf8'));rules.pop('retainedVersions',None);rules['inventory']['initialSlots'].pop('永久特殊',None);rules['inventory']['unlimited']=['永久特殊','紀念品','禮物','任務'];rules['mail']['individualExpiry']=True;rules['mail']['expiryDisplay']='每封信各自的遊戲年月日時間及剩餘日／小時／分鐘，讀取不重設';rules['historicalChangelog']=['0.7.0','0.7.1','0.7.2'];rules['historicalPlayableEntrances']=False;rules['build']=BUILD;rules['sourceModules'].append({'name':'revision8-1019.js','sha256':pub.digest(P/'revision8-1019.js')});f.write_text(json.dumps(rules,ensure_ascii=False,indent=2),'utf8');(R/'最新定案母檔_0.7.3.json').write_text(json.dumps({'inherits':'最新定案母檔_0.7.2.json','official073':rules},ensure_ascii=False,indent=2),'utf8');shutil.copy2(f,T/'official073/定案規則_0.7.3.json')
local=(P/'preview.html').read_text('utf8')
for prefix in ['/github-release/assets/','/新增美術_2026-10-16/','/素材美術_2026-10-18/','/物品美術_2026-10-18/','/人物全身_2026-10-18/','/物品獨立美術_2026-10-18/','/物品修正美術_2026-10-19/','/長右血條正式美術_2026-10-19/','/修正24美術_2026-10-19/','/郵箱背包美術_2026-10-19/']:local=local.replace(prefix,'.'+prefix)
local=rel.official(local).replace('<base href="preview/v0.7.3/">','');local+='<script>window.JZ073_BUILD_ID="'+BUILD+'";</script>';(R/'九州修仙錄_正式母檔_0.7.3.html').write_text(local,'utf8')
old=(P/'baseline-scripts/139-jz1011b-ui.js').read_text('utf8');history=ast.literal_eval(old.split('const sections=')[1].split(';showModal')[0])
body='<h1>0.7.3 背包、郵箱與圖鑑修正</h1><p><a href="../../../?build='+BUILD+'">開始遊玩</a></p><h2>改動</h2><p>永久特殊不限格數；裝備比較及卸下按鈕移入對應格子；背包字體加大；九類圖鑑統一格子與圖片尺寸。黃色框的圖鑑置左，移除正式版文字及歷史版本遊玩入口。</p><h2>BUG修復</h2><p>每封信顯示獨立到期年月日、時間與倒數，存讀檔不重設；重要道具未領取仍保留。手動存檔按下立即刷新卡片與儲存時間。素材顯示正式階級。</p><h2>逐項測試</h2><p>20項本機檢查通過，沒有未處理錯誤。含11項本輪實際介面檢查、6項成長／配方／存檔回歸，以及3項正常戰利品／煉製／收禮溢出流程。</p><table><tr><th>檢查</th><th>結果</th></tr>'+''.join('<tr><td>'+html.escape(r['name'])+'</td><td>通過</td></tr>' for r in cases)+'</table><p><a href="test-source/v073/revision8-1019.js">對應程式</a> · <a href="10-19G_修正8項驗收.json">完整驗收資料</a></p><h2>歷代更新紀錄</h2>'
for v,groups in history:
 body+='<h3>'+v+'</h3>'
 for kind,texts in groups:body+='<h4>'+kind+'</h4><ul>'+''.join('<li>'+html.escape(t)+'</li>' for t in dict.fromkeys(texts))+'</ul>'
 if v.startswith('V0.7.0'):body+='<p>原紀錄未另列改動與BUG修復項目，未補寫。</p>'
report='<!doctype html><meta charset="utf-8"><title>0.7.3 修正與驗收</title><style>body{max-width:1050px;margin:30px auto;padding:20px;background:#09151f;color:#dae6ee;font:17px/1.8 sans-serif}a{color:#efcf82}table{border-collapse:collapse;width:100%}td,th{border:1px solid #456073;padding:10px;text-align:left}</style>'+body
(D/'10-19G_修正與驗收報告.html').write_text(report,'utf8');(O/'10-19G_修正與驗收報告.html').write_text(report,'utf8')
coverage={'build':BUILD,'completed':8,'pending':0,'module':'revision8-1019.js','tests':cases,'historicalNote':'保留各版更新紀錄；移除歷史版本遊玩入口。0.7.0未記載的修復不編造。'};(D/'10-19G_施工覆蓋表.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2),'utf8')
for folder in [D/'test-source/v073',T/'test-source/v073']:
 for name in ['revision8-1019.js','revision8-test.cjs','package8.py','finalize8.py','build.py']:shutil.copy2(P/name,folder/name)
for name in ['修正8_背包.png','修正8_圖鑑.png']:
 # Keep full resolution screenshots locally; avoid needless public asset duplication.
 assert (O/name).exists()
(pub.W/'README.md').write_text('# 九州修仙錄 0.7.3\n\n正式遊玩：https://a03697ss1.github.io/jiuzhou-rpg/\n\n本輪修正與20項驗收：'+pub.URL+'10-19G_修正與驗收報告.html\n\n歷代更新內容保留於遊戲內「更新內容」，涵蓋0.7.0、0.7.1、0.7.2、0.7.3；不提供歷史版本遊玩入口。\n\n永久特殊不限格數，郵件各自到期，背包格內裝備比較，統一圖鑑格子，手動存檔即時更新，素材顯示階級。\n\n存檔沿用0.7.3先前進度，保留原版紀錄副本讀取。音樂暫不實裝。\n','utf8')
state={'build':BUILD,'url':'https://a03697ss1.github.io/jiuzhou-rpg/?build='+BUILD,'base':pub.git(pub.W,'rev-parse','HEAD'),'tests':20,'siteBytes':sum(f.stat().st_size for f in pub.W.rglob('*') if f.is_file() and '.git' not in f.parts),'oldRules':{n:pub.git(pub.W,'rev-parse','HEAD:'+n) for n in ['定案規則_0.7.0.json','定案規則_0.7.1.json','定案規則_0.7.2.json']}}
assert state['siteBytes']<1073741824
# Prove the incremental update retained all previously published script bodies.
old=pub.git(pub.W,'show','HEAD:preview/v0.7.3/index.html');new=(D/'index.html').read_text('utf8');scripts=lambda s:{m[1]:m[2] for m in re.finditer(r'<script id="([^"]+)">(.*?)</script>',s,re.S)};a,b=scripts(old),scripts(new);assert all(b[k]==v for k,v in a.items()),'Existing modules changed'
(P/'revision8-state.json').write_text(json.dumps(state,ensure_ascii=False,indent=2),'utf8');print(json.dumps(state,ensure_ascii=False))
