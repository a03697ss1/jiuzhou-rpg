from pathlib import Path
import json,html,hashlib,shutil,collections,re
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'V0.7.3_部分項目補完_2026-10-18';OLD=R/'V0.7.3_獨立測試_2026-10-17';W=OLD/'Git測試分支'
read=lambda p:json.loads(p.read_text('utf-8-sig'))
def write(name,data): (O/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),'utf8')
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for chunk in iter(lambda:f.read(8*1024*1024),b''):h.update(chunk)
 return h.hexdigest()
protected=read(O/'施工前保護檔案雜湊.json');checks=[{'path':n,'before':s,'after':sha(R/n),'unchanged':sha(R/n)==s} for n,s in protected.items()]
assert all(r['unchanged'] for r in checks),'Protected formal/published file changed'
write('正式與已發布檔案保護驗證.json',checks)
meta=read(O/'施工狀態與規格.json');art=read(O/'素材圖片檔案驗收.json');display=read(O/'素材圖片實際顯示驗收.json')
offline=read(O/'單檔離線驗收.json');assert offline['pass'],'Standalone offline validation failed'
assert len(art)==69 and all(r['exists'] and r['mode']=='RGBA' and r['alpha'][0]==0 for r in art)
assert display['displayed']==69 and not display['broken'] and not meta['missingImages']
testfiles=['施工測試結果.json','擴充流程測試結果.json','A線與NPC公式測試結果.json','B線與補充定案測試結果.json','本輪正常流程驗收.json','素材正常流程驗收.json','寵物已知公式與阻礙驗收.json']
tests=[];summaries=[]
for name in testfiles:
 d=read(O/name);rows=d['rows'];assert all(r['pass'] for r in rows) and not d.get('errors'),name
 summaries.append({'name':name,'total':len(rows),'passed':len(rows)})
 for row in rows:tests.append({**row,'file':name})
for name in ['r1011-reg-main-results.json','reg-sides-results.json','reg-commissions-results.json','reg-systems-results.json']:
 d=read(P/'regression'/name);rows=d['results'];assert all(r['pass'] for r in rows) and not d.get('errors'),name
 shutil.copy2(P/'regression'/name,O/name);summaries.append({'name':name,'total':len(rows),'passed':len(rows)})
 for row in rows:tests.append({**row,'name':row['id'],'file':name,'evidenceLevel':'既有正常流程回歸'})
e=lambda v:html.escape(str(v));css='body{background:#0b1720;color:#dce8eb;font:16px/1.7 Microsoft JhengHei,sans-serif;margin:0}main{max-width:1280px;margin:auto;padding:24px}h1{color:#ecd18d;font-size:28px}h2{color:#b9d7dd;margin-top:30px}a{color:#99d1f3}table{border-collapse:collapse;width:100%;font-size:14px}td,th{border:1px solid #3b5a68;padding:10px;vertical-align:top}th{background:#213843}tr:nth-child(even){background:#132631}.scroll{overflow:auto}.note{padding:16px;border:1px solid #bf9556;border-radius:8px;background:#302819}.ok{color:#98dbaa}.pending{color:#ffcf8c}nav{display:flex;gap:18px;flex-wrap:wrap;margin:20px 0}img{max-width:100%}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:13px/1.6 Consolas,monospace}button{font:inherit;background:#223b49;color:#dce8eb;border:1px solid #5d7a89;padding:8px;border-radius:6px}details{margin:8px 0}.metrics{display:flex;gap:16px;flex-wrap:wrap}.metrics>div{padding:16px;border:1px solid #45616d;border-radius:8px}'
links=[('閱讀我_先看這裡.html','遊戲與交付'),('逐項施工工程覆蓋表.html','逐項覆蓋表'),('BUG修復與待補清單.html','修復與待補'),('完整測試及驗收報告.html','測試報告'),('素材圖片清單與預覽.html','素材圖片')]
nav='<nav>'+''.join('<a href="'+n+'">'+t+'</a>' for n,t in links)+'</nav>'
warning='<p class="note">V0.7.3・2026-10-18本地獨立測試補完，沿用最新0.7.3測試來源。正式母檔、正式版本及GitHub內容未更新。仍待玩家驗收；新三寵正常取得及完整成長尚未完成。</p>'
def page(name,title,body): (O/name).write_text('<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><title>'+e(title)+'</title><style>'+css+'</style><main><h1>'+e(title)+'</h1>'+nav+body+'</main></html>','utf8')
source=O/'施工來源';source.mkdir(exist_ok=True)
for f in list(P.glob('*.js'))+list(P.glob('*1018*.cjs'))+list(P.glob('*1018*.py'))+[P/'build.py',P/'style.css',P/'baseline.json',P/'side015-original.txt',P/'side016-original.txt',P/'side1018-dialogues.json']:
 shutil.copy2(f,source/f.name)
