from pathlib import Path
import importlib.util,json,html,shutil,re,sys,datetime,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'V0.7.3_物品與收禮修正_2026-10-19';BUILD='20261019-items-battle-1'
spec=importlib.util.spec_from_file_location('pub',P/'publish-preview.py');pub=importlib.util.module_from_spec(spec);spec.loader.exec_module(pub)
W=pub.W;D=pub.DEST;T=R/'V0.7.3_獨立測試_2026-10-17/Git測試分支';STATE=P/'items1019-release-state.json'
MODULES=['items1019','boss1019','battle1019'];ART=R/'物品修正美術_2026-10-19'
FILES=['build.py',*[m+'.js' for m in MODULES],'items1019-test.cjs','items1019-save.cjs','battle1019-story-test.cjs','battle1019-boss-test.cjs','battle1019-stress.cjs','items1019-art.cjs','items1019-art-manifest.json','review18-qa.cjs','items1019-release.py']

def check_reports():
 reports={}
 for f,folder in [('物品與介面實際驗收.json',O),('主線連續戰鬥退出驗收.json',O),('長右與黑衣人勝敗退出驗收.json',O),('連續野外戰鬥診斷.json',O),('隱藏裝備測試結果.json',R/'V0.7.3_隱藏裝備修正_2026-10-19'),('18項功能驗收.json',R/'V0.7.3_18項修正_2026-10-18'),('正常介面與藥品效果驗收.json',R/'V0.7.3_18項修正_2026-10-18')]:
  d=json.loads((folder/f).read_text('utf8'));assert d['rows'] and all(r['pass'] for r in d['rows']) and not d['errors'],f
  reports[f]=d
  if folder!=O:shutil.copy2(folder/f,O/f)
 assert json.loads((O/'功法遷移存讀檔驗收.json').read_text('utf8'))['pass']
 art=json.loads((O/'圖片檔案與無損驗證.json').read_text('utf8'));assert len(art)==8 and all(r['alphaPreserved'] and r['visibleRGBPreserved'] for r in art)
 return reports,art

