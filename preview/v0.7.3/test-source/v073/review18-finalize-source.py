from pathlib import Path
import importlib.util,shutil,json
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'V0.7.3_18項修正_2026-10-18';W=R/'V0.7.3_獨立測試_2026-10-17/Git測試分支'
spec=importlib.util.spec_from_file_location('pub',P/'publish-preview.py');pub=importlib.util.module_from_spec(spec);spec.loader.exec_module(pub)
assert pub.git(W,'branch','--show-current')=='test/v0.7.3-20261017'
for f in P.iterdir():
 if f.suffix in ['.js','.cjs','.py','.css','.json'] and f.stat().st_size<5_000_000:
  shutil.copy2(f,O/'施工來源'/f.name);shutil.copy2(f,W/'test-source/v073'/f.name)
for name in ['線上圖片無損編碼驗證.json','既有預覽圖片無損編碼驗證.json','驗收截圖無損編碼驗證.json']:
 d=json.loads((O/name).read_text('utf8'));assert d['pass']
pub.git(W,'add','--','test-source/v073')
if pub.git(W,'diff','--cached','--name-only'):pub.git(W,'commit','-m','Verify lossless preview image encodings and delivery checks')
d={'commit':pub.git(W,'rev-parse','HEAD'),'branch':pub.git(W,'branch','--show-current'),'formalUpdated':False,'pushed':False,'originalPNGImages':384}
(O/'本地測試分支保存紀錄.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),'utf8')
print(json.dumps(d,ensure_ascii=False))
