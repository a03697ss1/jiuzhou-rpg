from pathlib import Path
import json,html,shutil,hashlib,importlib.util
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'V0.7.3_逐項修正_2026-10-18';W=R/'V0.7.3_獨立測試_2026-10-17/Git測試分支'
esc=html.escape
labels=['深窟座標與道路','野外妖物境界與東州顯示','七種製作功能顯示成品圖','全部物品補圖','背包裝備比較','背包物品圖片','圖鑑返回保留捲動','圖鑑返回按鈕','圖鑑視窗加大','任務物品移出圖鑑但保留圖片','四隻新妖物背景','新寵物合法技能隨機取得','圖鑑卡片分格美化','妖物技能可點選詳情','精晶礦靈掉落','臂巨礦掉落','素材來源機率四捨五入','妖物全區與東州分頁','素材類型與階級組合篩選','圖鑑依類型及階級排序','圖鑑搜尋','NPC分頁與人物順位','地區分頁與類型順位','裝備部位分頁','飾品分頁','藥水丹藥合併分類','丹藥百分比浮點文字','禮物用途文字','物品實際來源與來源未知','八狀態移至幫助','功法階級分頁','功法階級排序','功法階級顯示','幫助可捲至最下方','幫助相關連結黃字','幫助詳述玩法','移除幫助開發用詞','治療境界倍率與範例','移除NPC美術池內部說明','八狀態整合一頁與幫助重寫','補齊問道檯與已開放玩法','長右專屬血條內數字','長右戰我方全身立繪','狀態移至氣血左上','第二階段全畫面提示','長右風雨雷光特效','長右禁止自動戰鬥','長右我方戰位縮小並預留敵方位置','長右稱號移至詳情','長右血條上方與階段位置','三夥伴與兩寵上限','A路線測試舊任務追蹤修復']
ids=[str(i) for i in range(1,44)]+['44a','44b']+[str(i) for i in range(45,52)]
assert len(ids)==len(labels)==52
def load(name):return json.loads((O/name).read_text('utf-8'))
reports=['逐項修正驗收.json','物品美術與介面驗收.json','施工測試結果.json','A線與NPC公式測試結果.json','B線與補充定案測試結果.json','新三寵正常孵化與成長驗收.json','舊版存檔銜接驗收.json']
results={name:load(name) for name in reports}
for name,d in results.items():assert d['rows'] and all(r['pass'] for r in d['rows']) and not d.get('errors'),name
total=sum(len(d['rows']) for d in results.values())
origins={r['name']:r for f in P.glob('revision-art-batch*.json') for r in json.loads(f.read_text('utf-8'))}
people={r['name']:r for r in json.loads((P/'revision-fullbody-manifest.json').read_text('utf-8'))}
people['邱山河']=json.loads((P/'revision-fullbody-correction.json').read_text('utf-8'))
art=[]
from PIL import Image
for folder,kind in [('物品美術_2026-10-18','物品類型共用'),('人物全身_2026-10-18','長右戰全身人物'),('素材美術_2026-10-18','沿用素材原圖')]:
 for p in sorted((R/folder).glob('*.png')):
  im=Image.open(p);origin=(people if kind=='長右戰全身人物' else origins).get(p.stem,{})
  art.append({'name':p.stem,'category':kind,'path':folder+'/'+p.name,'originalSource':origin.get('source','沿用既有素材原圖'),'prompt':origin.get('prompt',''),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'width':im.width,'height':im.height,'alpha':im.mode=='RGBA' and im.getchannel('A').getextrema()[0]==0})
assert len(art)==148 and all(r['alpha'] for r in art)
(O/'物品圖片來源與檔案清單.json').write_text(json.dumps(art,ensure_ascii=False,indent=2),'utf-8')
(O/'缺圖清單.json').write_text(json.dumps({'registeredItems':results['物品美術與介面驗收.json']['rows'][0]['detail']['items'],'missing':[],'note':'同類物品共用圖片，逐件映射見完整物品圖片映射。'},ensure_ascii=False,indent=2),'utf-8')
cov=[]
for id,title in zip(ids,labels):
 tests=[f for f in reports for r in results[f]['rows'] if id in list(map(str,r.get('ids',[])))]
 assert tests,(id,title)
 source='revision-world1018.js' if id in ['1','2','12','15','16','17','27','28','50','51'] else 'revision-items1018.js' if id in ['3','4','5','6','29'] else 'revision-boss1018.js' if id in ['42','43','44a','44b','45','46','47','48','49'] else 'revision-help1018.js' if id in ['30','34','35','36','37','38','39','40','41'] else 'revision-codex1018.js'
 cov.append({'id':id,'title':title,'state':'已實裝；自動驗收通過；待玩家驗收','source':source,'tests':sorted(set(tests)),'remaining':'美術與文字呈現待玩家逐項確認；來源未知條目未新增取得途徑。' if id in ['4','29','43','45'] else ''})
