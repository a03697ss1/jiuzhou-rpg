from pathlib import Path
import importlib.util,json,shutil,html,re,sys,datetime,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'V0.7.3_裝備圖片修正_2026-10-19';BUILD='20261019-equipment-1'
spec=importlib.util.spec_from_file_location('pub',P/'publish-preview.py');pub=importlib.util.module_from_spec(spec);spec.loader.exec_module(pub)
T=R/'V0.7.3_獨立測試_2026-10-17/Git測試分支';D=pub.DEST;STATE=P/'equipment1019-release-state.json';FILES=['equipment1019.js','equipment1019-test.cjs','equipment1019-release.py','build.py']
def boss_scripts(s):return {name:hashlib.sha256(re.search(r'<script id="jz073-'+name+r'">(.*?)</script>',s,re.S)[1].encode()).hexdigest() for name in ['revision-boss1018','boss1019']}
def prepare():
 data=json.loads((O/'裝備圖片實際驗收.json').read_text('utf8'));assert len(data['rows'])==6 and all(x['pass'] for x in data['rows']) and not data['errors']
 for name,old in json.loads((P/'baseline.json').read_text('utf8'))['protected'].items():assert pub.digest(R/name)==old['sha256'],name
 assert not pub.git(pub.W,'diff','--name-only')
 state={'build':BUILD,'url':pub.URL+'?build='+BUILD,'base':pub.git(pub.W,'rev-parse','HEAD'),'formalUpdated':False,'bossDesignImplemented':False,'protectedBlobs':{n:pub.git(pub.W,'rev-parse','HEAD:'+n) for n in ['index.html','定案規則_0.7.2.json']}}
 for folder in [T,D]:
  f=folder/'index.html';s=f.read_text('utf8');before=boss_scripts(s);code='<script id="jz073-equipment1019">'+(P/'equipment1019.js').read_text('utf8')+'</script>'
  if 'id="jz073-equipment1019"' in s:s=re.sub(r'<script id="jz073-equipment1019">.*?</script>',lambda m:code,s,flags=re.S)
  else:s+='\n'+code
  s,n=re.subn(r'window.JZ073_BUILD_ID="[^"]+";',lambda m:'window.JZ073_BUILD_ID='+json.dumps(BUILD)+';',s);assert n==1
  assert before==boss_scripts(s);f.write_text(s,'utf8')
  if folder==D:state['unchangedBossScripts']=before
 for folder in [T/'test-source/v073',D/'test-source/v073',D/'施工來源',O/'施工來源']:
  folder.mkdir(parents=True,exist_ok=True)
  for f in FILES:shutil.copy2(P/f,folder/f)
 local=(P/'preview.html').read_text('utf8')
 for prefix in ['/github-release/assets/','/新增美術_2026-10-16/','/素材美術_2026-10-18/','/物品美術_2026-10-18/','/人物全身_2026-10-18/','/物品獨立美術_2026-10-18/','/物品修正美術_2026-10-19/']:local=local.replace(prefix,'..'+prefix)
 (O/'九州修仙錄_V0.7.3_獨立測試版.html').write_text(local+'<script>window.JZ073_BUILD_ID='+json.dumps(BUILD)+';</script>','utf8')
 coverage={'build':BUILD,'changes':['玩家已穿戴裝備八格圖片','夥伴已穿戴裝備與共用裝備庫圖片','角色狀態裝備圖','穿戴、卸下與品質名稱對應共用圖片'],'tests':6,'formalUpdated':False,'bossDesignImplemented':False,'bossScripts':state['unchangedBossScripts'],'bossDesignState':'新血條只有獨立設計預覽，待玩家確認後才可實裝。','images':'沿用現有物品圖片，未新增或替換裝備美術。','code':'equipment1019.js'}
 (O/'施工覆蓋與驗收.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2),'utf8')
 screenshots=['玩家裝備八格圖片','夥伴裝備圖片','角色狀態裝備圖片']
 body='<h1>V0.7.3 裝備介面圖片修正</h1><p><a href="index.html?build='+BUILD+'">開啟最新測試遊戲</a> · '+BUILD+'</p><p>補齊已穿戴裝備、夥伴共用裝備庫與角色狀態的裝備圖片。圖片沿用同件物品的現有獨立美術，數值與穿卸操作保持原樣。空格維持無裝備，不顯示假物品圖。</p><p>六項實際介面測試均通過。<a href="10-19C_裝備圖片實際驗收.json">測試結果</a> · <a href="施工來源/equipment1019.js">程式位置</a></p><ul>'+''.join('<li>'+html.escape(r['name'])+'</li>' for r in data['rows'])+'</ul><p>本次沒有套用新的長右血條。新血條另存為設計預覽，等待玩家確認；現行兩個BOSS介面模組逐字校驗一致。</p>'
 for n in screenshots:shutil.copy2(O/(n+'.webp'),D/('10-19C_'+n+'.webp'));body+='<h2>'+n+'</h2><img src="10-19C_'+n+'.webp" loading="lazy">'
 report='<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>裝備介面圖片修正驗收</title><style>body{max-width:1400px;margin:30px auto;padding:0 24px;background:#091820;color:#dcebef;font:16px/1.9 Microsoft JhengHei}h1,h2{color:#eed5a0}a{color:#f1cf83}img{max-width:100%;border:1px solid #486476}</style>'+body+'</html>'
 (D/'10-19C_裝備介面圖片修正報告.html').write_text(report,'utf8');(O/'裝備介面圖片修正報告.html').write_text(report.replace('index.html?build=','九州修仙錄_V0.7.3_獨立測試版.html?build=').replace('10-19C_',''),'utf8')
 for f in ['裝備圖片實際驗收.json','施工覆蓋與驗收.json']:shutil.copy2(O/f,D/('10-19C_'+f))
 f=D/'本輪交付清單.json';d=json.loads(f.read_text('utf8'));d.update(build=BUILD,equipmentCorrection=coverage);f.write_text(json.dumps(d,ensure_ascii=False,indent=2),'utf8')
 f=D/'閱讀我_先看這裡.html';s=f.read_text('utf8');note='<section id="equipment19"><h2>10/19 裝備介面圖片</h2><p>玩家、夥伴及角色狀態裝備圖片已補齊。新長右血條仍待設計確認，未套用。</p><a href="10-19C_裝備介面圖片修正報告.html">本次驗收</a> · <a href="index.html?build='+BUILD+'">最新遊戲</a></section>'
 if 'id="equipment19"' in s:s=re.sub(r'<section id="equipment19">.*?</section>',lambda m:note,s,flags=re.S)
 else:s=s.replace('</h1>','</h1>'+note,1)
 f.write_text(s,'utf8')
 state['siteBytes']=sum(f.stat().st_size for f in pub.W.rglob('*') if f.is_file() and '.git' not in f.parts);assert state['siteBytes']<1073741824
 pub.git(T,'add','--','index.html','test-source/v073');pub.git(T,'commit','-m','Add equipment images to worn gear and companion equipment interfaces')
 state['sourceCommit']=pub.git(T,'rev-parse','HEAD');STATE.write_text(json.dumps(state,ensure_ascii=False,indent=2),'utf8');print(json.dumps(state,ensure_ascii=False))
def publish():
 state=json.loads(STATE.read_text('utf8'));pub.git(T,'push','origin','HEAD:refs/heads/test/v0.7.3-20261017');pub.git(pub.W,'add','--',pub.PREFIX)
 assert all(n.startswith(pub.PREFIX+'/') for n in pub.git(pub.W,'diff','--cached','--name-only','-z').split('\0') if n)
 pub.git(pub.W,'commit','-m','Publish equipment interface images; keep boss bar design pending approval')
 for n,v in state['protectedBlobs'].items():assert pub.git(pub.W,'rev-parse','HEAD:'+n)==v
 assert all(n.startswith(pub.PREFIX+'/') for n in pub.git(pub.W,'diff','--name-only','-z',state['base'],'HEAD').split('\0') if n)
 pub.git(pub.W,'push','origin','HEAD:refs/heads/main');state.update(published=True,deploymentCommit=pub.git(pub.W,'rev-parse','HEAD'),publishedAt=datetime.datetime.now().astimezone().isoformat(timespec='seconds'));(O/'GitHub測試發布紀錄.json').write_text(json.dumps(state,ensure_ascii=False,indent=2),'utf8');print(json.dumps(state,ensure_ascii=False))
if __name__=='__main__':{'prepare':prepare,'publish':publish}[sys.argv[1]]()
