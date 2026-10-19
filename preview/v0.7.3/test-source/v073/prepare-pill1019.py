from pathlib import Path
import importlib.util,shutil
P=Path(__file__).resolve().parent;R=P.parents[1];s=importlib.util.spec_from_file_location('pub',P/'publish-preview.py');pub=importlib.util.module_from_spec(s);s.loader.exec_module(pub);s=importlib.util.spec_from_file_location('rel',P/'release-official073.py');rel=importlib.util.module_from_spec(s);s.loader.exec_module(rel);T=pub.O/'Git測試分支';D=pub.DEST;name='player-break-pill1019'
for f in [T/'index.html',D/'index.html',R/'九州修仙錄_正式母檔_0.7.3.html']:
 text=f.read_text('utf8');assert 'id="jz073-'+name+'"' not in text;f.write_text(text+'\n<script id="jz073-'+name+'">'+(P/(name+'.js')).read_text('utf8')+'</script>','utf8')
text=rel.official((D/'index.html').read_text('utf8'));(pub.W/'index.html').write_text(text,'utf8');(T/'official073/index.html').write_text(text,'utf8')
f=P/'build.py';text=f.read_text('utf8').replace(' return text+code'," code+='<script id=\"jz073-"+name+"\">'+(P/'"+name+".js').read_text('utf8')+'</script>\\n'\n return text+code");f.write_text(text,'utf8')
for folder in [T/'test-source/v073',D/'test-source/v073']:
 for n in [name+'.js','prepare-pill1019.py','package-pill-art1019.cjs','build.py']:shutil.copy2(P/n,folder/n)
