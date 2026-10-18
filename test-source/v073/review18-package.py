from pathlib import Path
import json,html,hashlib,shutil,importlib.util
from urllib.parse import quote
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'V0.7.3_18項修正_2026-10-18';D=R/'物品獨立美術_2026-10-18';W=R/'V0.7.3_獨立測試_2026-10-17/Git測試分支';esc=html.escape
reports=['18項功能驗收.json','正常介面與藥品效果驗收.json','獨立物品美術驗收.json','施工測試結果.json','A線與NPC公式測試結果.json','B線與補充定案測試結果.json']
data={n:json.loads((O/n).read_text('utf8')) for n in reports}
for n,x in data.items():assert x['rows'] and all(r['pass'] for r in x['rows']) and not x.get('errors'),n
total=sum(len(x['rows']) for x in data.values());jobs=json.loads((O/'新增獨立圖片提示詞.json').read_text('utf8'));expected={r['name'] for r in jobs}|{'［特殊］小型煉金爐'}
assert {p.stem for p in D.glob('*.png')}==expected
art=[]
for f in sorted(D.glob('*.png')):
 im=Image.open(f);origin=D/'生成紀錄'/(f.stem+'.json');source=json.loads(origin.read_text('utf-8-sig'))['source'] if origin.exists() else 'C:/Users/User/.codex/generated_images/01a0fe64-95aa-7260-ba13-9d565c3bee39/exec-2f92caff-d5a8-4433-a089-399f5492bcea.png'
 art.append({'name':f.stem,'file':str(f),'source':source,'method':'built-in imagegen','width':im.width,'height':im.height,'transparent':im.mode=='RGBA' and im.getchannel('A').getextrema()[0]==0,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'pixelSHA256':hashlib.sha256(im.tobytes()).hexdigest()})
assert all(r['transparent'] for r in art)
assert len({r['sha256'] for r in art})==len(art)
assert len({r['pixelSHA256'] for r in art})==len(art)
(O/'物品圖片來源與檔案清單.json').write_text(json.dumps(art,ensure_ascii=False,indent=2),'utf8')
allprompts=jobs+[{'name':'［特殊］小型煉金爐','prompt':'Use case: stylized-concept. Create one finished transparent game inventory item illustration for Chinese xianxia RPG 九州修仙錄. Item: ［特殊］小型煉金爐, a small portable alchemy furnace: squat three-legged dark bronze cauldron, open round furnace mouth with gentle amber fire, compact lid and side handles, subtle cloud carvings. Single isolated object centered, whole silhouette visible, no person, no background, no words, no frame, no label, no watermark. Hand-painted semi-realistic fantasy game asset with rich material detail and clean readable outline, matching elegant Chinese cultivation RPG. Square composition. It must visibly be a furnace, never a bag or chest.'}]
(O/'完整獨立圖片提示詞.json').write_text(json.dumps(allprompts,ensure_ascii=False,indent=2),'utf8')
protected={}
for name,old in json.loads((P/'baseline.json').read_text('utf8'))['protected'].items():
 sha=hashlib.sha256((R/name).read_bytes()).hexdigest();assert sha==old['sha256'],name;protected[name]={'sha256':sha,'unchanged':True}
(O/'正式檔案保護核對.json').write_text(json.dumps(protected,ensure_ascii=False,indent=2),'utf8')
labels=['狐尾與獸角歸妖物素材','蘇璃圖鑑優先顯示同行位置','裝備逐件獨立圖片','藥品逐件圖片與階級裝飾','精確階級取得來源','移除未設計的三階凝靈妖丹','靈根丹3～5點及25種藥水正式效果','功法圖鑑醒目階級','柳清妍任務／委託入口','戰鬥戰位與權威血量同步','背包移除查看來源按鈕','特殊道具獨立圖片','主線戰鬥按鈕限定正確地點','18名NPC靈根與平民無靈根','必敗戰手動1倍與玩家確認','交談保留暫時離開並隱藏關閉','放大布告欄與下方布告箱','測試999可重複開啟長右']
coverage=[]
for i,name in enumerate(labels,1):
 evidence=[file for file,x in data.items() for row in x['rows'] if i in (row.get('id',row.get('ids',[])) if isinstance(row.get('id',row.get('ids',[])),list) else [row.get('id')])]
 if i==17:evidence.append(reports[1])
 assert evidence,(i,name)
 coverage.append({'id':i,'title':name,'state':'已實裝；驗收測試通過；待玩家檢查','source':'review18-art.js' if i in [3,4,8,12] else 'review18-fixes.js','tests':list(dict.fromkeys(evidence))})
