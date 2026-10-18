from pathlib import Path
import re,json
s=Path('release-tools/v073/baseline-preview.html').read_text('utf8')
for key in ['S.roots[','S.roots.',"key==='靈根丹'","n==='［初階］靈根丹'",'function showModal(', 'U.openBoard=', 'U.openBoard','U.openBox=', 'sleepResist']:
 print('\n###',key)
 for m in list(re.finditer(re.escape(key),s))[-3:]:print(s[max(0,m.start()-120):m.start()+800])
x=json.loads(Path('V0.7.3_18項修正_2026-10-18/18項功能驗收.json').read_text('utf8'));print('\n### board inspect\n'+json.dumps(x['rows'][-1]['detail'],ensure_ascii=False,indent=2))
