from pathlib import Path
import importlib.util,json,shutil
P=Path(__file__).resolve().parent;s=importlib.util.spec_from_file_location('p',P/'publish-pet1018.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
manifest=json.loads((m.O/'本輪交付清單.json').read_text('utf8'));manifest.update(published=True,url=m.old.URL,build=m.BUILD)
(m.DEST/'本輪交付清單.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),'utf8')
shutil.copy2(m.O/'GitHub發布前驗收.json',m.DEST/'GitHub發布前驗收.json')
m.publish()
r=json.loads((m.O/'GitHub獨立測試部署紀錄.json').read_text('utf8'));manifest['deploymentCommit']=r['deploymentCommit']
(m.O/'本輪交付清單.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),'utf8')
