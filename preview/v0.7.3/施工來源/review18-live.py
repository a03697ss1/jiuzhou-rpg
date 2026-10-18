from pathlib import Path
import json, hashlib, urllib.request, urllib.parse, datetime, sys, subprocess, importlib.util
P=Path(__file__).resolve().parent; ROOT=P.parents[1]; O=ROOT/'V0.7.3_18項修正_2026-10-18'
state=json.loads((P/'review18-publish-state.json').read_text('utf8'))
spec=importlib.util.spec_from_file_location('publisher',P/'publish-revision1018.py'); pub=importlib.util.module_from_spec(spec); spec.loader.exec_module(pub)
def blobsha(n,revision='HEAD'):
    return hashlib.sha256(subprocess.check_output([pub.old.G,'-c','safe.directory='+pub.W.as_posix(),'-C',str(pub.W),'show',revision+':'+n])).hexdigest()
expected=blobsha('preview/v0.7.3/index.html')
url=state['url']+'?build='+state['build']
def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers={'Cache-Control':'no-cache','User-Agent':'Jiuzhou-preview-validation'}),timeout=60) as r:return r.read()
data=fetch(url); sha=hashlib.sha256(data).hexdigest()
result={'url':url,'expectedSha256':expected,'actualSha256':sha,'previewMatches':sha==expected,'formalEntrySha256':hashlib.sha256(fetch('https://a03697ss1.github.io/jiuzhou-rpg/?check=20261018')).hexdigest(),'formalRulesSha256':hashlib.sha256(fetch('https://a03697ss1.github.io/jiuzhou-rpg/'+urllib.parse.quote('定案規則_0.7.2.json')+'?check=20261018')).hexdigest()}
result['formalEntryUnchanged']=result['formalEntrySha256']==blobsha('index.html',state['base'])
result['formalRulesUnchanged']=result['formalRulesSha256']==blobsha('定案規則_0.7.2.json',state['base'])
result['pass']=all(result[k] for k in ['previewMatches','formalEntryUnchanged','formalRulesUnchanged'])
(O/'GitHub線上版本與正式入口驗證.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),'utf8')
print(json.dumps(result,ensure_ascii=False))
sys.exit(0 if result['pass'] else 1)
