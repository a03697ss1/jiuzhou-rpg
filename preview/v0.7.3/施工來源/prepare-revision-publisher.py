from pathlib import Path
P=Path(__file__).resolve().parent
s=(P/'publish-recovery1018.py').read_text('utf-8')
for a,b in [('V0.7.3_存檔銜接修復_2026-10-18','V0.7.3_逐項修正_2026-10-18'),('20261018-save-recovery-4','20261018-review-fixes-1'),('publish-recovery1018-state.json','publish-revision1018-state.json'),('Add protected old-save recovery to independent 0.7.3 preview','Publish October 18 catalogue help boss and item art fixes to independent 0.7.3 preview')]:s=s.replace(a,b)
s=s.replace("('/素材美術_2026-10-18/','material-assets/'),","('/素材美術_2026-10-18/','material-assets/'),('/物品美術_2026-10-18/','item-assets/'),('/人物全身_2026-10-18/','fullbody-assets/'),")
s=s.replace("('素材美術_2026-10-18','material-assets')]:","('素材美術_2026-10-18','material-assets'),('物品美術_2026-10-18','item-assets'),('人物全身_2026-10-18','fullbody-assets')]:")
s=s.replace("('../素材美術_2026-10-18/','material-assets/'),","('../素材美術_2026-10-18/','material-assets/'),('../物品美術_2026-10-18/','item-assets/'),('../人物全身_2026-10-18/','fullbody-assets/'),")
(P/'publish-revision1018.py').write_text(s,'utf-8')
