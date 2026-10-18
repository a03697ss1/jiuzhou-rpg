from pathlib import Path
import importlib.util,json,html,shutil,hashlib,re,sys,datetime
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'V0.7.3_隱藏裝備修正_2026-10-19';BUILD='20261019-hidden-steal-1'
spec=importlib.util.spec_from_file_location('pub',P/'publish-preview.py');pub=importlib.util.module_from_spec(spec);spec.loader.exec_module(pub)
W=pub.W;D=pub.DEST;T=R/'V0.7.3_獨立測試_2026-10-17/Git測試分支';STATE=P/'hidden-steal1019-release-state.json'
def prepare():
 reports={}
 for file,folder in [('隱藏裝備測試結果.json',O),('18項功能驗收.json',R/'V0.7.3_18項修正_2026-10-18'),('正常介面與藥品效果驗收.json',R/'V0.7.3_18項修正_2026-10-18')]:
  data=json.loads((folder/file).read_text('utf8'));assert all(x['pass'] for x in data['rows']) and not data['errors'],file;reports[file]=data
  if folder!=O:shutil.copy2(folder/file,O/file)
 protected={}
 for name,info in json.loads((P/'baseline.json').read_text('utf8'))['protected'].items():
  sha=pub.digest(R/name);assert sha==info['sha256'];protected[name]=sha
 assert pub.git(T,'branch','--show-current')=='test/v0.7.3-20261017'
 for f in [P/'build.py',P/'hidden-steal1019.js',P/'hidden-steal1019-test.cjs',Path(__file__)]:shutil.copy2(f,T/'test-source/v073'/f.name)
 preview=(P/'preview.html').read_text('utf8')
 replacements=[('/github-release/assets/','assets/'),('/新增美術_2026-10-16/','new-assets/'),('/素材美術_2026-10-18/','material-assets/'),('/物品美術_2026-10-18/','item-assets/'),('/人物全身_2026-10-18/','fullbody-assets/'),('/物品獨立美術_2026-10-18/','unique-item-assets/')]
 source=preview
 for a,b in replacements:source=source.replace(a,b)
 (T/'index.html').write_text(source+'<script>window.JZ073_BUILD_ID='+json.dumps(BUILD)+';</script>','utf8')
 local=preview
 for a,b in replacements:local=local.replace(a,'..'+a)
 (O/'九州修仙錄_V0.7.3_獨立測試版.html').write_text(local+'<script>window.JZ073_BUILD_ID='+json.dumps(BUILD)+';</script>','utf8')
 pub.git(T,'add','--','index.html','test-source/v073')
 if pub.git(T,'diff','--cached','--name-only'):pub.git(T,'commit','-m','Implement five unique hidden NPC robbery rewards at 5 percent')
 base=pub.git(W,'rev-parse','HEAD');blobs={n:pub.git(W,'rev-parse','HEAD:'+n) for n in ['index.html','定案規則_0.7.2.json']}
 assert not pub.git(W,'diff','--name-only'), 'Unexpected publisher edits'
 text=(D/'index.html').read_text('utf8');script='<script id="jz073-hidden-steal1019">'+(P/'hidden-steal1019.js').read_text('utf8')+'</script>'
 if 'id="jz073-hidden-steal1019"' in text:text=re.sub(r'<script id="jz073-hidden-steal1019">.*?</script>',lambda m:script,text,flags=re.S)
 else:text+='\n'+script
 text,n=re.subn(r'window.JZ073_BUILD_ID="[^"]+";',lambda m:'window.JZ073_BUILD_ID='+json.dumps(BUILD)+';',text);assert n==1
 (D/'index.html').write_text(text,'utf8')
 for folder in [D/'施工來源',D/'test-source/v073',O/'施工來源']:
  folder.mkdir(parents=True,exist_ok=True)
  for f in [P/'build.py',P/'hidden-steal1019.js',P/'hidden-steal1019-test.cjs',Path(__file__)]:shutil.copy2(f,folder/f.name)
 count=sum(len(d['rows']) for d in reports.values())
 coverage=[{'npc':n,'item':i,'chance':.05,'uniquePerGame':True,'codex':'未知來源','state':'已實裝、測試通過，待玩家驗收'} for n,i in {'林夏于':'［特殊］火霞刀','蘇璃':'［特殊］靈水劍','柳清妍':'［特殊］秘術弓','邱山河':'［特殊］鹿絞槍','蘇項':'［特殊］土靈盔'}.items()]
 result={'build':BUILD,'version':'0.7.3','testCount':count,'coverage':coverage,'protectedLocal':protected,'formalUpdated':False,'savePrefix':'jz073-independent-20261017:','note':'僅接入已確認的五件隱藏物品；未補造其他一般搶奪戰利品池。'}
 (O/'施工覆蓋與驗收.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),'utf8')
 body='<h1>10/19 特殊裝備修正驗收</h1><p>已依使用者定案，搶奪對應NPC並戰勝後有5%機率取得；每件在同一遊戲紀錄僅發放一次。圖鑑在取得前後均顯示未知來源，不公開NPC或機率。</p><table><tr><th>NPC</th><th>裝備</th><th>狀態</th></tr>'+''.join('<tr><td>'+r['npc']+'</td><td>'+r['item']+'</td><td>'+r['state']+'</td></tr>' for r in coverage)+'</table><p>已穿戴、放在背包或交給夥伴的現有裝備也會登記為已取得；首次取得後即使移除物品，仍不會再次發放。未命中時，後續合法搶奪勝利可繼續抽取。一般搶奪冷卻與敵對代價沿用原規則。</p>'
 for file,data in reports.items():body+='<h2>'+html.escape(file[:-5])+'</h2><ul>'+''.join('<li>通過：'+html.escape(row['name'])+'</li>' for row in data['rows'])+'</ul>'
 body+='<p>共'+str(count)+'項檢查通過。五名NPC均透過確認搶奪、實際戰鬥及勝利結算驗證；邊界測試另外控制隨機數。正式母檔與正式入口未更動。</p>'
 report='<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><title>特殊裝備修正驗收</title><style>body{background:#091923;color:#deebef;font:16px/1.9 Microsoft JhengHei;padding:30px;max-width:1200px;margin:auto}h1,h2{color:#edd194}td,th{border:1px solid #456375;padding:10px}table{border-collapse:collapse;width:100%}a{color:#f2cf7c}</style>'+body+'</html>'
 (O/'完整施工與驗收報告.html').write_text(report,'utf8')
 for name in ['隱藏裝備測試結果.json','18項功能驗收.json','正常介面與藥品效果驗收.json','施工覆蓋與驗收.json','完整施工與驗收報告.html']:shutil.copy2(O/name,D/('10-19_'+name))
 readme=D/'閱讀我_先看這裡.html';s=readme.read_text('utf8');note='<section id="hidden1019"><h2>10/19 修正</h2><p>修復部分特殊裝備取得結算及重複發放。圖鑑取得來源仍保留未知。</p><p><a href="10-19_完整施工與驗收報告.html">本次施工與驗收報告</a></p></section>'
 if 'id="hidden1019"' in s:s=re.sub(r'<section id="hidden1019">.*?</section>',lambda m:note,s,flags=re.S)
 else:s=s.replace('</h1>','</h1>'+note,1)
 readme.write_text(s,'utf8')
 manifest=D/'本輪交付清單.json';m=json.loads(manifest.read_text('utf-8-sig'));m.update(build=BUILD,supplement={'date':'2026-10-19','tested':count,'formalUpdated':False});manifest.write_text(json.dumps(m,ensure_ascii=False,indent=2),'utf8')
 state={'base':base,'protectedBlobs':blobs,'build':BUILD,'sourceCommit':pub.git(T,'rev-parse','HEAD'),'url':pub.URL+'?build='+BUILD,'prepared':True,'formalUpdated':False};STATE.write_text(json.dumps(state,ensure_ascii=False,indent=2),'utf8');print(json.dumps(state,ensure_ascii=False))
def publish():
 state=json.loads(STATE.read_text('utf8'));pub.git(T,'push','origin','HEAD:refs/heads/test/v0.7.3-20261017')
 pub.git(W,'add','--',pub.PREFIX);changed=pub.git(W,'diff','--cached','--name-only','-z').split('\0');assert all(n.startswith(pub.PREFIX+'/') for n in changed if n)
 pub.git(W,'commit','-m','Fix unique hidden equipment rewards after successful NPC robbery')
 for n,blob in state['protectedBlobs'].items():assert pub.git(W,'rev-parse','HEAD:'+n)==blob
 assert all(n.startswith(pub.PREFIX+'/') for n in pub.git(W,'diff','--name-only','-z',state['base'],'HEAD').split('\0') if n)
 pub.git(W,'push','origin','HEAD:refs/heads/main')
 state.update(published=True,deploymentCommit=pub.git(W,'rev-parse','HEAD'),publishedAt=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(timespec='seconds'));(O/'GitHub測試發布紀錄.json').write_text(json.dumps(state,ensure_ascii=False,indent=2),'utf8');print(json.dumps(state,ensure_ascii=False))
if __name__=='__main__':{'prepare':prepare,'publish':publish}[sys.argv[1]]()
