from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parents[1];A=R/'素材美術_2026-10-18'
rows=[]
for name in ['生成清單與提示詞.json','生成清單與提示詞_後24項.json']:
 rows+=json.loads((A/name).read_text('utf-8-sig'))
unique={r['name']:r for r in rows}
assert len(unique)==69, len(unique)
assert all((R/r['file']).exists() for r in unique.values())
(A/'生成清單與提示詞.json').write_text(json.dumps(list(unique.values()),ensure_ascii=False,indent=2),'utf8')
print('69 icon sources and complete prompts merged.')
