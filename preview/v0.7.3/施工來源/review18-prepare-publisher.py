from pathlib import Path
P=Path(__file__).resolve().parent;s=(P/'publish-revision1018.py').read_text('utf8')
s=s.replace("ROOT/'V0.7.3_逐項修正_2026-10-18'","ROOT/'V0.7.3_18項修正_2026-10-18'").replace("BUILD = '20261018-review-fixes-2'","BUILD = '20261018-review18-1'")
s=s.replace("('/人物全身_2026-10-18/','fullbody-assets/'),","('/人物全身_2026-10-18/','fullbody-assets/'),('/物品獨立美術_2026-10-18/','unique-item-assets/'),")
s=s.replace("('../人物全身_2026-10-18/','fullbody-assets/'),","('../人物全身_2026-10-18/','fullbody-assets/'),('../物品獨立美術_2026-10-18/','unique-item-assets/'),")
s=s.replace("('人物全身_2026-10-18','fullbody-assets')","('人物全身_2026-10-18','fullbody-assets'),('物品獨立美術_2026-10-18','unique-item-assets')")
s=s.replace('publish-revision1018-state.json','review18-publish-state.json')
s=s.replace('Publish October 18 catalogue help boss and item art fixes to independent 0.7.3 preview','Publish 18 gameplay review fixes and independent item art to 0.7.3 preview')
(P/'review18-publish.py').write_text(s,'utf8')
# Keep the proven branch push and online hash checks, targeting this delivery and build.
for old,new in [('push-revision-source1018.py','review18-push-source.py'),('live-revision1018.py','review18-live.py')]:
 t=(P/old).read_text('utf8').replace('V0.7.3_逐項修正_2026-10-18','V0.7.3_18項修正_2026-10-18').replace('publish-revision1018-state.json','review18-publish-state.json').replace('20261018-review-fixes-2','20261018-review18-1')
 (P/new).write_text(t,'utf8')
