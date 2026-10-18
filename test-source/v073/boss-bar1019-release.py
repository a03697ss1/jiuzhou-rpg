from pathlib import Path
import importlib.util,json,shutil,html,re,sys,datetime,urllib.parse,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'V0.7.3_長右血條實裝_2026-10-19';A=R/'長右血條正式美術_2026-10-19';BUILD='20261019-bossbar-1'
spec=importlib.util.spec_from_file_location('pub',P/'publish-preview.py');pub=importlib.util.module_from_spec(spec);spec.loader.exec_module(pub)
T=R/'V0.7.3_獨立測試_2026-10-17/Git測試分支';D=pub.DEST;STATE=P/'boss-bar1019-release-state.json'
FILES=['boss-bar1019.js','boss-bar1019-test.cjs','boss-bar1019-combat.cjs','boss-bar1019-release.py','boss-bar1019-verify.py','build.py']
def prepare():
 tests=[]
 for n in ['雙階段血條實際驗收.json','長右與黑衣人勝敗退出驗收.json']:
  d=json.loads((O/n).read_text('utf8'));assert all(x['pass'] for x in d['rows']) and not d['errors'];tests+=d['rows']
 assert len(tests)==9
 for name,old in json.loads((P/'baseline.json').read_text('utf8'))['protected'].items():assert pub.digest(R/name)==old['sha256'],name
 assert not pub.git(pub.W,'diff','--name-only')
 state={'build':BUILD,'url':pub.URL+'?build='+BUILD,'base':pub.git(pub.W,'rev-parse','HEAD'),'formalUpdated':False,'bossDesignImplemented':True,'protectedBlobs':{n:pub.git(pub.W,'rev-parse','HEAD:'+n) for n in ['index.html','定案規則_0.7.2.json']}}
 for folder in [T,D]:
  f=folder/'index.html';s=f.read_text('utf8');old={m[1]:hashlib.sha256(m[2].encode()).hexdigest() for m in re.finditer(r'<script id="jz073-([^"<>]+)">(.*?)</script>',s,re.S)}
  code=(P/'boss-bar1019.js').read_text('utf8').replace('/長右血條正式美術_2026-10-19/','boss-bar-assets/');s+='\n<script id="jz073-boss-bar1019">'+code+'</script>'
  s,n=re.subn(r'window.JZ073_BUILD_ID="[^"]+";',lambda m:'window.JZ073_BUILD_ID='+json.dumps(BUILD)+';',s);assert n==1
  after={m[1]:hashlib.sha256(m[2].encode()).hexdigest() for m in re.finditer(r'<script id="jz073-([^"<>]+)">(.*?)</script>',s,re.S)};assert all(after[k]==v for k,v in old.items());f.write_text(s,'utf8')
  dest=folder/'boss-bar-assets';dest.mkdir(exist_ok=True)
  for asset in A.iterdir():
   if folder==T or asset.suffix!='.png':shutil.copy2(asset,dest/asset.name)
 # Historical screenshots stay available in the source test branch; archive only preview copies.
 archive=T/'qa-archive/20261019';archive.mkdir(parents=True,exist_ok=True);mapping={}
 for name in ['10-19B_長右專屬血條與小型戰位.webp','999重複長右入口.webp','10-19B_長右第二階段專屬血條.webp','10-19B_BOSS與三隻隨從排版驗收.webp','B線九珠陰雷戰鬥畫面.webp','長右回歸驗收.webp']:
  f=D/name;assert f.resolve().parent==D.resolve();shutil.copy2(f,archive/name);assert pub.digest(f)==pub.digest(archive/name)
  url='https://raw.githubusercontent.com/a03697ss1/jiuzhou-rpg/test/v0.7.3-20261017/qa-archive/20261019/'+urllib.parse.quote(name);mapping[name]=url
  for report in D.iterdir():
   if report.suffix in ['.html','.json']:
    s=report.read_text('utf8');s=s.replace(name,url);report.write_text(s,'utf8')
  f.unlink()
 state['historicalScreenshotArchive']=mapping
 for folder in [T/'test-source/v073',D/'test-source/v073',D/'施工來源',O/'施工來源']:
  folder.mkdir(parents=True,exist_ok=True)
  for name in FILES:shutil.copy2(P/name,folder/name)
 local=(P/'preview.html').read_text('utf8')
 for prefix in ['/github-release/assets/','/新增美術_2026-10-16/','/素材美術_2026-10-18/','/物品美術_2026-10-18/','/人物全身_2026-10-18/','/物品獨立美術_2026-10-18/','/物品修正美術_2026-10-19/','/長右血條正式美術_2026-10-19/']:local=local.replace(prefix,'..'+prefix)
 (O/'九州修仙錄_V0.7.3_獨立測試版.html').write_text(local+'<script>window.JZ073_BUILD_ID='+json.dumps(BUILD)+';</script>','utf8')
 coverage={'build':BUILD,'status':'已實裝並完成測試','approvedByUser':True,'changes':['四耳猿首、封印鎖鏈的第一階段專屬血條','第二階段確實切換斷鏈、破碎封印、水雷圖片','即時氣血數字與比例、階段及屬性同步','預載兩套圖片，保留小型我方戰位與敵方隨從空間'],'tests':len(tests),'formalUpdated':False,'mechanicsChanged':False,'remainingBlockers':[],'code':'boss-bar1019.js','assetFolder':'boss-bar-assets/','testCode':['boss-bar1019-test.cjs','boss-bar1019-combat.cjs'],'normalFlowEvidence':'使用正式手動普攻、點選長右、跨階段後勝利；失敗結算與A線黑衣人正常勝利均通過。','artTool':'built-in image_gen','artPrompts':'boss-bar-assets/生成提示詞.json'}
 (O/'施工覆蓋與驗收.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2),'utf8')
 body='<h1>V0.7.3 長右雙階段專屬血條</h1><p><a href="index.html?build='+BUILD+'">開啟測試遊戲</a> · '+BUILD+'</p><p>依玩家確認的設計實裝四耳猿首、古銅封印與鎖鏈。氣血到達既有第二階段門檻時，整套切換為破碎封印、水流與雷光圖片，血條由紅轉為水雷藍紫。名稱、階段、血量數字與填滿比例均由戰鬥資料即時產生。</p><p>沿用原本階段與傷害規則；保留禁止自動、小型全身我方戰位、隨從預留區、全畫面第二階段提示及勝敗退出修正。正式母檔與正式發布內容未修改。</p><h2>測試與驗收</h2><ul>'+''.join('<li>'+html.escape(x['name'])+'：通過</li>' for x in tests)+'</ul><p>九項均通過，無瀏覽器程式錯誤。三隻隨從僅作排版測試，沒有新增正式長右小怪或掉落。</p><h2>BUG修復與待補</h2><p>完成長右血條美術與第二階段實際換圖。本項無待補。既有主線勝利關閉戰鬥畫面的修正保留。</p><p><a href="10-19D_雙階段血條實際驗收.json">血條驗收資料</a> · <a href="10-19D_長右與黑衣人勝敗退出驗收.json">實際戰鬥驗收</a> · <a href="施工來源/boss-bar1019.js">程式位置</a> · <a href="boss-bar-assets/生成提示詞.json">內建生圖工具提示詞與來源</a> · <a href="boss-bar-assets/圖片無損驗證.json">透明度與無損編碼驗證</a></p>'
 for n in ['長右第一階段實裝','長右第二階段實裝','長右與三隻隨從排版']:
  shutil.copy2(O/(n+'.webp'),D/('10-19D_'+n+'.webp'));body+='<h2>'+n+'</h2><img src="10-19D_'+n+'.webp" loading="lazy">'
 report='<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>長右雙階段專屬血條驗收</title><style>body{max-width:1400px;margin:30px auto;padding:0 24px;background:#091820;color:#dcebef;font:16px/1.9 Microsoft JhengHei}h1,h2{color:#eed5a0}a{color:#f1cf83}img{max-width:100%;border:1px solid #486476}</style>'+body+'</html>'
 (D/'10-19D_長右雙階段血條驗收報告.html').write_text(report,'utf8');(O/'長右雙階段血條驗收報告.html').write_text(report.replace('index.html?build=','九州修仙錄_V0.7.3_獨立測試版.html?build=').replace('10-19D_','').replace('boss-bar-assets/','../長右血條正式美術_2026-10-19/'),'utf8')
 for n in ['雙階段血條實際驗收.json','長右與黑衣人勝敗退出驗收.json','施工覆蓋與驗收.json']:shutil.copy2(O/n,D/('10-19D_'+n))
 f=D/'本輪交付清單.json';d=json.loads(f.read_text('utf8'));d.update(build=BUILD,bossBarApprovedImplementation=coverage);f.write_text(json.dumps(d,ensure_ascii=False,indent=2),'utf8')
 f=D/'閱讀我_先看這裡.html';s=f.read_text('utf8').replace('新長右血條仍待設計確認，未套用。','長右新血條已於玩家確認後實裝，包含第二階段換圖。');note='<section id="bossbar19"><h2>10/19 長右雙階段專屬血條</h2><p>玩家確認設計已實裝。第二階段確實更換水雷、斷鏈與破碎封印圖片。</p><a href="10-19D_長右雙階段血條驗收報告.html">本次驗收</a> · <a href="index.html?build='+BUILD+'">最新遊戲</a></section>';s=s.replace('</h1>','</h1>'+note,1);f.write_text(s,'utf8')
 f=R/'長右專屬血條_設計預覽_2026-10-19/設計提示詞與狀態.json';d=json.loads(f.read_text('utf8'));d.update(approved=True,implemented=True,build=BUILD,implementationReport=str(O/'長右雙階段血條驗收報告.html'));f.write_text(json.dumps(d,ensure_ascii=False,indent=2),'utf8')
 state['siteBytes']=sum(f.stat().st_size for f in pub.W.rglob('*') if f.is_file() and '.git' not in f.parts);assert state['siteBytes']<1073741824,state['siteBytes']
 pub.git(T,'add','--','index.html','test-source/v073','boss-bar-assets','qa-archive');pub.git(T,'commit','-m','Implement approved Changyou four-ear boss bar and phase-two art switching')
 state['sourceCommit']=pub.git(T,'rev-parse','HEAD');STATE.write_text(json.dumps(state,ensure_ascii=False,indent=2),'utf8');print(json.dumps(state,ensure_ascii=False))
def publish():
 state=json.loads(STATE.read_text('utf8'));pub.git(T,'push','origin','HEAD:refs/heads/test/v0.7.3-20261017');pub.git(pub.W,'add','--',pub.PREFIX)
 assert all(n.startswith(pub.PREFIX+'/') for n in pub.git(pub.W,'diff','--cached','--name-only','-z').split('\0') if n)
 pub.git(pub.W,'commit','-m','Publish approved Changyou dual-phase painted boss health bar to test preview')
 for n,v in state['protectedBlobs'].items():assert pub.git(pub.W,'rev-parse','HEAD:'+n)==v
 assert all(n.startswith(pub.PREFIX+'/') for n in pub.git(pub.W,'diff','--name-only','-z',state['base'],'HEAD').split('\0') if n)
 pub.git(pub.W,'push','origin','HEAD:refs/heads/main');state.update(published=True,deploymentCommit=pub.git(pub.W,'rev-parse','HEAD'),publishedAt=datetime.datetime.now().astimezone().isoformat(timespec='seconds'));(O/'GitHub測試發布紀錄.json').write_text(json.dumps(state,ensure_ascii=False,indent=2),'utf8');print(json.dumps(state,ensure_ascii=False))
if __name__=='__main__':{'prepare':prepare,'publish':publish}[sys.argv[1]]()
