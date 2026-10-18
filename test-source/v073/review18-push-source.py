from pathlib import Path
import importlib.util,json
p=Path(__file__).resolve().parent/'publish-preview.py'
spec=importlib.util.spec_from_file_location('pub',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
w=m.ROOT/'V0.7.3_獨立測試_2026-10-17/Git測試分支'
branch=m.git(w,'branch','--show-current');assert branch=='test/v0.7.3-20261017'
print(m.git(w,'push','origin','HEAD:refs/heads/'+branch),flush=True)
o=m.ROOT/'V0.7.3_18項修正_2026-10-18/本地測試分支保存紀錄.json'
d=json.loads(o.read_text('utf-8'));d.update(pushed=True,remoteBranch=branch);o.write_text(json.dumps(d,ensure_ascii=False,indent=2),'utf-8')
print(json.dumps(d,ensure_ascii=False),flush=True)
