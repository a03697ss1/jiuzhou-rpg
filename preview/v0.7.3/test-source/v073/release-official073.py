from pathlib import Path
import importlib.util,json,shutil,re,sys,datetime,hashlib,html,gzip,subprocess
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'V0.7.3_正式發布_2026-10-19';QA=R/'V0.7.3_歷練與夥伴背景_2026-10-19';A=R/'郵箱背包美術_2026-10-19';BUILD='20261019-official073-1'
spec=importlib.util.spec_from_file_location('pub',P/'publish-preview.py');pub=importlib.util.module_from_spec(spec);spec.loader.exec_module(pub);T=pub.O/'Git測試分支';D=pub.DEST;STATE=P/'official073-release-state.json'
MODULES=['experience1019','partner-background1019','inventory-layout1019','help-scroll1019','inventory-mail1019','inventory-art1019','official073']
FILES=[n+'.js' for n in MODULES]+['build.py','experience-test.cjs','experience-battle-test.cjs','inventory-mail-test.cjs','mail-normal-flow-test.cjs','mail-art.cjs','release-official073.py']
TESTS=['歷練與夥伴背景驗收.json','戰鬥歷練驗收.json','背包郵箱固定格驗收.json','郵箱正常取得流程驗收.json']
OLD={'0.7.0':'6b140ae','0.7.1':'be25276','0.7.2':'a420a77'}
def blob(ref,name):return subprocess.check_output([pub.G,'-c','safe.directory='+pub.W.as_posix(),'-C',str(pub.W),'show',ref+':'+name])
def jsdump(v):return json.dumps(v,ensure_ascii=False).replace('</','<\\/')
def official(s):
 def amend(m):return m[0].replace('獨立測試・待玩家驗收','正式版').replace('masterPromoted=false','masterPromoted=true').replace('V0.7.3 獨立測試','V0.7.3').replace('0.7.3 獨立測試','0.7.3')
 s,n=re.subn(r'<script id="jz072-official">.*?</script>',amend,s,flags=re.S);assert n==1
 s=s.replace('<head>','<head><base href="preview/v0.7.3/"><script>window.JZ073_OFFICIAL=true;</script>',1)
 return s
def legacy_page(v,sha):
 injection='<base href="'+pub.URL.replace('preview/v0.7.3/','')+'"><script>(()=>{const p="legacy-v'+v+':",g=Storage.prototype.getItem,s=Storage.prototype.setItem,r=Storage.prototype.removeItem;Storage.prototype.getItem=function(k){const own=g.call(this,p+k);if(own!==null)return own;const old=g.call(this,k);if(old!==null)s.call(this,p+k,old);return old;};Storage.prototype.setItem=function(k,v){s.call(this,p+k,v);};Storage.prototype.removeItem=function(k){r.call(this,p+k);};})();</script>'
 # Same-origin local testing uses the same archive base, rather than production.
 injection=injection.replace('<base href="'+pub.URL.replace('preview/v0.7.3/','')+'">','<base href="__ARCHIVE_ROOT__">')
 return '<!doctype html><meta charset="utf-8"><title>九州修仙錄 '+v+' 保留版</title><p id="loading">正在載入 '+v+' 保留版…</p><script>(async()=>{const r=await fetch("source.html.gz"),raw=await r.arrayBuffer();let bytes=new Uint8Array(raw);if(bytes[0]===31&&bytes[1]===139)bytes=new Uint8Array(await new Response(new Blob([bytes]).stream().pipeThrough(new DecompressionStream("gzip"))).arrayBuffer());const digest=[...new Uint8Array(await crypto.subtle.digest("SHA-256",bytes))].map(v=>v.toString(16).padStart(2,"0")).join("");if(digest!=="'+sha+'")throw Error("版本檔案核對未通過");const root=new URL("../../",location.href).href,inject='+jsdump(injection)+'.replace("__ARCHIVE_ROOT__",root),source=new TextDecoder().decode(bytes).replace("<head>","<head>"+inject);document.open();document.write(source);document.close();})().catch(e=>document.getElementById("loading").textContent="載入未完成："+e.message);</script>'