(O/'逐項施工工程覆蓋表.json').write_text(json.dumps(cov,ensure_ascii=False,indent=2),'utf-8')
source=O/'施工來源';source.mkdir(exist_ok=True)
for f in P.iterdir():
 if f.suffix in ['.js','.cjs','.py','.css','.json'] and not f.name.startswith('publish-') and f.stat().st_size<5_000_000:shutil.copy2(f,source/f.name)
protected={}
for name,base in json.loads((P/'baseline.json').read_text('utf-8'))['protected'].items():
 p=R/name;sha=hashlib.sha256(p.read_bytes()).hexdigest();assert sha==base['sha256'],name;protected[name]={'sha256':sha,'unchanged':True}
(O/'正式檔案保護核對.json').write_text(json.dumps(protected,ensure_ascii=False,indent=2),'utf-8')
def page(title,body):return '<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+title+'</title><style>body{background:#081720;color:#d8e5eb;font:16px/1.9 "Microsoft JhengHei",sans-serif;margin:0}main{max-width:1400px;margin:auto;padding:28px}a{color:#f0d592}h1,h2,h3{color:#ead1a0}section{background:#102630;border:1px solid #365363;padding:20px;border-radius:12px;margin:18px 0}table{border-collapse:collapse;width:100%}th,td{border:1px solid #365363;padding:9px;text-align:left;vertical-align:top}img{max-width:100%}.gallery{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:12px}.gallery figure{margin:0;text-align:center;background:#112b39;border:1px solid #365363;border-radius:9px;padding:8px}.gallery img{width:130px;height:130px;object-fit:contain}.people img{height:270px}.note{color:#a9c1cc}</style><main><p><a href="閱讀我_先看這裡.html">交付目錄</a> · <a href="九州修仙錄_V0.7.3_獨立測試版.html">開啟遊戲</a></p><h1>'+title+'</h1>'+body+'</main></html>'
links='<ul>'+''.join('<li><a href="'+f+'">'+f[:-5]+'</a></li>' for f in ['逐項施工工程覆蓋表.html','BUG修復與待補清單.html','完整測試及驗收報告.html','素材圖片清單與預覽.html'])+'</ul>'
(O/'閱讀我_先看這裡.html').write_text(page('V0.7.3・10/18 逐項修正',f'<section><p>本輪52項（包含兩個44）已在目前0.7.3測試底稿上增量實裝。{total}項自動及流程檢查通過；美術與玩法仍待玩家驗收。正式母檔與正式入口沒有更新。</p><p>沿用同一個測試版存檔前綴，並保留上一輪舊版紀錄副本讀取功能。個人Chrome存檔沒有由本輪測試直接讀取。</p></section>'+links),'utf-8')
rows=''.join('<tr><td>'+r['id']+'</td><td>'+r['title']+'</td><td>'+r['state']+'</td><td><a href="施工來源/'+r['source']+'">'+r['source']+'</a><br>'+''.join('<a href="'+f+'">驗收證據</a> ' for f in r['tests'])+'</td><td>'+r['remaining']+'</td></tr>' for r in cov)
(O/'逐項施工工程覆蓋表.html').write_text(page('52項施工工程覆蓋表','<p>44a為狀態位置，44b為第二階段提示。每列均連結對應程式與本輪測試證據。</p><table><tr><th>項目</th><th>修正內容</th><th>狀態</th><th>程式與測試</th><th>剩餘事項</th></tr>'+rows+'</table>'),'utf-8')
(O/'BUG修復與待補清單.html').write_text(page('BUG修復與待補清單','<section><h2>本輪修復</h2><p>深窟位置與路線、A路線測試前置、圖鑑返回捲動、幫助底部裁切、製作成品圖、物品缺圖、丹藥百分比文字、初始寵物技能，以及長右戰的立繪、血條、狀態與階段演出。</p><h2>保留事項</h2><p>其餘七種特殊狀態依先前確認保留於遊戲，沒有新增施加功法。未登錄取得途徑的物品顯示來源未知，沒有新增掉落或商店。</p><p>素材原圖69張沿用；新增71類物品美術共用於對應物品，名稱與階級另外顯示。不是每件同類裝備各生成一張不同圖片。8張全身圖只用於長右戰，其他已驗收人物圖保留。</p><p>完整手動主線測試使用提高能力的隔離角色，以驗證流程，不代表長右數值平衡已由玩家驗收。</p></section>'),'utf-8')
body=f'<p>本輪共重新執行{total}項檢查，全部通過。以下數字不重複計入前輪報告。</p>'
for name,d in results.items():body+='<section><h2>'+name[:-5]+'（'+str(len(d['rows']))+'項）</h2><p><a href="'+name+'">完整結果</a></p><ul>'+''.join('<li>'+esc(r['name'])+'</li>' for r in d['rows'])+'</ul></section>'
body+='<section><h2>畫面證據</h2>'+''.join('<p>'+esc(f.stem)+'</p><img loading="lazy" src="'+f.name+'">' for f in sorted(O.glob('*.png')) if '施工檢查' not in f.name)+'</section>'
(O/'完整測試及驗收報告.html').write_text(page('完整測試及驗收報告',body),'utf-8')
body='<p>同一名稱在背包、圖鑑、製作與商店使用同一映射。<a href="完整物品圖片映射.json">逐件物品圖片對照表</a>。任務物品有圖，但不加入圖鑑清單。</p>'
for folder,title,cls in [('物品美術_2026-10-18','新增71類物品美術',''),('人物全身_2026-10-18','長右戰8名全身人物','people'),('素材美術_2026-10-18','沿用69張素材圖','')]:
 files=sorted((R/folder).glob('*.png'));body+='<h2>'+title+'</h2><div class="gallery '+cls+'">'+''.join('<figure><img loading="lazy" src="../'+folder+'/'+f.name+'" alt="'+f.stem+'"><figcaption>'+f.stem+'</figcaption></figure>' for f in files)+'</div>'
(O/'素材圖片清單與預覽.html').write_text(page('物品與全身圖片清單',body),'utf-8')
manifest={'version':'0.7.3','supplement':'20261018-review-fixes-1','items':52,'tests':total,'passed':total,'published':False,'formalUpdated':False,'savePrefix':'jz073-independent-20261017:','art':{'materials':69,'itemFamilies':len(list((R/'物品美術_2026-10-18').glob('*.png'))),'fullbody':8},'personalChromeRecordsVerified':False}
(O/'本輪交付清單.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),'utf-8')
preview=(P/'preview.html').read_text('utf-8')
for a,b in [('/github-release/assets/','assets/'),('/新增美術_2026-10-16/','new-assets/'),('/素材美術_2026-10-18/','material-assets/'),('/物品美術_2026-10-18/','item-assets/'),('/人物全身_2026-10-18/','fullbody-assets/')]:preview=preview.replace(a,b)
(W/'index.html').write_text(preview,'utf-8')
for folder,target in [('物品美術_2026-10-18','item-assets'),('人物全身_2026-10-18','fullbody-assets')]:shutil.copytree(R/folder,W/target,dirs_exist_ok=True)
for f in source.iterdir():shutil.copy2(f,W/'test-source/v073'/f.name)
spec=importlib.util.spec_from_file_location('pub',P/'publish-preview.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.git(W,'add','--','index.html','test-source/v073','item-assets','fullbody-assets')
if m.git(W,'diff','--cached','--name-only'):m.git(W,'commit','-m','Implement October 18 catalogue help boss and item art revisions on 0.7.3 test branch')
receipt={'commit':m.git(W,'rev-parse','HEAD'),'branch':m.git(W,'branch','--show-current'),'formalUpdated':False,'pushed':False}
(O/'本地測試分支保存紀錄.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),'utf-8')
print(json.dumps({'tests':total,'rows':52,'commit':receipt['commit']},ensure_ascii=False))
