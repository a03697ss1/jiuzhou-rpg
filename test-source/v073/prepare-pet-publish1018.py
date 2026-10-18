from pathlib import Path
P=Path(__file__).resolve().parent
s=(P/'publish1018.py').read_text('utf8').replace("O = ROOT/'V0.7.3_部分項目補完_2026-10-18'","O = ROOT/'V0.7.3_新三寵補完_2026-10-18'").replace('20261018-material-side-preview-1','20261018-pet-complete-2').replace('publish1018-state.json','publish-pet1018-state.json').replace('October 18 supplement','October 18 completed pet cores').replace('Update 0.7.3 independent preview with October 18 supplement','Complete 0.7.3 pet cores, hatching and version display')
(P/'publish-pet1018.py').write_text(s,'utf8')
s=(P/'publish1018-qa.cjs').read_text('utf8').replace('V0.7.3_部分項目補完_2026-10-18','V0.7.3_新三寵補完_2026-10-18').replace('20261018-material-side-preview-1','20261018-pet-complete-2').replace('partial!==4','partial!==1')
(P/'publish-pet1018-qa.cjs').write_text(s,'utf8')
s=(P/'offline1018.cjs').read_text('utf8').replace('V0.7.3_部分項目補完_2026-10-18','V0.7.3_新三寵補完_2026-10-18')
(P/'offline-pet1018.cjs').write_text(s,'utf8')
s=(P/'live1018.py').read_text('utf8').replace('V0.7.3_部分項目補完_2026-10-18','V0.7.3_新三寵補完_2026-10-18').replace('publish1018-state.json','publish-pet1018-state.json').replace("P/'publish1018.py'","P/'publish-pet1018.py'")
(P/'live-pet1018.py').write_text(s,'utf8')
