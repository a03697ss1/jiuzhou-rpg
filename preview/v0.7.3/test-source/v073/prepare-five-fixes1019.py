from pathlib import Path
import importlib.util,re,shutil
P=Path(__file__).resolve().parent;R=P.parents[1]
def load(name,file):
 s=importlib.util.spec_from_file_location(name,P/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
pub=load('pub','publish-preview.py');rel=load('rel','release-official073.py');heal=load('heal','heal-dot1019.py');T=pub.O/'Git測試分支';D=pub.DEST
for f in [T/'index.html',D/'index.html',R/'九州修仙錄_正式母檔_0.7.3.html']:
 s=f.read_text('utf8');assert 'id="jz073-five-fixes1019"' not in s;s=heal.patch(s);s+='\n<script id="jz073-five-fixes1019">'+(P/'five-fixes1019.js').read_text('utf8')+'</script>';s=re.sub(r'window.JZ073_BUILD_ID="[^"]+";',lambda m:'window.JZ073_BUILD_ID="20261019-official073-7";',s);f.write_text(s,'utf8')
s=rel.official((D/'index.html').read_text('utf8'));(pub.W/'index.html').write_text(s,'utf8');(T/'official073/index.html').write_text(s,'utf8')
f=P/'build.py';s=f.read_text('utf8');s=s.replace(' return text+code'," code+='<script id=\"jz073-five-fixes1019\">'+(P/'five-fixes1019.js').read_text('utf8')+'</script>\\n'\n import importlib.util\n sp=importlib.util.spec_from_file_location('heal_dot1019',P/'heal-dot1019.py');mod=importlib.util.module_from_spec(sp);sp.loader.exec_module(mod);text=mod.patch(text)\n return text+code");f.write_text(s,'utf8')
for folder in [T/'test-source/v073',D/'test-source/v073']:
 for name in ['five-fixes1019.js','heal-dot1019.py','prepare-five-fixes1019.py','build.py']:shutil.copy2(P/name,folder/name)
print('Prepared five fixes, build 7')