(O/'逐項施工工程覆蓋表.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2),'utf8')
source=O/'施工來源';source.mkdir(exist_ok=True)
for f in P.iterdir():
 if f.suffix in ['.js','.cjs','.py','.css','.json'] and f.stat().st_size<5_000_000:shutil.copy2(f,source/f.name)
def page(title,body):return '<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+title+'</title><style>body{background:#081720;color:#dbe9ee;font:16px/1.9 Microsoft JhengHei,sans-serif;margin:0}main{max-width:1450px;margin:auto;padding:30px}a{color:#f1ce77}section{padding:20px;margin:20px 0;background:#102631;border:1px solid #345369;border-radius:12px}h1,h2{color:#edd19b}table{border-collapse:collapse;width:100%}th,td{border:1px solid #36505e;padding:10px;text-align:left;vertical-align:top}.gallery{display:grid;grid-template-columns:repeat(auto-fill,minmax(155px,1fr));gap:12px}.gallery figure{margin:0;background:#102b3a;border:1px solid #35556b;border-radius:10px;padding:8px;text-align:center}.gallery img{width:140px;height:140px;object-fit:contain}img{max-width:100%}</style><main><p><a href="閱讀我_先看這裡.html">交付目錄</a> · <a href="九州修仙錄_V0.7.3_獨立測試版.html">開啟遊戲</a></p><h1>'+title+'</h1>'+body+'</main></html>'
links=['逐項施工工程覆蓋表.html','BUG修復與待補清單.html','完整測試及驗收報告.html','素材圖片清單與預覽.html']
(O/'閱讀我_先看這裡.html').write_text(page('V0.7.3・本輪18項修正',f'<section><p>18項修正已實裝，{total}項檢查通過。本輪新增{len(art)}張獨立物品圖，包含254件裝備、各階藥品及特殊物品。正式母檔與正式入口保持原樣，等待玩家驗收。</p><p>仍使用同一測試版存檔前綴，不重新建立或覆寫玩家原有紀錄。驗收使用獨立瀏覽器與測試999。</p></section><ul>'+''.join('<li><a href="'+f+'">'+f[:-5]+'</a></li>' for f in links)+'</ul>'),'utf8')
table='<table><tr><th>項目</th><th>修正內容</th><th>狀態</th><th>證據</th></tr>'+''.join('<tr><td>'+str(r['id'])+'</td><td>'+r['title']+'</td><td>'+r['state']+'</td><td><a href="施工來源/'+r['source']+'">程式位置</a><br>'+''.join('<a href="'+n+'">'+n+'</a><br>' for n in r['tests'])+'</td></tr>' for r in coverage)+'</table>'
(O/'逐項施工工程覆蓋表.html').write_text(page('18項施工工程覆蓋表',table),'utf8')
(O/'BUG修復與待補清單.html').write_text(page('BUG修復與待補清單','<section><h2>已修正</h2><p>主線敵方陣形不再引用開戰前的妖物副本，戰位、詳細資訊、選取目標與戰鬥結算使用同一組物件。長右測試會重設037／038測試狀態，已完成者也能重打。主線033A按鈕只在青陽山及正確進度顯示。</p><p>來源以完整階級名稱比對，沒有新增中、高、仙、天階藥水的取得途徑；這12項維持來源未知。移除三階凝靈妖丹，不影響其他妖丹。</p><h2>名稱核對</h2><p>本輪提供的「萬乾坤」水51對應遊戲現有「萬錢坤」。保留現有NPC姓名、任務與位置，未新增第二名NPC。</p><h2>保留事項</h2><p>目前無阻擋本輪18項施工的缺稿。尚未指定來源的物品顯示來源未知；未新增掉落、配方或商店。同名裝備的品質前綴版本沿用該件裝備圖，254個不同裝備名稱各有獨立圖片。更早的未設計玩法與其餘七種狀態施加來源仍依既有待補紀錄保留。</p></section>'),'utf8')
body=f'<p>本輪重新執行{total}項檢查，全部通過。完整A／B線測試角色提高能力以驗證流程，並非難度平衡驗收。兩線必敗戰都實際按下繼續。</p>'
for file,x in data.items():body+='<section><h2>'+file[:-5]+'（'+str(len(x['rows']))+'項）</h2><p><a href="'+file+'">完整結果</a></p><ul>'+''.join('<li>'+esc(r['name'])+'</li>' for r in x['rows'])+'</ul></section>'
for f in sorted(O.glob('*.png')):body+='<section><h2>'+esc(f.stem)+'</h2><img loading="lazy" src="'+quote(f.name)+'"></section>'
(O/'完整測試及驗收報告.html').write_text(page('完整測試及驗收報告',body),'utf8')
body='<p>使用內建imagegen製作；每個物品名稱有獨立PNG，跨背包、圖鑑與製作介面共用同一張。原69張素材圖保留。<a href="物品圖片來源與檔案清單.json">圖片來源與SHA256</a> · <a href="完整獨立圖片提示詞.json">完整提示詞</a> · <a href="完整物品圖片映射.json">物品映射</a></p><div class="gallery">'+''.join('<figure><img loading="lazy" src="../物品獨立美術_2026-10-18/'+quote(r['name']+'.png')+'" alt="'+esc(r['name'])+'"><figcaption>'+esc(r['name'])+'</figcaption></figure>' for r in art)+'</div>'
(O/'素材圖片清單與預覽.html').write_text(page('本輪獨立物品圖片清單',body),'utf8')
(O/'缺圖清單.json').write_text(json.dumps({'requestedIndependentImages':len(art),'missing':[],'registeredItemImages':'完整物品圖片映射.json'},ensure_ascii=False,indent=2),'utf8')
manifest={'version':'0.7.3','build':'20261018-review18-1','items':18,'tests':total,'passed':total,'newIndependentImages':len(art),'baseEquipmentImages':254,'published':False,'formalUpdated':False,'savePrefix':'jz073-independent-20261017:'}
(O/'本輪交付清單.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),'utf8')
preview=(P/'preview.html').read_text('utf8')
local=preview
for prefix in ['/github-release/assets/','/新增美術_2026-10-16/','/素材美術_2026-10-18/','/物品美術_2026-10-18/','/人物全身_2026-10-18/','/物品獨立美術_2026-10-18/']:local=local.replace(prefix,'..'+prefix)
(O/'九州修仙錄_V0.7.3_獨立測試版.html').write_text(local+'<script>window.JZ073_BUILD_ID="20261018-review18-1";</script>','utf8')
for a,b in [('/github-release/assets/','assets/'),('/新增美術_2026-10-16/','new-assets/'),('/素材美術_2026-10-18/','material-assets/'),('/物品美術_2026-10-18/','item-assets/'),('/人物全身_2026-10-18/','fullbody-assets/'),('/物品獨立美術_2026-10-18/','unique-item-assets/')]:preview=preview.replace(a,b)
(W/'index.html').write_text(preview,'utf8');shutil.copytree(D,W/'unique-item-assets',dirs_exist_ok=True)
for f in source.iterdir():shutil.copy2(f,W/'test-source/v073'/f.name)
spec=importlib.util.spec_from_file_location('pub',P/'publish-preview.py');pub=importlib.util.module_from_spec(spec);spec.loader.exec_module(pub)
assert not pub.git(W,'diff','--cached','--name-only'),'Unexpected staged source changes'
pub.git(W,'add','--','index.html','test-source/v073','unique-item-assets')
if pub.git(W,'diff','--cached','--name-only'):pub.git(W,'commit','-m','Implement 18 review fixes and independent item artwork in 0.7.3 test branch')
receipt={'commit':pub.git(W,'rev-parse','HEAD'),'branch':pub.git(W,'branch','--show-current'),'formalUpdated':False,'pushed':False}
(O/'本地測試分支保存紀錄.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),'utf8')
print(json.dumps({'tests':total,'coverage':18,'images':len(art),'source':receipt},ensure_ascii=False))
