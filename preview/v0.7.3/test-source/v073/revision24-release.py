from pathlib import Path
import importlib.util,json,shutil,re,sys,datetime,hashlib,html,urllib.parse
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'V0.7.3_24項修正_2026-10-19';A=R/'修正24美術_2026-10-19';BUILD='20261019-revision24-1'
spec=importlib.util.spec_from_file_location('pub',P/'publish-preview.py');pub=importlib.util.module_from_spec(spec);spec.loader.exec_module(pub)
T=R/'V0.7.3_獨立測試_2026-10-17/Git測試分支';D=pub.DEST;STATE=P/'revision24-release-state.json'
MODULES=['revision24-items','revision24-combat','revision24-ui','revision24-art']
FILES=[n+'.js' for n in MODULES]+['revision24-test.cjs','revision24-battle.cjs','revision24-effects.cjs','revision24-growth-save.cjs','revision24-inspect.cjs','revision24-release.py','revision24-verify.py','build.py']
TESTS=['介面與物品驗收.json','戰鬥與嚴重BUG驗收.json','問道18裝備特殊效果驗收.json','配方成長存讀檔驗收.json']
ITEMS=[
(1,'護盾值','血條上方顯示護盾數字，承傷扣除、破盾消失。','revision24-combat.js'),
(2,'問道裝備與五種丹藥','18件裝備採本輪完整數值、位階與效果；補完整商店。五種丹藥35點可重複兌換，鎮心丹改為抵抗＋12、3回合。','revision24-items.js / revision24-combat.js'),
(3,'紀念品歷練','已查明現行領取沒有給歷練；現有原表只有紀念品敘述，沒有獎勵數字。待玩家補充每件數量及重複取得規則。','baseline-scripts/99-jzw-word-integration.js：jzClaimNpcGift'),
(4,'缺圖與凝力丹','核對912個現有物品名稱之圖片路徑，缺檔0。凝力丹等五丹沿用既有獨立圖，補齊商店顯示；獸技殘頁新增獨立圖。','revision24-items.js / revision24-art.js'),
(5,'一、二階素材箱','換成樸素木箱與鐵包角木箱，共用同一映射；保留開箱內容與數量。','revision24-art.js'),
(6,'戰意玉說明','特殊裝備進階素材。','revision24-items.js'),
(7,'戰鬥背包排除未開箱','自選護體丹箱等箱子不出現在戰鬥背包；直接呼叫使用亦不消耗。','revision24-items.js'),
(8,'長右水／水雷本體','第一階段水元素，第二階段切換水雷立繪；血條與本體均依實際階段換圖。','revision24-art.js'),
(9,'BOSS勝利後氣血0','玩家倒地而夥伴擊殺長右後至少1氣血，可醫館治療；通用BOSS最終勝利寫回同樣保護。','revision24-combat.js：ensureBossSurvivor24 / battleWin'),
(10,'獸魂晶','寵物升星核心素材。','revision24-items.js'),
(11,'圖鑑搜尋輸入','更新搜尋結果時保留輸入元件、焦點與選取；中文組字期間不重畫。','revision24-ui.js：catalogSearch1018'),
(12,'東州大禮包','使用按鈕移入物品卡片；實際使用發放與數量正常。','revision24-items.js：renderBag'),
(13,'獸靈果丹與靈獸露丹','兩者配方各自專用素材×5；物品庫與材料庫共用計數。公共爐實際製作通過，永久＋5／＋20與屬傷10%上限通過。','revision24-items.js：petMaterialCount24 / r59ConsumeIngredients'),
(14,'寵物自選專屬技能箱','打開後可自選該寵物合法池技能。沿用既有合法技能池。','revision24-items.js'),
(15,'獸技殘頁','萬獸檯35點兌換改為獸技殘頁；描述為妖物技能相關素材，可用於特殊合成。','revision24-items.js'),
(16,'初階寵物用破境丹','寵物境界突破與破境率＋5%。','revision24-items.js'),
(17,'中階寵物用破境丹','寵物境界突破與破境率＋8%。','revision24-items.js'),
(18,'靈契玉','進階寵物裝備用材料。','revision24-items.js'),
(19,'萬獸徽記','採用本輪完整敘述：五星特殊突破及萬獸檯高級兌換憑證。','revision24-items.js'),
(20,'寵物秘術卷軸','提升一層境界，不可用於破境；實測圓滿拒用且不扣道具。','revision24-items.js / 既有JZR.petAdvance'),
(21,'出售限制','所有［特殊］及自選箱不可出售、不列入出售介面。','revision24-items.js：saleBlocked'),
(22,'功法殘卷售價','每個實際出售取得200靈幣。','revision24-items.js：sellQuote'),
(23,'突破／破境數值預覽','玩家、永久夥伴與寵物顯示目前、提升後、增加量；玩家與夥伴實際突破後八核與預覽一致。','revision24-ui.js'),
(24,'築基圓滿上限','玩家築基圓滿的突破按鈕關閉，直接呼叫亦拒絕；不扣修為、歷練或丹藥。','revision24-ui.js')]
def prepare():
 tests=[]
 for n in TESTS:
  d=json.loads((O/n).read_text('utf8'));assert all(x['pass'] for x in d['rows']) and not d['errors'],n;tests+=d['rows']
 assert len(tests)==42
 regression=[(R/'V0.7.3_物品與收禮修正_2026-10-19','連續野外戰鬥診斷.json'),(R/'V0.7.3_物品與收禮修正_2026-10-19','主線連續戰鬥退出驗收.json'),(R/'V0.7.3_裝備圖片修正_2026-10-19','裝備圖片實際驗收.json')]
 regression_count=0
 for folder,n in regression:
  d=json.loads((folder/n).read_text('utf8'));assert all(x['pass'] for x in d['rows']) and not d['errors'],n;shutil.copy2(folder/n,O/('回歸_'+n));regression_count+=len(d['rows'])
 for name,old in json.loads((P/'baseline.json').read_text('utf8'))['protected'].items():assert pub.digest(R/name)==old['sha256'],name
 assert not pub.git(pub.W,'diff','--name-only')
 state={'build':BUILD,'url':pub.URL+'?build='+BUILD,'base':pub.git(pub.W,'rev-parse','HEAD'),'formalUpdated':False,'completed':23,'pending':[3],'tests':len(tests),'regressionTests':regression_count,'protectedBlobs':{n:pub.git(pub.W,'rev-parse','HEAD:'+n) for n in ['index.html','定案規則_0.7.2.json']}}
 runtime=json.loads((P/'revision24-runtime.json').read_text('utf8'));audit=[]
 for row in runtime['icons']:
  src=row['src'];path=None if src=='data-image' else R/urllib.parse.unquote(src.split('?')[0].lstrip('/'));audit.append({**row,'exists':path is None or path.is_file()})
 assert len(audit)==912 and all(a['exists'] for a in audit)
 (O/'全部物品圖片映射核對.json').write_text(json.dumps({'count':len(audit),'missing':0,'rows':audit},ensure_ascii=False,indent=2),'utf8')
 souvenirs=[{'npc':npc,'hearts':heart,'name':n,'qty':qty,'experience':None} for npc,gifts in runtime['gifts'].items() for row in gifts for heart,n,qty in [row[:3]] if n in runtime['souvenirs']]
 pending={'id':3,'status':'待補','finding':'現行jzClaimNpcGift只給物品並記錄已領取，沒有增加歷練。現存紀念品原表只有敘述，未給歷練數值。','needed':['各紀念品獲得的歷練數量','同物品重複獲得是否再次給予歷練'],'sources':['baseline-scripts/99-jzw-word-integration.js：souvenirs / jzClaimNpcGift','revision24-runtime.json：gifts / souvenirs'],'knownNpcSouvenirs':souvenirs}
 (O/'紀念品歷練待補清單.json').write_text(json.dumps(pending,ensure_ascii=False,indent=2),'utf8')
 for folder in [T,D]:
  f=folder/'index.html';s=f.read_text('utf8');old={m[1]:hashlib.sha256(m[2].encode()).hexdigest() for m in re.finditer(r'<script id="jz073-([^"<>]+)">(.*?)</script>',s,re.S)}
  for name in MODULES:
   assert 'id="jz073-'+name+'"' not in s
   code=(P/(name+'.js')).read_text('utf8').replace('/修正24美術_2026-10-19/','revision24-assets/')
   s+='\n<script id="jz073-'+name+'">'+code+'</script>'
  s,n=re.subn(r'window.JZ073_BUILD_ID="[^"]+";',lambda m:'window.JZ073_BUILD_ID='+json.dumps(BUILD)+';',s);assert n==1
  after={m[1]:hashlib.sha256(m[2].encode()).hexdigest() for m in re.finditer(r'<script id="jz073-([^"<>]+)">(.*?)</script>',s,re.S)};assert all(after[k]==v for k,v in old.items());f.write_text(s,'utf8')
  dest=folder/'revision24-assets';dest.mkdir(exist_ok=True)
  for asset in A.iterdir():
   if folder==T or asset.suffix!='.png':shutil.copy2(asset,dest/asset.name)
 # Replace ten ornate early-tier box images with two shared modest tier assets. Keep originals in the source archive.
 archive=T/'qa-archive/20261019-boxes';archive.mkdir(parents=True,exist_ok=True);replaced=[]
 for f in list((D/'unique-item-assets').glob('*.webp')):
  name=f.name
  if not (((('一階' in name or '二階' in name) and ('自選' in name or '綜合' in name)) or name in ['［特殊］自選晶石箱.webp','［特殊］自選護體丹箱.webp']) and '箱' in name):continue
  assert f.resolve().parent==(D/'unique-item-assets').resolve();shutil.copy2(f,archive/name);assert pub.digest(f)==pub.digest(archive/name)
  target='revision24-assets/'+('二階樸素素材箱.webp' if '二階' in name or '晶石' in name else '一階樸素素材箱.webp')
  for report in D.rglob('*'):
   if report.is_file() and report.suffix in ['.html','.js','.json','.css','.md']:
    text=report.read_text('utf8');changed=text.replace('unique-item-assets/'+name,target).replace('unique-item-assets/'+urllib.parse.quote(name),urllib.parse.quote(target,safe='/'))
    if changed!=text:report.write_text(changed,'utf8')
  replaced.append({'old':name,'current':target,'oldSha256':pub.digest(f),'archivedSource':'https://raw.githubusercontent.com/a03697ss1/jiuzhou-rpg/test/v0.7.3-20261017/qa-archive/20261019-boxes/'+urllib.parse.quote(name)});f.unlink()
 assert len(replaced)==10
 (O/'素材箱替換清單.json').write_text(json.dumps(replaced,ensure_ascii=False,indent=2),'utf8')
 for folder in [T/'test-source/v073',D/'test-source/v073',D/'施工來源',O/'施工來源']:
  folder.mkdir(parents=True,exist_ok=True)
  for name in FILES:shutil.copy2(P/name,folder/name)
 local=(P/'preview.html').read_text('utf8')
 for prefix in ['/github-release/assets/','/新增美術_2026-10-16/','/素材美術_2026-10-18/','/物品美術_2026-10-18/','/人物全身_2026-10-18/','/物品獨立美術_2026-10-18/','/物品修正美術_2026-10-19/','/長右血條正式美術_2026-10-19/','/修正24美術_2026-10-19/']:local=local.replace(prefix,'..'+prefix)
 (O/'九州修仙錄_V0.7.3_獨立測試版.html').write_text(local+'<script>window.JZ073_BUILD_ID='+json.dumps(BUILD)+';</script>','utf8')
 coverage={'build':BUILD,'version':'0.7.3','completed':23,'pending':1,'tests':len(tests),'regressionTests':regression_count,'formalUpdated':False,'rows':[{'id':i,'title':title,'status':'待補' if i==3 else '已實裝／驗證通過','result':desc,'code':code,'evidence':TESTS if i!=3 else ['紀念品歷練待補清單.json']} for i,title,desc,code in ITEMS]}
 (O/'逐項施工覆蓋表.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2),'utf8')
 body='<h1>V0.7.3・24項物品與戰鬥修正</h1><p><a href="index.html?build='+BUILD+'">開啟最新可遊玩測試版</a> · '+BUILD+'</p><p>本輪23項完成，第3項紀念品歷練待補數字。42項新增驗收與'+str(regression_count)+'項回歸檢查通過。正式母檔、正式版本及正式入口保持不變。</p><h2>逐項施工覆蓋表</h2><table><thead><tr><th>項目</th><th>狀態</th><th>實裝與測試結果</th><th>程式位置</th></tr></thead><tbody>'
 for row in coverage['rows']:body+='<tr><td>'+str(row['id'])+' · '+html.escape(row['title'])+'</td><td>'+row['status']+'</td><td>'+html.escape(row['result'])+'</td><td>'+html.escape(row['code'])+'</td></tr>'
 body+='</tbody></table><h2>BUG修復</h2><p>BOSS勝利後的0氣血已修正，長右與通用BOSS寫回路徑均驗證。未開箱的護體丹箱移出戰鬥背包；圖鑑中文組字與逐字輸入保持焦點；突破預覽與實際成功八核一致；鎮心丹不再使用舊身法效果；補回完整問道兌換清單與裝備正名。</p><h2>待補</h2><p>紀念品領取目前確實沒有歷練。現存表僅有紀念品敘述，沒有可引用的獎勵數字，故本輪沒有自行發放或宣稱此項完成。請補各紀念品歷練數量與重複取得規則。<a href="10-19E_紀念品歷練待補清單.json">對象與原始資料清單</a></p><h2>完整測試及驗收</h2>'
 for n in TESTS:
  data=json.loads((O/n).read_text('utf8'));body+='<h3>'+n.replace('.json','')+'</h3><p><a href="10-19E_'+n+'">原始驗收紀錄</a></p><ul>'+''.join('<li>'+html.escape(x['name'])+'：通過</li>' for x in data['rows'])+'</ul>'
 body+='<p>回歸：28種一般妖物連續戰鬥、A線2場與B線3波主線、6項裝備操作。控制單位的18件特殊效果驗算另有實際商店、正式施法、手動BOSS、公共爐製作、正常孵化與存讀檔作交叉驗證；未將測試用BOSS旗標或敵方隨從加入正式遭遇設定。</p><h2>圖片清單與來源</h2><p>核對912個現有名稱的圖片路徑，缺檔0；已有獨立圖的凝力丹等五丹沿用。內建image_gen製作5張新圖，保留原生解析度與透明度，WebP僅作無損編碼。</p><p><a href="10-19E_全部物品圖片映射核對.json">全部物品圖片清單</a> · <a href="revision24-assets/生圖提示詞與素材清單.json">生圖提示詞與來源</a> · <a href="revision24-assets/無損美術驗證.json">無損驗證</a> · <a href="10-19E_素材箱替換清單.json">10款低階箱外觀替換對應</a></p><ul>'
 for name in ['長右_水','長右_水雷','一階樸素素材箱','二階樸素素材箱','獸技殘頁']:body+='<li><a href="revision24-assets/'+name+'.webp">'+name+'・正式圖片</a></li>'
 body+='</ul>'
 for name in ['長右第一階段水元素與護盾','長右第二階段水雷本體','玩家倒地勝利後可治療','問道完整兌換與圖片','玩家突破數值預覽','夥伴突破數值預覽']:
  shutil.copy2(O/(name+'.webp'),D/('10-19E_'+name+'.webp'));body+='<h3>'+name+'</h3><img loading="lazy" src="10-19E_'+name+'.webp">'
 report='<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>0.7.3 24項修正覆蓋與驗收</title><style>body{max-width:1450px;margin:28px auto;padding:0 24px;background:#091820;color:#dcebef;font:16px/1.85 Microsoft JhengHei}h1,h2,h3{color:#eed5a0}a{color:#f1cf83}img{max-width:100%;border:1px solid #486476}table{border-collapse:collapse;width:100%}th,td{border:1px solid #385063;padding:10px;text-align:left;vertical-align:top}td:first-child{min-width:120px}td:last-child{font-size:12px;overflow-wrap:anywhere}</style>'+body+'</html>'
 (D/'10-19E_24項修正覆蓋與驗收報告.html').write_text(report,'utf8');(O/'24項修正覆蓋與驗收報告.html').write_text(report.replace('index.html?build=','九州修仙錄_V0.7.3_獨立測試版.html?build=').replace('10-19E_','').replace('revision24-assets/','../修正24美術_2026-10-19/'),'utf8')
 for n in TESTS+['逐項施工覆蓋表.json','紀念品歷練待補清單.json','全部物品圖片映射核對.json','素材箱替換清單.json']+['回歸_'+n for _,n in regression]:shutil.copy2(O/n,D/('10-19E_'+n))
 f=D/'本輪交付清單.json';d=json.loads(f.read_text('utf8'));d.update(build=BUILD,revision24=coverage);f.write_text(json.dumps(d,ensure_ascii=False,indent=2),'utf8')
 f=D/'閱讀我_先看這裡.html';s=f.read_text('utf8');note='<section id="revision24"><h2>10/19 最新24項修正</h2><p>23項完成，紀念品歷練數量待補。護盾、問道商店、0氣血勝利、搜尋與突破預覽等均已驗證。</p><a href="10-19E_24項修正覆蓋與驗收報告.html">逐項覆蓋與驗收</a> · <a href="index.html?build='+BUILD+'">最新遊戲</a></section>';s=s.replace('</h1>','</h1>'+note,1);f.write_text(s,'utf8')
 state['siteBytes']=sum(f.stat().st_size for f in pub.W.rglob('*') if f.is_file() and '.git' not in f.parts);assert state['siteBytes']<1073741824,state['siteBytes']
 pub.git(T,'add','--','index.html','test-source/v073','revision24-assets','qa-archive');pub.git(T,'commit','-m','Implement 23 requested item combat and UI fixes; document missing souvenir experience rule')
 state['sourceCommit']=pub.git(T,'rev-parse','HEAD');STATE.write_text(json.dumps(state,ensure_ascii=False,indent=2),'utf8');print(json.dumps(state,ensure_ascii=False))
def publish():
 state=json.loads(STATE.read_text('utf8'));pub.git(T,'push','origin','HEAD:refs/heads/test/v0.7.3-20261017');pub.git(pub.W,'add','--',pub.PREFIX)
 assert all(n.startswith(pub.PREFIX+'/') for n in pub.git(pub.W,'diff','--cached','--name-only','-z').split('\0') if n)
 pub.git(pub.W,'commit','-m','Publish 0.7.3 item combat and UI fixes only to preview; keep souvenir amount pending')
 for n,v in state['protectedBlobs'].items():assert pub.git(pub.W,'rev-parse','HEAD:'+n)==v
 assert all(n.startswith(pub.PREFIX+'/') for n in pub.git(pub.W,'diff','--name-only','-z',state['base'],'HEAD').split('\0') if n)
 pub.git(pub.W,'push','origin','HEAD:refs/heads/main');state.update(published=True,deploymentCommit=pub.git(pub.W,'rev-parse','HEAD'),publishedAt=datetime.datetime.now().astimezone().isoformat(timespec='seconds'));(O/'GitHub測試發布紀錄.json').write_text(json.dumps(state,ensure_ascii=False,indent=2),'utf8');print(json.dumps(state,ensure_ascii=False))
if __name__=='__main__':{'prepare':prepare,'publish':publish}[sys.argv[1]]()