def prepare():
 reports,art=check_reports();protected={}
 for name,record in json.loads((P/'baseline.json').read_text('utf8'))['protected'].items():
  sha=pub.digest(R/name);assert sha==record['sha256'],name;protected[name]=sha
 assert pub.git(T,'branch','--show-current')=='test/v0.7.3-20261017'
 assert not pub.git(W,'diff','--name-only'),'Unexpected publisher changes'
 base=pub.git(W,'rev-parse','HEAD');blobs={n:pub.git(W,'rev-parse','HEAD:'+n) for n in ['index.html','定案規則_0.7.2.json']}
 # Keep current production HTML and its accepted WebP mappings; append only this incremental patch.
 text=(D/'index.html').read_text('utf8')
 for module in MODULES:
  code=(P/(module+'.js')).read_text('utf8')
  if module=='items1019':code=code.replace('/物品修正美術_2026-10-19/','unique-item-assets/').replace("n+'.png'","n+'.webp?rev="+BUILD+"'")
  script='<script id="jz073-'+module+'">'+code+'</script>'
  if 'id="jz073-'+module+'"' in text:text=re.sub(r'<script id="jz073-'+module+r'">.*?</script>',lambda m:script,text,flags=re.S)
  else:text+='\n'+script
 text,n=re.subn(r'window.JZ073_BUILD_ID="[^"]+";',lambda m:'window.JZ073_BUILD_ID='+json.dumps(BUILD)+';',text);assert n==1
 (D/'index.html').write_text(text,'utf8')
 for row in art:shutil.copy2(R/row['webp'],D/'unique-item-assets'/(row['name']+'.webp'))
 preview=(P/'preview.html').read_text('utf8');source=preview;local=preview
 replacements=[('/github-release/assets/','assets/'),('/新增美術_2026-10-16/','new-assets/'),('/素材美術_2026-10-18/','material-assets/'),('/物品美術_2026-10-18/','item-assets/'),('/人物全身_2026-10-18/','fullbody-assets/'),('/物品獨立美術_2026-10-18/','unique-item-assets/'),('/物品修正美術_2026-10-19/','item-review19-assets/')]
 for a,b in replacements:source=source.replace(a,b);local=local.replace(a,'..'+a)
 (T/'index.html').write_text(source+'<script>window.JZ073_BUILD_ID='+json.dumps(BUILD)+';</script>','utf8')
 (O/'九州修仙錄_V0.7.3_獨立測試版.html').write_text(local+'<script>window.JZ073_BUILD_ID='+json.dumps(BUILD)+';</script>','utf8')
 (T/'item-review19-assets').mkdir(exist_ok=True)
 for row in art:shutil.copy2(R/row['png'],T/'item-review19-assets'/(row['name']+'.png'))
 for folder in [T/'test-source/v073',D/'test-source/v073',D/'施工來源',O/'施工來源']:
  folder.mkdir(parents=True,exist_ok=True)
  for f in FILES:shutil.copy2(P/f,folder/f)
 labels=[('1','NPC收取禮物','依後續確認，林熙沒有回禮；不新增入口。其他已定案NPC回禮入口已實測。','items1019-test.cjs'),('2','七本特殊功法','改成功法分類、書冊圖片；舊背包物品保留數量移回持有功法，原學習流程與存讀檔通過。','items1019.js'),('3','百靈藥水','原配方已為百年靈草×1＋玉葉果×1＋靈露×1；實際公共煉製成功，沒有要求或消耗一階靈草。','items1019-test.cjs')]
 named={4:'鎮岳錘',5:'逐星弓',6:'問道槍',7:'問心劍',8:'納靈葫蘆',9:'破境拳套',10:'破軍刀、玄機靈傘',12:'問靈道冠',13:'玄心道袍、問天戰衣、問道戰靴、踏虛靈履、問道戰衣'}
 for i in range(4,15):
  if i in named:labels.append((str(i),named[i],'依本次確認標示問道檯來源，不新增未定價的商品或改動庫存。','items1019.js'))
  elif i==11:labels.append(('11','忡靈四件套裝圖鑑','四件皆顯示集齊後永久解鎖忡靈術，可點選查看原功法；未新增額外套裝倍率。','items1019.js'))
  elif i==14:labels.append(('14','不滅獸甲圖片','改為獨立可穿戴的空心獸甲，不含妖物本體；所有介面共用同圖。','items1019.js'))
 labels += [('追加1','六件問道飾品','問心戒、戰心指環、破境項鍊、道心靈墜、問道佩、問天玉佩標示問道檯。','items1019.js'),('追加2','新手護符來源','標示開啟新手大禮包取得×1。','items1019.js'),('追加3','特殊裝備隱藏位階','初位、中位、高位、仙位及原能力、效果和跨位基礎能力縮放保持不變，已比對全部現有特殊裝備。','items1019-test.cjs'),('長右','專屬血條與戰位','上方專屬裝飾血條、數字內置、雙階段換色；我方四格縮小，另驗證三名敵方隨從排版空間。僅預留位置，未新增長右小怪設定。','boss1019.js'),('戰鬥','主線結算後不退出','已重現A線青臭蟲全倒、任務推進但舊戰鬥視窗仍鎖住。修正共用退出流程，保留後續對話、勝敗提示及必敗戰繼續步驟。','battle1019.js')]
 count=sum(len(d['rows']) for d in reports.values())+1;coverage=[{'id':i,'name':n,'status':'已完成／核對通過，待玩家驗收','detail':detail,'code':file} for i,n,detail,file in labels]
 manifest={'version':'0.7.3','build':BUILD,'checks':count,'imageChecks':len(art),'coverage':coverage,'protected':protected,'formalUpdated':False,'savePrefix':'jz073-independent-20261017:','remainingBlockers':[]}
 (O/'施工覆蓋與驗收.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),'utf8')
 body='<h1>V0.7.3・10/19物品與主線戰鬥修正</h1><p><a href="index.html?build='+BUILD+'">開啟本次遊戲測試版</a> · 建置 '+BUILD+'</p><p>本次共'+str(count)+'項功能與流程檢查通過，另有8張圖片的透明度與無損編碼核對。正式母檔與正式遊戲入口保持原樣。</p><h2>戰鬥卡住的原因與修正</h2><p>主線勝利已更新任務進度，但沒有關閉舊戰鬥視窗。畫面仍停在舊血量和鎖定按鈕。本次在完成結算且已離開原戰鬥後，關閉殘留戰鬥視窗；已有新對話、結果提示時保留新畫面，必敗戰仍需玩家按繼續。</p><table><tr><th>項目</th><th>內容</th><th>完成情形</th><th>位置</th></tr>'
 body+=''.join('<tr><td>'+html.escape(r['id'])+'</td><td>'+html.escape(r['name'])+'</td><td>'+html.escape(r['detail'])+'</td><td><a href="施工來源/'+r['code']+'">'+r['code']+'</a></td></tr>' for r in coverage)+'</table>'
 body+='<h2>逐項測試</h2>'
 for f,d in reports.items():body+='<details><summary>'+html.escape(f[:-5])+'：'+str(len(d['rows']))+'項通過</summary><ul>'+''.join('<li>'+html.escape(r['name'])+'</li>' for r in d['rows'])+'</ul><a href="10-19B_'+f+'">完整結果</a></details>'
 body+='<p>另通過七本特殊功法的正常存檔、重新載入與數量保留。<a href="10-19B_主線卡住重現.json">修復前重現記錄</a> · <a href="10-19B_功法遷移存讀檔驗收.json">功法存讀檔</a> · <a href="10-19B_圖片檔案與無損驗證.json">圖片核對</a> · <a href="施工來源/items1019-art-manifest.json">內建imagegen來源與提示詞</a></p><h2>八件替換美術</h2><div class="gallery">'
 body+=''.join('<figure><img loading="lazy" src="unique-item-assets/'+r['name']+'.webp?rev='+BUILD+'"><figcaption>'+html.escape(r['name'])+'</figcaption></figure>' for r in art)+'</div><h2>實際畫面</h2>'
 screenshots=['長右專屬血條與小型戰位','長右第二階段專屬血條','BOSS與三隻隨從排版驗收','長右勝利退出實際畫面']
 for name in screenshots:body+='<h3>'+name+'</h3><img class="screen" loading="lazy" src="10-19B_'+name+'.webp">'
 body+='<p>驗收使用獨立瀏覽器與測試角色，未存取玩家Chrome紀錄。流程測試提高角色能力以驗證結算，並非難度平衡驗收；BOSS隨從只做排版測試，不是新遭遇設定。</p>'
 css='body{background:#081820;color:#dcebef;font:16px/1.85 Microsoft JhengHei;margin:30px auto;padding:0 24px;max-width:1400px}h1,h2,h3{color:#ead49e}a{color:#f3cf79}table{width:100%;border-collapse:collapse}td,th{border:1px solid #405c6b;padding:10px;text-align:left;vertical-align:top}details{border:1px solid #405c6b;padding:12px;margin:12px 0}.gallery{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px}.gallery figure{margin:0;padding:12px;background:#122a36;border-radius:10px}.gallery img{width:100%;height:175px;object-fit:contain}.screen{max-width:100%;border:1px solid #546570}'
 report='<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>10/19物品與主線戰鬥修正驗收</title><style>'+css+'</style>'+body+'</html>'
 (D/'10-19B_完整施工與驗收報告.html').write_text(report,'utf8')
 localReport=report.replace('index.html?build=','九州修仙錄_V0.7.3_獨立測試版.html?build=').replace('unique-item-assets/','../物品修正美術_2026-10-19/').replace('10-19B_','')
 (O/'完整施工與驗收報告.html').write_text(localReport,'utf8')
 for name in screenshots:
  assert (O/(name+'.webp')).exists(),name;shutil.copy2(O/(name+'.webp'),D/('10-19B_'+name+'.webp'))
 for f in list(reports)+['施工覆蓋與驗收.json','主線卡住重現.json','功法遷移存讀檔驗收.json','圖片檔案與無損驗證.json']:shutil.copy2(O/f,D/('10-19B_'+f))
 readme=D/'閱讀我_先看這裡.html';s=readme.read_text('utf8');note='<section id="items1019"><h2>10/19 物品與主線戰鬥修復</h2><p>修復打完主線妖物後仍停留在戰鬥畫面；新增長右專屬血條、縮小戰位及本次物品修正。</p><p><a href="10-19B_完整施工與驗收報告.html">本次完整報告</a> · <a href="index.html?build='+BUILD+'">開啟最新測試遊戲</a></p></section>'
 if 'id="items1019"' in s:s=re.sub(r'<section id="items1019">.*?</section>',lambda m:note,s,flags=re.S)
 else:s=s.replace('</h1>','</h1>'+note,1)
 readme.write_text(s,'utf8')
 delivery=D/'本輪交付清單.json';d=json.loads(delivery.read_text('utf-8-sig'));d.update(build=BUILD,latestCorrection={'date':'2026-10-19','checks':count,'imageChecks':8,'report':'10-19B_完整施工與驗收報告.html','formalUpdated':False});delivery.write_text(json.dumps(d,ensure_ascii=False,indent=2),'utf8')
 size=sum(f.stat().st_size for f in W.rglob('*') if f.is_file() and '.git' not in f.parts);assert size<1073741824,('GitHub Pages size',size)
 pub.git(T,'add','--','index.html','test-source/v073','item-review19-assets');pub.git(T,'commit','-m','Fix main-story battle exit and special item records, add dedicated boss health UI')
 state={'base':base,'build':BUILD,'protectedBlobs':blobs,'sourceCommit':pub.git(T,'rev-parse','HEAD'),'url':pub.URL+'?build='+BUILD,'siteBytes':size,'checks':count,'formalUpdated':False,'prepared':True};STATE.write_text(json.dumps(state,ensure_ascii=False,indent=2),'utf8');print(json.dumps(state,ensure_ascii=False))

def publish():
 state=json.loads(STATE.read_text('utf8'));pub.git(T,'push','origin','HEAD:refs/heads/test/v0.7.3-20261017');pub.git(W,'add','--',pub.PREFIX)
 assert all(n.startswith(pub.PREFIX+'/') for n in pub.git(W,'diff','--cached','--name-only','-z').split('\0') if n)
 pub.git(W,'commit','-m','Publish 0.7.3 story battle exit fix, boss health UI and item corrections')
 for name,blob in state['protectedBlobs'].items():assert pub.git(W,'rev-parse','HEAD:'+name)==blob
 assert all(n.startswith(pub.PREFIX+'/') for n in pub.git(W,'diff','--name-only','-z',state['base'],'HEAD').split('\0') if n)
 pub.git(W,'push','origin','HEAD:refs/heads/main');state.update(published=True,deploymentCommit=pub.git(W,'rev-parse','HEAD'),publishedAt=datetime.datetime.now().astimezone().isoformat(timespec='seconds'));(O/'GitHub測試發布紀錄.json').write_text(json.dumps(state,ensure_ascii=False,indent=2),'utf8');print(json.dumps(state,ensure_ascii=False))

if __name__=='__main__':{'prepare':prepare,'publish':publish}[sys.argv[1]]()
