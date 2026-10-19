from pathlib import Path
import importlib.util,re,shutil
P=Path(__file__).resolve().parent;R=P.parents[1];BUILD='20261019-official073-5';sp=importlib.util.spec_from_file_location('pub',P/'publish-preview.py');pub=importlib.util.module_from_spec(sp);sp.loader.exec_module(pub);sp=importlib.util.spec_from_file_location('rel',P/'release-official073.py');rel=importlib.util.module_from_spec(sp);sp.loader.exec_module(rel);T=pub.O/'Git測試分支';D=pub.DEST;names=['material-capacity1019','main-sidebar1019']
for folder in [T,D]:
 f=folder/'index.html';s=f.read_text('utf8')
 for name in names:
  assert 'id="jz073-'+name+'"' not in s;s+='\n<script id="jz073-'+name+'">'+(P/(name+'.js')).read_text('utf8')+'</script>';shutil.copy2(P/(name+'.js'),folder/'test-source/v073'/(name+'.js'))
 s=re.sub(r'window.JZ073_BUILD_ID="[^"]+";',lambda m:'window.JZ073_BUILD_ID="'+BUILD+'";',s);f.write_text(s,'utf8')
s=rel.official((D/'index.html').read_text('utf8'));(pub.W/'index.html').write_text(s,'utf8');(T/'official073/index.html').write_text(s,'utf8')
f=P/'build.py';s=f.read_text('utf8')
for name in names:s=s.replace(' return text+code'," code+='<script id=\"jz073-"+name+"\">'+(P/'"+name+".js').read_text('utf8')+'</script>\\n'\n return text+code")
f.write_text(s,'utf8');f=R/'九州修仙錄_正式母檔_0.7.3.html';s=f.read_text('utf8')
for name in names:
 assert 'id="jz073-'+name+'"' not in s;s+='\n<script id="jz073-'+name+'">'+(P/(name+'.js')).read_text('utf8')+'</script>'
s+='<script>window.JZ073_BUILD_ID="'+BUILD+'";</script>';f.write_text(s,'utf8');print('Prepared material capacity and main sidebar patches')
