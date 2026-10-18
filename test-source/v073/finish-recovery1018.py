from pathlib import Path
import json,shutil,importlib.util
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'V0.7.3_存檔銜接修復_2026-10-18';W=R/'V0.7.3_獨立測試_2026-10-17/Git測試分支'
p=P/'save-recovery1018.js';s=p.read_text('utf8').replace('E(r.savedAt)','E(D.time(r.savedAt))');p.write_text(s,'utf8')
shutil.copy2(p,O/'施工來源'/p.name);shutil.copy2(p,W/'test-source/v073'/p.name)
for n in ['publish-recovery1018.py','publish-recovery1018-qa.cjs']:
 p=P/n;s=p.read_text('utf8').replace('20261018-save-recovery-3','20261018-save-recovery-4');p.write_text(s,'utf8')