preview=(P/'preview.html').read_text('utf8').replace('/github-release/assets/','assets/').replace('/新增美術_2026-10-16/','new-assets/').replace('/素材美術_2026-10-18/','material-assets/')
(W/'index.html').write_text(preview,'utf8');(W/'material-assets').mkdir(exist_ok=True)
for f in (R/'素材美術_2026-10-18').glob('*.png'):shutil.copy2(f,W/'material-assets'/f.name)
for f in list(P.glob('*.js'))+[P/'build.py']:
 target=W/'test-source/v073'/f.name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,target)
origin=read(OLD/'逐項施工工程覆蓋表.json');sources={'L18':'status1018.js','L19':'pet1018.js','L20':'pet1018.js','L23':'side1018.js','L31':'material1018.js','L33':'material1018.js','L34':'pets.js'}
coverage=[]
for old in origin:
 row={**old};key=row['id'];state=meta['coverage'][key];row.update(implementation=state['state'],reason=state['reason'],source=sources.get(key,row.get('source','core.js')),tests=[t['name'] for t in tests if key in str(t.get('id',''))],acceptance='待玩家明確驗收');coverage.append(row)
write('逐項施工工程覆蓋表.json',coverage)
counts=collections.Counter(r['implementation'] for r in coverage)
table='<div class="scroll"><table><thead><tr><th>項目／程式位置</th><th>實裝狀態</th><th>本輪結果與剩餘阻礙</th><th>測試證據</th></tr></thead><tbody>'
for row in coverage:
 table+='<tr data-status="'+e(row['implementation'])+'"><td><b>'+e(row['id']+' '+row['item'])+'</b><p><a href="施工來源/'+e(row['source'])+'">'+e(row['source'])+'</a></p></td><td>'+e(row['implementation'])+'</td><td>'+e(row['reason'])+'</td><td>'+''.join('<p>✓ '+e(t)+'</p>' for t in row['tests'])+'<p>待玩家驗收</p></td></tr>'
