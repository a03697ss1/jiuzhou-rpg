from pathlib import Path
import importlib.util,re,shutil,json
P=Path(__file__).resolve().parent;R=P.parents[1]
f=P/'revision8-1019.js';s=f.read_text('utf8').replace('N.releaseHistory073.改動=',"N.releaseHistory073??={新增:[],改動:[],BUG修復:[]};\nN.releaseHistory073.改動=",1);f.write_text(s,'utf8')
spec=importlib.util.spec_from_file_location('pub',P/'publish-preview.py');pub=importlib.util.module_from_spec(spec);spec.loader.exec_module(pub)
spec=importlib.util.spec_from_file_location('rel',P/'release-official073.py');rel=importlib.util.module_from_spec(spec);spec.loader.exec_module(rel)
T=pub.O/'Git測試分支';D=pub.DEST;BUILD='20261019-official073-2'
for folder in [T,D]:
 f=folder/'index.html';s=f.read_text('utf8');code=(P/'revision8-1019.js').read_text('utf8');pattern=r'<script id="jz073-revision8-1019">.*?</script>'
 if re.search(pattern,s,re.S):s=re.sub(pattern,lambda m:'<script id="jz073-revision8-1019">'+code+'</script>',s,flags=re.S)
 else:s+='\n<script id="jz073-revision8-1019">'+code+'</script>'
 s=re.sub(r'window.JZ073_BUILD_ID="[^"]+";',lambda m:'window.JZ073_BUILD_ID="'+BUILD+'";',s);f.write_text(s,'utf8')
 for name in ['revision8-1019.js','build.py']:
  dest=folder/'test-source/v073'/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(P/name,dest)
root=rel.official((D/'index.html').read_text('utf8'));(pub.W/'index.html').write_text(root,'utf8');(T/'official073/index.html').write_text(root,'utf8')
print('Prepared incrementally; previous modules preserved')
