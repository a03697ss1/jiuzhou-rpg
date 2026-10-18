from pathlib import Path
import json,shutil,html,importlib.util
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'V0.7.3_存檔銜接修復_2026-10-18';PREV=R/'V0.7.3_新三寵補完_2026-10-18';W=R/'V0.7.3_獨立測試_2026-10-17/Git測試分支'
for f in PREV.iterdir():
 if f.is_file() and f.suffix in ['.json','.png','.html'] and f.name!='九州修仙錄_V0.7.3_獨立測試版.html' and not (O/f.name).exists():shutil.copy2(f,O/f.name)
source=O/'施工來源';source.mkdir(exist_ok=True)
for f in list(P.glob('*.js'))+[P/'build.py',P/'save-recovery1018-qa.cjs']:shutil.copy2(f,source/f.name)
preview=(P/'preview.html').read_text('utf8').replace('/github-release/assets/','assets/').replace('/新增美術_2026-10-16/','new-assets/').replace('/素材美術_2026-10-18/','material-assets/')
(W/'index.html').write_text(preview,'utf8')
for f in list(P.glob('*.js'))+[P/'build.py']:shutil.copy2(f,W/'test-source/v073'/f.name)
read=lambda p:json.loads(p.read_text('utf8'))
qa=read(O/'舊版存檔銜接驗收.json');assert len(qa['rows'])==8 and all(r['pass'] for r in qa['rows']) and not qa['errors']
coverage=read(PREV/'逐項施工工程覆蓋表.json')
reason='保留測試版隔離；新增原版四槽副本讀取、保留區、讀取前自動存檔備份及不覆蓋手動槽的JSON匯入。'
for row in coverage:
 if row['id']=='L36':row.update(reason=reason,source='save-recovery1018.js',tests=['舊版存檔銜接驗收.json'])
(O/'逐項施工工程覆蓋表.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2),'utf8')
section='<section><h2>本輪存檔銜接修復</h2><p>0.7.3先前使用獨立存檔區，一般清單不會列出正式版紀錄。新版在登入畫面及存檔管理新增「讀取舊版紀錄」。同一網站原存檔可直接列出並以副本讀取；原版四槽與現有測試手動槽不改寫，讀取前的測試版自動存檔另存於保留區。</p><p>若原存檔在本機HTML、另一網址或另一Chrome設定檔，此網站無法直接讀取。可回原遊戲匯出JSON，再以本頁「從存檔檔案讀取」開啟；不會覆蓋手動槽1。</p><p>本輪8項驗證通過。測試使用隔離瀏覽器建立的0.7.2紀錄；尚未直接讀取使用者Chrome個人紀錄，因此不宣稱使用者的個人存檔已恢復。</p><p><a href="舊版存檔銜接驗收.json">8項測試證據</a> · <a href="施工來源/save-recovery1018.js">對應程式</a></p><img src="找到原版四槽.png"><img src="新舊存檔與保留備份.png"></section>'
for name in ['閱讀我_先看這裡.html','BUG修復與待補清單.html','完整測試及驗收報告.html']:
 p=O/name;s=p.read_text('utf8').replace('本次重新執行105項檢查，全部通過。','前輪新三寵補完105項檢查通過；本輪另執行8項存檔銜接檢查，沒有重跑或重複計入前輪檢查。');s=s.replace('</main>',section+'</main>');p.write_text(s,'utf8')
p=O/'逐項施工工程覆蓋表.html';s=p.read_text('utf8');old=next(r for r in read(PREV/'逐項施工工程覆蓋表.json') if r['id']=='L36')['reason'];s=s.replace(html.escape(old),html.escape(reason));s=s.replace('</main>',section+'</main>');p.write_text(s,'utf8')
manifest=read(PREV/'本輪交付清單.json');manifest.update(published=False,supplement='2026-10-18-save-recovery',recoveryTests={'passed':8,'total':8},personalChromeRecordsVerified=False)
(O/'本輪交付清單.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),'utf8')
spec=importlib.util.spec_from_file_location('old',P/'publish1018.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
old.git(W,'add','--','index.html','test-source/v073');old.git(W,'commit','-m','Add read-only old-save discovery and protected recovery copies')
receipt={'commit':old.git(W,'rev-parse','HEAD'),'branch':old.git(W,'branch','--show-current'),'formalUpdated':False,'pushed':False}
(O/'本地測試分支保存紀錄.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),'utf8')
s=(P/'publish-pet1018.py').read_text('utf8').replace("O = ROOT/'V0.7.3_新三寵補完_2026-10-18'","O = ROOT/'V0.7.3_存檔銜接修復_2026-10-18'").replace('20261018-pet-complete-2','20261018-save-recovery-3').replace('publish-pet1018-state.json','publish-recovery1018-state.json')
(P/'publish-recovery1018.py').write_text(s,'utf8')
for src,dest in [('publish-pet1018-qa.cjs','publish-recovery1018-qa.cjs'),('live-pet1018.py','live-recovery1018.py')]:
 s=(P/src).read_text('utf8').replace('V0.7.3_新三寵補完_2026-10-18','V0.7.3_存檔銜接修復_2026-10-18').replace('20261018-pet-complete-2','20261018-save-recovery-3').replace('publish-pet1018-state.json','publish-recovery1018-state.json').replace("P/'publish-pet1018.py'","P/'publish-recovery1018.py'")
 (P/dest).write_text(s,'utf8')
s=(P/'final-publish-pet1018.py').read_text('utf8').replace("P/'publish-pet1018.py'","P/'publish-recovery1018.py'")
(P/'final-publish-recovery1018.py').write_text(s,'utf8')
print(json.dumps({'localCommit':receipt['commit'],'recoveryTests':8,'personalRecordsVerified':False},ensure_ascii=False))