def prepare():
 O.mkdir(exist_ok=True)
 for f,old in json.loads((P/'baseline.json').read_text('utf8'))['protected'].items():assert pub.digest(R/f)==old['sha256'],f
 assert not pub.git(pub.W,'status','--porcelain');assert not pub.git(T,'status','--porcelain')
 records=[]
 for name in TESTS:
  d=json.loads((QA/name).read_text('utf8'));assert not d['errors'] and all(r['pass'] for r in d['rows']),name;records+=d['rows'];shutil.copy2(QA/name,O/name)
 assert len(records)==40
 state={'build':BUILD,'version':'0.7.3','formalUpdated':True,'authorization':'2026-10-19玩家明確同意升正式0.7.3，並保留0.7.0／0.7.1／0.7.2；圖鑑與主線已由玩家驗收通過。','url':pub.URL.replace('preview/v0.7.3/','')+'?build='+BUILD,'base':pub.git(pub.W,'rev-parse','HEAD'),'oldRules':{n:pub.git(pub.W,'rev-parse','HEAD:'+n) for n in ['定案規則_0.7.0.json','定案規則_0.7.1.json','定案規則_0.7.2.json']},'newTests':len(records)}
 for folder in [T,D]:
  f=folder/'index.html';s=f.read_text('utf8');old={m[1]:hashlib.sha256(m[2].encode()).hexdigest() for m in re.finditer(r'<script id="jz073-([^"<>]+)">(.*?)</script>',s,re.S)}
  for name in MODULES:
   assert 'id="jz073-'+name+'"' not in s
   code=(P/(name+'.js')).read_text('utf8').replace('/郵箱背包美術_2026-10-19/','inventory-assets/')
   s+='\n<script id="jz073-'+name+'">'+code+'</script>'
  s,n=re.subn(r'window.JZ073_BUILD_ID="[^"]+";',lambda m:'window.JZ073_BUILD_ID='+json.dumps(BUILD)+';',s);assert n==1
  after={m[1]:hashlib.sha256(m[2].encode()).hexdigest() for m in re.finditer(r'<script id="jz073-([^"<>]+)">(.*?)</script>',s,re.S)};assert all(after[k]==v for k,v in old.items());f.write_text(s,'utf8')
  dest=folder/'inventory-assets';dest.mkdir(exist_ok=True)
  for asset in A.iterdir():
   if folder==T or asset.suffix!='.png':shutil.copy2(asset,dest/asset.name)
 for folder in [T/'test-source/v073',D/'test-source/v073',D/'施工來源',O/'施工來源']:
  folder.mkdir(parents=True,exist_ok=True)
  for name in FILES:shutil.copy2(P/name,folder/name)
 # Preserve the exact previous production blobs; only the small loader adds
 # archive-specific storage isolation. Gzip decoding does not change the source.
 versions=[]
 for v,ref in OLD.items():
  raw=blob(ref,'index.html');sha=hashlib.sha256(raw).hexdigest();folder=pub.W/'versions'/v;folder.mkdir(parents=True,exist_ok=True);(folder/'source.html.gz').write_bytes(gzip.compress(raw,mtime=0));(folder/'index.html').write_text(legacy_page(v,sha),'utf8');versions.append({'version':v,'commit':pub.git(pub.W,'rev-parse',ref),'sha256':sha,'bytes':len(raw),'gzipBytes':(folder/'source.html.gz').stat().st_size,'url':state['url'].split('?')[0]+'versions/'+v+'/'})
  local=O/'歷史版本'/v;local.mkdir(parents=True,exist_ok=True);(local/'原版.html').write_bytes(raw);shutil.copy2(folder/'source.html.gz',local/'source.html.gz')
 state['retainedVersions']=versions
 (pub.W/'versions/index.html').write_text('<!doctype html><meta charset="utf-8"><title>九州修仙錄・歷史版本</title><style>body{max-width:800px;margin:50px auto;background:#09141d;color:#dce8ee;font:18px/1.9 sans-serif}a{color:#edcd78}section{padding:20px;border:1px solid #456073;margin:20px 0}</style><h1>九州修仙錄・歷史版本</h1><p><a href="../">目前正式版0.7.3</a></p><p>保留各版最後發布內容。舊版使用自己的存檔副本，避免覆寫新版進度。</p>'+''.join('<section><a href="'+v+'/">開啟 '+v+' 保留版</a></section>' for v in OLD),'utf8')
 (pub.W/'versions/版本保留核對.json').write_text(json.dumps(versions,ensure_ascii=False,indent=2),'utf8')
 root=official((D/'index.html').read_text('utf8'));(pub.W/'index.html').write_text(root,'utf8')
 source=T/'official073';source.mkdir(exist_ok=True);(source/'index.html').write_text(root,'utf8')
 local=(P/'preview.html').read_text('utf8')
 for prefix in ['/github-release/assets/','/新增美術_2026-10-16/','/素材美術_2026-10-18/','/物品美術_2026-10-18/','/人物全身_2026-10-18/','/物品獨立美術_2026-10-18/','/物品修正美術_2026-10-19/','/長右血條正式美術_2026-10-19/','/修正24美術_2026-10-19/','/郵箱背包美術_2026-10-19/']:local=local.replace(prefix,'.'+prefix)
 local=official(local).replace('<base href="preview/v0.7.3/">','');local+='<script>window.JZ073_BUILD_ID='+json.dumps(BUILD)+';</script>';(R/'九州修仙錄_正式母檔_0.7.3.html').write_text(local,'utf8');(O/'九州修仙錄_V0.7.3_正式版.html').write_text('<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=../九州修仙錄_正式母檔_0.7.3.html"><a href="../九州修仙錄_正式母檔_0.7.3.html">開啟0.7.3正式版</a>','utf8')
 rules={'meta':{'version':'0.7.3','date':'2026-10-19','phase':'正式版','base':'定案規則_0.7.2.json','priority':'沿用0.7.2與已驗收0.7.3測試分支；本輪使用者最新確認規則優先。舊版內容只保留作歷史，不回蓋新版。','authorization':state['authorization']},'accepted':['圖鑑','A／B主線','既有0.7.3測試分支已實裝與驗收功能'],'experience':{'visibleCap':100,'hiddenCap':20,'spendStep':10,'chancePerStep':1,'mainQuest':1,'sideQuest':1,'commissionsPerPoint':5,'teaCap':7,'firstTea':1,'firstEnlightenmentTeaExtra':3,'monsterKillsPerPoint':{'一般種':30,'特殊種':20,'高位種':10,'高危種（特）':5},'monsterDirect':{'妖王種':1,'神獸種':5,'災獸種':5},'humanDirect':{'長老級':5,'道祖級':5,'州府統領':3},'gathersPerPoint':30,'wildMinutesPerPoint':1440,'travelExcluded':True,'npcHeart':{'5':1,'10':2},'petHeart':{'5':1,'10':2},'petFirst5Stars':3,'souvenirFirstEach':1,'moonJadeFirst':5,'token':3},'inventory':{'initialSlots':{'物品':50,'材料':50,'裝備':30,'永久特殊':30,'消耗特殊':30},'unlimited':['紀念品','禮物','任務'],'stackByName':True,'expansionItem':'［特殊］背包擴充格','expansionStep':3,'expansionUpperCap':None},'mail':{'position':'幫助左側','maxLetters':10,'expiresAfterGameDays':7,'deleteOnlyWhenEmpty':True,'important':['［任務］物品','［特殊］物品','裝備'],'importantDoesNotExpireWhileUnclaimed':True,'fullOrdinary':'拒收並提示','fullImportant':'另外保留','pioneer':{'existingCharactersOnly':True,'once':True,'text':'我是a03697ss1，感謝各位當測試員並遊玩我的遊戲，在此準備禮物給你們這些先驅者。','items':[['抽獎卷',10],['［特殊］改名卡',1]],'coins':5000}},'retainedVersions':versions,'sourceModules':[{'name':n+'.js','sha256':pub.digest(P/(n+'.js'))} for n in MODULES],'notInvented':['抽獎池與抽獎功能未設計；票券先保留。','背包擴充格未指定取得來源，不新增商店、配方或掉落。','其餘七種新狀態無正式施加來源，保留接口與說明。','金丹玩家成長未開放，築基圓滿停止突破。']}
 (pub.W/'定案規則_0.7.3.json').write_text(json.dumps(rules,ensure_ascii=False,indent=2),'utf8');(R/'最新定案母檔_0.7.3.json').write_text(json.dumps({'inherits':'最新定案母檔_0.7.2.json','official073':rules},ensure_ascii=False,indent=2),'utf8');shutil.copy2(pub.W/'定案規則_0.7.3.json',source/'定案規則_0.7.3.json')
 body='<h1>九州修仙錄0.7.3・正式發布與驗收</h1><p><a href="../../../?build='+BUILD+'">開始遊玩0.7.3</a> · <a href="../../../versions/">0.7.0／0.7.1／0.7.2保留版</a></p><p>圖鑑與主線經玩家驗收通過，並獲明確授權升為正式版。既有已完成內容增量保留。本次新增40項驗收通過；舊版三份規則不變，三個可遊玩版本保留原始程式雜湊。</p><h2>新增</h2><p>背包50／50／30／30／30初始容量與固定格，擴充格一次增加指定分頁3格；郵箱10封、7遊戲日到期、重要道具保管；舊角色先驅者感謝信，抽獎卷10、改名卡1、靈幣5000。</p><h2>改動</h2><p>全部歷練來源採本輪規則，保留100＋20池、整10點投入；每種紀念品首次1、月玉珮5。蘇璃、蘇項及未來可結婚夥伴共用專屬背景規則。背包、功法及全部製作類型採固定格；細節區可捲動，操作保留。</p><h2>BUG修復</h2><p>紀念品漏發歷練；月玉珮合成漏查紀念品欄；品茗7點上限誤計為角色總歷練；多敵歷練漏算；幫助切換回頂與冒險日誌遮擋。前輪24項修正中的第3項已補完，其餘保留。</p><h2>逐項工程覆蓋表與測試</h2><table><tr><th>項目</th><th>結果與程式位置</th><th>證據</th></tr>'
 coverage=[('歷練與紀念品','已完成；experience1019.js。領取、合成、存讀檔、溢出上限、茶館、任務、好感、孵化與升星。',TESTS[0]),('戰鬥歷練','已完成；experience1019.js。A線真實三隻青臭蟲退出與逐隻計數；種類／大境界限制及防重複。',TESTS[1]),('夥伴背景','已完成；partner-background1019.js。蘇璃、蘇項隊伍與夥伴管理圖片實載，後續可結婚對象自動套用。',TESTS[0]),('背包容量、固定格、擴充與郵箱','已完成；inventory-mail1019.js／inventory-layout1019.js。滿50格、擴充3格、滿10封、7日到期、重要道具、獎勵與存讀檔。',TESTS[2]),('正常取得流程','已完成；inventory-mail1019.js。真實野外戰鬥、公共煉製、NPC收禮均可觸發寄存。',TESTS[3]),('幫助捲動','已完成；help-scroll1019.js。切換保持側欄位置，回到舊條目恢復內文位置。',TESTS[2])]
 for title,result,evidence in coverage:body+='<tr><td>'+title+'</td><td>'+result+'</td><td><a href="10-19F_'+evidence+'">驗收紀錄</a></td></tr>'
 body+='</table><h2>存檔與舊版本</h2><p>正式0.7.3延續現有0.7.3測試存檔。若沒有0.7.3自動存檔，會以副本帶入原版自動存檔；原版手動槽與原始資料保留，也可從存檔管理讀取舊紀錄。紀念品以目前持有、NPC領取紀錄、已完成合成及首通證據補發一次；舊主支線、好感與升星既有門檻不重播，避免無法確認歷史發放時重複獎勵。</p><p>0.7.0／0.7.1／0.7.2保留原始發布程式，另加獨立存檔副本入口。壓縮只用於傳輸，載入後核對原始SHA-256，不更換程式內容。</p><h2>待後續設定</h2><ul>'+''.join('<li>'+html.escape(x)+'</li>' for x in rules['notInvented'])+'</ul><h2>素材與生圖提示詞</h2><p>使用內建image_gen；4張1254×1254透明圖，原生解析度、可見RGB與透明度無損WebP。</p><p><a href="inventory-assets/生圖提示詞與素材清單.json">最終提示詞與來源清單</a> · <a href="inventory-assets/無損圖片驗證.json">無損核對</a></p><ul>'+''.join('<li><a href="inventory-assets/'+n+'.webp">'+n+'</a></li>' for n in ['背包擴充格','抽獎卷','改名卡','靈幣'])+'</ul><h2>實際畫面</h2>'
 # Lossless screenshots are small; the full originals remain in the workspace.
 for n in ['先驅者感謝信與靈幣圖片','材料背包固定格與擴充','幫助切頁保留捲動']:
  f=QA/(n+'.webp')
  if f.exists():shutil.copy2(f,D/('10-19F_'+f.name));body+='<p>'+n+'</p><img style="max-width:100%" src="10-19F_'+f.name+'">'
 report='<!doctype html><meta charset="utf-8"><title>0.7.3正式發布與驗收</title><style>body{max-width:1200px;margin:32px auto;padding:20px;background:#0b1720;color:#deebef;font:16px/1.8 sans-serif}a{color:#f1cf7c}h1,h2{color:#efd6a6}table{border-collapse:collapse;width:100%}td,th{padding:12px;border:1px solid #3a5265;text-align:left}img{border:1px solid #3a5265;border-radius:10px}</style>'+body
 (D/'10-19F_正式發布與驗收報告.html').write_text(report,'utf8');(O/'正式發布與驗收報告.html').write_text(report.replace('../../../?build=',state['url'].split('?')[0]+'?build=').replace('../../../versions/',state['url'].split('?')[0]+'versions/').replace('10-19F_','').replace('inventory-assets/','../郵箱背包美術_2026-10-19/'),'utf8')
 for n in TESTS:shutil.copy2(QA/n,D/('10-19F_'+n))
 (O/'逐項施工覆蓋表.json').write_text(json.dumps({'build':BUILD,'version':'0.7.3','formal':True,'previous24Completed':24,'rows':[{'title':t,'result':r,'evidence':e} for t,r,e in coverage],'pending':rules['notInvented']},ensure_ascii=False,indent=2),'utf8')
 shutil.copy2(O/'逐項施工覆蓋表.json',D/'10-19F_逐項施工覆蓋表.json')
 # Resolve the previous missing-value entry instead of leaving the latest table stale.
 f=D/'10-19E_逐項施工覆蓋表.json';d=json.loads(f.read_text('utf8'));d['completed']=24;d['pending']=0
 for row in d['rows']:
  if row['id']==3:row.update(status='已實裝／驗證通過',result='每種紀念品首次＋1、月玉珮＋5；持有／領取證據補發一次，存讀檔防重複。',code='experience1019.js',evidence=TESTS[:2])
 f.write_text(json.dumps(d,ensure_ascii=False,indent=2),'utf8')
 (pub.W/'README.md').write_text('# 九州修仙錄 0.7.3\n\n正式遊玩：https://a03697ss1.github.io/jiuzhou-rpg/\n\n更新／驗收：'+pub.URL+'10-19F_正式發布與驗收報告.html\n\n歷史版本：https://a03697ss1.github.io/jiuzhou-rpg/versions/\n\n新增：長右與新地區、A／B主線、三寵、圖鑑、背包容量及郵箱。改動：修為靈幣、歷練、裝備及固定格。BUG修復：戰鬥退出、0氣血、圖鑑搜尋、幫助捲動、月玉珮合成與紀念品歷練。\n\n0.7.3延續測試存檔；無測試存檔時以副本帶入原版自動存檔。原版手動槽保留。0.7.0、0.7.1、0.7.2原始發布程式與規則保留，各有獨立存檔副本入口。\n\n抽獎尚未開放，票券先保留。背包擴充格未指定取得來源，不增設來源。音樂暫停。\n','utf8')
 f=D/'閱讀我_先看這裡.html';s=f.read_text('utf8');s=s.replace('</h1>','</h1><section><h2>0.7.3已升正式版</h2><p>圖鑑、主線經玩家驗收。<a href="../../../">正式遊玩</a> · <a href="10-19F_正式發布與驗收報告.html">分類更新與完整驗收</a> · <a href="../../../versions/">舊版保留入口</a></p></section>',1);f.write_text(s,'utf8')
 state['siteBytes']=sum(f.stat().st_size for f in pub.W.rglob('*') if f.is_file() and '.git' not in f.parts);state['rootSha256']=pub.digest(pub.W/'index.html');STATE.write_text(json.dumps(state,ensure_ascii=False,indent=2),'utf8');print(json.dumps(state,ensure_ascii=False))
