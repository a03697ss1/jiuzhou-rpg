from pathlib import Path
import json,shutil,importlib.util
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'V0.7.3_存檔銜接修復_2026-10-18';W=R/'V0.7.3_獨立測試_2026-10-17/Git測試分支'
s=(P/'preview.html').read_text('utf8').replace('/github-release/assets/','assets/').replace('/新增美術_2026-10-16/','new-assets/').replace('/素材美術_2026-10-18/','material-assets/')
(W/'index.html').write_text(s,'utf8')
for f in [P/'build.py',P/'save-recovery1018.js']:
 shutil.copy2(f,W/'test-source/v073'/f.name);shutil.copy2(f,O/'施工來源'/f.name)
spec=importlib.util.spec_from_file_location('publisher',P/'publish-recovery1018.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.git(W,'add','--','index.html','test-source/v073');m.git(W,'commit','-m','Display recovered save timestamps in Taiwan time')
(O/'本地測試分支保存紀錄.json').write_text(json.dumps({'commit':m.git(W,'rev-parse','HEAD'),'branch':m.git(W,'branch','--show-current'),'formalUpdated':False,'pushed':False},ensure_ascii=False,indent=2),'utf8')
p=P/'publish-recovery1018.py';s=p.read_text('utf8').replace('Update 0.7.3 independent preview with October 18 completed pet cores','Add protected old-save recovery to independent 0.7.3 preview');p.write_text(s,'utf8')
s=(P/'save-recovery1018-qa.cjs').read_text('utf8').replace('http://127.0.0.1:18776/github-release/index.html','https://a03697ss1.github.io/jiuzhou-rpg/').replace('http://127.0.0.1:18776/release-tools/v073/preview.html','https://a03697ss1.github.io/jiuzhou-rpg/preview/v0.7.3/?build=20261018-save-recovery-4').replace('舊版存檔銜接驗收.json','GitHub線上存檔銜接驗收.json')
(P/'live-recovery1018-qa.cjs').write_text(s,'utf8')
print('Updated local test commit and online recovery acceptance')