table+='</tbody></table></div>'
page('逐項施工工程覆蓋表.html','逐項施工工程覆蓋表',warning+'<p>'+e(dict(counts))+'。L33素材69張完成；裝備／丹藥／禮物／任務物品依原工作檔保留後續獨立圖示目標。</p><button onclick="document.querySelectorAll(\'tr[data-status]\').forEach(r=>r.hidden=r.dataset.status!==\'部分實裝\')">只看部分實裝</button> <button onclick="document.querySelectorAll(\'tr[data-status]\').forEach(r=>r.hidden=false)">顯示全部</button>'+table)
fixes=[('支線原稿','015接入88節點、016接入212節點。兩日門檻、036B、B線專屬、10心收禮與一次性報酬均驗證。'),('對話續讀','存檔保存交談位置；舊摘要已領獎的測試存檔可補讀全文，不再領獎。'),('遺漏素材','68項原目錄加回正式合成產物龜甲片。原17項未分類素材仍可查；泛用委託維持51項。'),('來源反查','新增天穹浮島掉落、晶礦元素分池、深窟採集、商店、舊任務、委託與正式素材箱來源；兩項無原生來源明示待補。'),('素材共用圖片','69張獨立透明PNG接入圖鑑、背包、工坊、商店及委託；保留現有妖物／NPC／地圖圖片。'),('圖鑑主素材圖','避免配方來源圖片插到主素材圖之前。'),('新寵物操作','沿用升星3／5／7／15／20獸魂晶成本與正式倍率；補齊新三寵核心顯示、合法技能家族及已定MP／CD選招畫面。'),('L18驗證','正式長右戰鬥中洪水在極高效果抵抗下仍附加潮濕；圖示懸停名稱、雷傷單次消耗通過。其餘七種未指定來源，不修改368庫。')]
write('BUG修復與待補清單.json',{'fixed':[{'item':a,'detail':b} for a,b in fixes],'pending':meta['pending'],'materialNativeMissing':[r['name'] for r in meta['sources'] if r['pending']],'remainingCodexArtCount':len(meta['remainingCodexArt'])})
page('BUG修復與待補清單.html','BUG修復與待補清單',warning+'<h2>本輪修復與補完</h2><ul>'+''.join('<li><b>'+e(a)+'</b>：'+e(b)+'</li>' for a,b in fixes)+'</ul><h2>仍待補</h2><ul>'+''.join('<li><b>'+e(r['id'])+'</b>：'+e(r['reason'])+'</li>' for r in meta['pending'])+'</ul><p><a href="新三寵已知八核與49項缺列.json">新三寵逐列八核缺口</a> · <a href="新寵物原稿交叉查核.json">原稿查核紀錄</a> · <a href="圖鑑後續圖片資源命名與缺圖清單.json">其餘圖鑑圖片命名與缺圖目標</a></p>')
testbody=warning+'<p>總計'+str(len(tests))+'項檢查通過。寵物公式檢查與正常遊戲流程分別列明；新三寵正常孵化、完整成長及完整10心任務尚未通過，不以隔離數值測試替代。</p><table><tr><th>測試組</th><th>通過</th></tr>'+''.join('<tr><td><a href="'+s['name']+'">'+e(s['name'])+'</a></td><td>'+str(s['passed'])+'/'+str(s['total'])+'</td></tr>' for s in summaries)+'</table><h2>素材圖片與來源</h2><p>69張獨立RGBA PNG，透明底、無破圖；'+str(sum(len(r['sources']) for r in meta['sources']))+'筆來源映射。獸角及狐毛目前只確認素材箱來源，不新增掉落。五個介面共用同一圖片表。</p><p><a href="素材圖片檔案驗收.json">尺寸／透明度／雜湊</a> · <a href="素材圖片實際顯示驗收.json">瀏覽器顯示結果</a> · <a href="全部素材來源映射.json">全部來源映射</a></p><h2>正常流程畫面</h2>'+''.join('<details><summary>'+e(n)+'</summary><img src="'+e(n)+'"></details>' for n in ['支線015完成.png','支線016與十心收禮.png','洪水正常長右戰鬥_潮濕圖示.png','委託材料共用圖片.png','素材圖片驗收_1.png','素材圖片驗收_2.png','素材圖片驗收_3.png'])+'<h2>逐案證據</h2>'
for t in tests:testbody+='<details><summary>✓ '+e(t['name'])+' · '+e(t.get('evidenceLevel','本地功能／流程檢查'))+'</summary><pre>'+e(json.dumps(t.get('detail',{}),ensure_ascii=False,indent=2))+'</pre></details>'
testbody+='<h2>正式／已發布內容保護</h2><p>5個受保護檔案雜湊均與施工前一致；本輪未執行推送或發布。</p><a href="正式與已發布檔案保護驗證.json">檔案雜湊證據</a>'
testbody+='<h2>單檔離線</h2><p>以file://開啟最新獨立測試HTML，阻擋HTTP／HTTPS請求，69張素材圖均由內嵌PNG載入，無外部請求與程式錯誤。</p><p><a href="單檔離線驗收.json">單檔離線驗收資料</a></p><img src="單檔離線_素材圖鑑.png">'
page('完整測試及驗收報告.html','完整測試及驗收報告',testbody)
page('閱讀我_先看這裡.html','V0.7.3 本輪補完交付',warning+'<h2>開啟遊戲</h2><p><a href="九州修仙錄_V0.7.3_獨立測試版.html">最新可遊玩的獨立測試HTML</a>（單檔，內嵌原圖與本輪素材圖）。測試存檔仍使用原0.7.3獨立名稱空間。</p><h2>已補完</h2><ul><li>L23：兩條完整支線原稿、存檔續讀、前置及10心收禮。</li><li>L31：全部69項素材來源反查，泛用委託仍51項。</li><li>L33素材階段：69張獨立透明PNG，各介面共用。</li><li>L18：八種狀態在遊戲內可查，洪水正常戰鬥流程已驗。</li></ul><h2>未完成</h2><p>L19／L20／L34：新三寵起始及部分連續成長八核仍缺49個練氣／築基層位。已知公式、技能與操作補完，正常孵化保持不扣蛋保護。其餘圖鑑圖片目標依原工作檔分期保留。</p><p>所有狀態與證據見上方覆蓋表及驗收報告。素材原圖與完整提示詞保存在工作區「素材美術_2026-10-18」。</p>')
shutil.copy2(R/'素材美術_2026-10-18/生成清單與提示詞.json',O/'素材圖片生成提示詞與路徑.json')
write('本輪交付清單.json',{'version':'0.7.3','supplement':'2026-10-18','published':False,'formalUpdated':False,'basis':'目前最新test/v0.7.3-20261017測試來源，增量模組補完','coverage':dict(counts),'tests':summaries,'passedChecks':len(tests),'materials':len(art),'sourceRows':sum(len(r['sources']) for r in meta['sources']),'genericCommissionMaterials':len(meta['eligible']),'petMissingRows':sum(len(r['missing']) for r in meta['petAudit']),'protected':checks,'standalone':{'file':'九州修仙錄_V0.7.3_獨立測試版.html','sha256':sha(O/'九州修仙錄_V0.7.3_獨立測試版.html')}})
print('Packaged local supplement:',dict(counts),'checks',len(tests),'materials',len(art))
