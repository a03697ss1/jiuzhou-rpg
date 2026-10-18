from pathlib import Path
import json,shutil,html,collections,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'V0.7.3_新三寵補完_2026-10-18';PREV=R/'V0.7.3_部分項目補完_2026-10-18';W=R/'V0.7.3_獨立測試_2026-10-17/Git測試分支'
read=lambda p:json.loads(p.read_text('utf8'))
meta=read(O/'施工狀態與規格.json');e=lambda v:html.escape(str(v))
for f in PREV.iterdir():
 if f.is_file() and f.suffix in ['.json','.png'] and not (O/f.name).exists():shutil.copy2(f,O/f.name)
for f in P.glob('*.js'):
 (O/'施工來源').mkdir(exist_ok=True);shutil.copy2(f,O/'施工來源'/f.name)
for f in [P/'build.py',P/'pet-complete1018.cjs',P/'pet-heart-events1018.js']:
 shutil.copy2(f,O/'施工來源'/f.name)
coverage=read(PREV/'逐項施工工程覆蓋表.json')
for row in coverage:
 state=meta['coverage'][row['id']];row.update(implementation=state['state'],reason=state['reason'],acceptance='待玩家明確驗收')
 if row['id'] in ['L19','L20','L34']:row.update(source='pet1018.js',tests=['新三寵正常孵化與成長驗收.json'])
(O/'逐項施工工程覆蓋表.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2),'utf8')
css='body{background:#0b1720;color:#dce8eb;font:16px/1.7 Microsoft JhengHei,sans-serif;margin:0}main{max-width:1280px;margin:auto;padding:24px}h1{color:#ecd18d}a{color:#99d1f3}td,th{border:1px solid #3b5a68;padding:10px;text-align:left;vertical-align:top}table{border-collapse:collapse;width:100%}nav{display:flex;gap:18px;flex-wrap:wrap;margin:20px 0}img{max-width:100%}button{font:inherit;padding:8px}pre{white-space:pre-wrap}'
pages=['閱讀我_先看這裡.html','逐項施工工程覆蓋表.html','BUG修復與待補清單.html','完整測試及驗收報告.html','素材圖片清單與預覽.html']
nav='<nav>'+''.join('<a href="'+n+'">'+n.replace('.html','')+'</a>' for n in pages)+'</nav>'
warning='<p>V0.7.3 獨立測試版・2026-10-18新三寵補完。正式母檔尚待玩家驗收；本輪發布GitHub測試頁。</p>'
def page(name,title,body):(O/name).write_text('<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><title>'+title+'</title><style>'+css+'</style><main><h1>'+title+'</h1>'+nav+warning+body+'</main></html>','utf8')
page(pages[0],'V0.7.3 新三寵補完交付','<p><a href="九州修仙錄_V0.7.3_獨立測試版.html">開啟最新版遊戲</a></p><p>已接入本輪49列八核，保留11列現有八核；神秘蛋25種全部開放，孵化6遊戲小時。靈珠蝶不重乘特殊種倍率。</p><p>原本網站首頁仍為0.7.2正式版；本輪成果在preview/v0.7.3獨立測試頁。測試版登入畫面與遊戲內均標示0.7.3，存檔仍與正式版隔離。</p><p>L19、L20、L34解除八核待補；L33其餘圖鑑美術仍為部分實裝。</p>')
counts=dict(collections.Counter(x['implementation'] for x in coverage))
table='<p>'+e(counts)+'</p><button onclick="document.querySelectorAll(\'tr[data-status]\').forEach(r=>r.hidden=r.dataset.status!==\'部分實裝\')">只看部分實裝</button> <button onclick="document.querySelectorAll(\'tr[data-status]\').forEach(r=>r.hidden=false)">顯示全部</button><table><tr><th>項目</th><th>狀態</th><th>內容</th><th>程式位置</th></tr>'+''.join('<tr data-status="'+e(r['implementation'])+'"><td>'+e(r['id']+' '+r['item'])+'</td><td>'+e(r['implementation'])+'</td><td>'+e(r['reason'])+'</td><td><a href="施工來源/'+e(r['source'])+'">'+e(r['source'])+'</a></td></tr>' for r in coverage)+'</table>'
page(pages[1],'逐項施工工程覆蓋表',table)
fixes=['49列八核接入、保留11列舊值，靈珠蝶不重複乘種級。','開放新三寵6小時孵化；沿用合法種級及滿格孵化規則。','修正硬黑蠍既定毒針被舊種族名稱擋住。','修正JZ071.ensure造成存檔版本回到0.7.2；測試登入畫面明示0.7.3。']
page(pages[2],'BUG修復與待補清單','<ul>'+''.join('<li>'+e(v)+'</li>' for v in fixes)+'</ul><p>原「新寵物全境界八核」待補已解除。</p><ul>'+''.join('<li>'+e(v['id']+'：'+v['reason'])+'</li>' for v in meta['pending'])+'</ul><p>其他圖鑑圖片仍有352個後續資源目標；素材69張已完成。</p>')
(O/'BUG修復與待補清單.json').write_text(json.dumps({'fixed':fixes,'pending':meta['pending']},ensure_ascii=False,indent=2),'utf8')
tests=[]
for f in ['施工測試結果.json','擴充流程測試結果.json','A線與NPC公式測試結果.json','B線與補充定案測試結果.json','新三寵正常孵化與成長驗收.json']:
 d=read(O/f);assert all(v['pass'] for v in d['rows']) and not d.get('errors'),f
 tests.append({'file':f,'passed':len(d['rows'])})
page(pages[3],'完整測試及驗收報告','<p>本次重新執行'+str(sum(t['passed'] for t in tests))+'項檢查，全部通過。</p><table><tr><th>測試組</th><th>通過</th></tr>'+''.join('<tr><td><a href="'+t['file']+'">'+t['file']+'</a></td><td>'+str(t['passed'])+'</td></tr>' for t in tests)+'</table><p>新三寵均由神秘蛋實際選取、359分鐘不可開、360分鐘開啟；經存檔續讀、練氣一層至築基圓滿的正式突破／破境操作、升星、五星二選一、餵食至10心、正式接取任務。成長測試提供達標修為與物品並固定成功亂數。</p><p>10心完成條件採上述正常孵化寵物，在受控的正式妖物戰鬥事件中施放技能累計；沒有直接寫入任務計數。此事件測試與完整手動冒險流程分別標示，不冒稱已逐場手動遊玩。</p><p>其餘A／B主線、長右、NPC生成、委託、醫館30分鐘與存檔回歸通過。最後玩家驗收尚待進行。</p><img src="登入版本073.png"><img src="神秘蛋正常孵化.png">')
shutil.copy2(PREV/pages[4],O/pages[4])
preview=(P/'preview.html').read_text('utf8').replace('/github-release/assets/','assets/').replace('/新增美術_2026-10-16/','new-assets/').replace('/素材美術_2026-10-18/','material-assets/')
(W/'index.html').write_text(preview,'utf8')
for f in list(P.glob('*.js'))+[P/'build.py']:shutil.copy2(f,W/'test-source/v073'/f.name)
(O/'新三寵完整八核.json').write_text(json.dumps(meta['petAudit'],ensure_ascii=False,indent=2),'utf8')
manifest={'version':'0.7.3','supplement':'2026-10-18-pet-complete','published':False,'formalUpdated':False,'coverage':counts,'tests':tests,'newCoreRows':49,'retainedCoreRows':11,'missingPetRows':0}
(O/'本輪交付清單.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),'utf8')
print(json.dumps(manifest,ensure_ascii=False))
