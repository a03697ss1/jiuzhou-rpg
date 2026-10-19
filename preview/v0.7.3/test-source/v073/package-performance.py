from pathlib import Path
import importlib.util,re,json,shutil
P=Path(__file__).resolve().parent;R=P.parents[1];BUILD='20261019-official073-4';sp=importlib.util.spec_from_file_location('pub',P/'publish-preview.py');pub=importlib.util.module_from_spec(sp);sp.loader.exec_module(pub);sp=importlib.util.spec_from_file_location('rel',P/'release-official073.py');rel=importlib.util.module_from_spec(sp);sp.loader.exec_module(rel);T=pub.O/'Git測試分支';D=pub.DEST
code=(P/'performance1019.js').read_text('utf8')
for folder in [T,D]:
 f=folder/'index.html';s=f.read_text('utf8');assert 'jz073-performance1019' not in s;s+='\n<script id="jz073-performance1019">'+code+'</script>';s=re.sub(r'window.JZ073_BUILD_ID="[^"]+";',lambda m:'window.JZ073_BUILD_ID="'+BUILD+'";',s);f.write_text(s,'utf8');shutil.copy2(P/'performance1019.js',folder/'test-source/v073/performance1019.js')
s=rel.official((D/'index.html').read_text('utf8'));(pub.W/'index.html').write_text(s,'utf8');(T/'official073/index.html').write_text(s,'utf8')
f=P/'build.py';s=f.read_text('utf8');s=s.replace(' return text+code'," code+='<script id=\"jz073-performance1019\">'+(P/'performance1019.js').read_text('utf8')+'</script>\\n'\n return text+code");f.write_text(s,'utf8')
# Keep the complete consolidated master. Do not replace it with the old patch-only file.
f=R/'九州修仙錄_正式母檔_0.7.3.html';s=f.read_text('utf8');assert 'jz073-performance1019' not in s;s+='\n<script id="jz073-performance1019">'+code+'</script><script>window.JZ073_BUILD_ID="'+BUILD+'";</script>';f.write_text(s,'utf8')
print('Prepared performance patch without replacing any existing module')
