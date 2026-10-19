from pathlib import Path
import importlib.util,json,hashlib,urllib.request,urllib.parse,concurrent.futures,subprocess
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'V0.7.3_24項修正_2026-10-19'
spec=importlib.util.spec_from_file_location('pub',P/'publish-preview.py');pub=importlib.util.module_from_spec(spec);spec.loader.exec_module(pub)
s=json.loads((O/'GitHub測試發布紀錄.json').read_text('utf8'))
def fetch(url):
 with urllib.request.urlopen(urllib.request.Request(url,headers={'Cache-Control':'no-cache','User-Agent':'Jiuzhou-preview-verification'}),timeout=60) as r:return r.read()
files=[('preview/v0.7.3/index.html',s['url']),('index.html','https://a03697ss1.github.io/jiuzhou-rpg/?verify='+s['build']),('定案規則_0.7.2.json','https://a03697ss1.github.io/jiuzhou-rpg/'+urllib.parse.quote('定案規則_0.7.2.json')+'?verify='+s['build'])]
files+=[('preview/v0.7.3/revision24-assets/'+n+'.webp',pub.URL+'revision24-assets/'+urllib.parse.quote(n+'.webp')+'?rev='+s['build']) for n in ['長右_水','長右_水雷','一階樸素素材箱','二階樸素素材箱','獸技殘頁']]
def check(row):
 name,url=row;expected=hashlib.sha256(subprocess.check_output([pub.G,'-c','safe.directory='+pub.W.as_posix(),'-C',str(pub.W),'show','HEAD:'+name])).hexdigest();actual=hashlib.sha256(fetch(url)).hexdigest();return {'file':name,'pass':expected==actual,'expected':expected,'actual':actual}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:checks=list(pool.map(check,files))
result={'build':s['build'],'pass':all(c['pass'] for c in checks),'formalUpdated':False,'checks':checks};(O/'GitHub線上版本與正式檔案核對.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),'utf8');print(json.dumps(result,ensure_ascii=False));raise SystemExit(0 if result['pass'] else 1)
