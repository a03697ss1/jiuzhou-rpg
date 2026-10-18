from pathlib import Path
import importlib.util,json
P=Path(__file__).resolve().parent;s=importlib.util.spec_from_file_location('p',P/'publish1018.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
W=m.ROOT/'V0.7.3_獨立測試_2026-10-17/Git測試分支';O=m.ROOT/'V0.7.3_新三寵補完_2026-10-18'
m.git(W,'add','--','index.html','test-source/v073')
paths=[x for x in m.git(W,'diff','--cached','--name-only','-z').split('\0') if x]
assert all(x=='index.html' or x.startswith('test-source/v073/') for x in paths)
if paths:m.git(W,'commit','-m','Complete user-confirmed new pet cores and normal hatch progression')
record={'commit':m.git(W,'rev-parse','HEAD'),'branch':m.git(W,'branch','--show-current'),'formalUpdated':False,'pushed':False}
(O/'本地測試分支保存紀錄.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),'utf8')
print(json.dumps(record,ensure_ascii=False))
