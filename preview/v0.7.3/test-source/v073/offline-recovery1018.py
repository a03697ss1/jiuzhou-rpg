from pathlib import Path
P=Path(__file__).resolve().parent
s=(P/'offline-pet1018.cjs').read_text('utf8').replace('V0.7.3_新三寵補完_2026-10-18','V0.7.3_存檔銜接修復_2026-10-18')
(P/'offline-recovery1018.cjs').write_text(s,'utf8')