def commit():
 state=json.loads(STATE.read_text('utf8'));assert state['siteBytes']<1073741824
 for n,v in state['oldRules'].items():assert pub.git(pub.W,'hash-object',n)==v
 pub.git(T,'add','--','index.html','test-source/v073','inventory-assets','official073');pub.git(T,'commit','-m','Complete experience inventory mailbox layouts and official 0.7.3 candidate after player acceptance');state['sourceCommit']=pub.git(T,'rev-parse','HEAD')
 pub.git(pub.W,'add','--','index.html','README.md','定案規則_0.7.3.json','versions',pub.PREFIX)
 allowed=lambda n:n in ['index.html','README.md','定案規則_0.7.3.json'] or n.startswith('versions/') or n.startswith(pub.PREFIX+'/')
 assert all(allowed(n) for n in pub.git(pub.W,'diff','--cached','--name-only','-z').split('\0') if n)
 pub.git(pub.W,'commit','-m','Release official 0.7.3 with inventory mailbox and experience fixes; preserve playable 0.7.0 0.7.1 0.7.2');state['deploymentCommit']=pub.git(pub.W,'rev-parse','HEAD');STATE.write_text(json.dumps(state,ensure_ascii=False,indent=2),'utf8');(O/'GitHub正式發布紀錄.json').write_text(json.dumps(state,ensure_ascii=False,indent=2),'utf8');print(json.dumps(state,ensure_ascii=False))
def publish():
 state=json.loads(STATE.read_text('utf8'));pub.git(T,'push','origin','HEAD:refs/heads/test/v0.7.3-20261017');pub.git(pub.W,'push','origin','HEAD:refs/heads/main');state['publishedAt']=datetime.datetime.now().astimezone().isoformat(timespec='seconds');STATE.write_text(json.dumps(state,ensure_ascii=False,indent=2),'utf8');(O/'GitHub正式發布紀錄.json').write_text(json.dumps(state,ensure_ascii=False,indent=2),'utf8');print(json.dumps(state,ensure_ascii=False))
if __name__=='__main__':{'prepare':prepare,'commit':commit,'publish':publish}[sys.argv[1]]()
