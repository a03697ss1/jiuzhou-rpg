from pathlib import Path
import importlib.util,json,shutil,re,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];sp=importlib.util.spec_from_file_location('pub',P/'publish-preview.py');pub=importlib.util.module_from_spec(sp);sp.loader.exec_module(pub);T=pub.O/'Git測試分支';D=pub.DEST;O=R/'V0.7.3_最新母檔整併_2026-10-19';BUILD='20261019-official073-3'
qa=json.loads((O/'郵件靈幣即時顯示驗收.json').read_text('utf8'));assert not qa['errors'] and len(qa['rows'])==5 and all(r['pass'] for r in qa['rows'])
for folder in [D/'test-source/v073',T/'test-source/v073']:
 for name in ['mail-refresh1019.js','mail-refresh-test.cjs','package-mail-refresh.py','finalize-mail-refresh.py','build.py']:shutil.copy2(P/name,folder/name)
f=pub.W/'定案規則_0.7.3.json';rules=json.loads(f.read_text('utf8'));rules['build']=BUILD;rules['mail']['claimCurrencyDisplay']='領取當下刷新左側靈幣，顯示本次增加金額及餘額；同步儲存入帳與附件已領取狀態，不重複補發。';rules['sourceModules'].append({'name':'mail-refresh1019.js','sha256':pub.digest(P/'mail-refresh1019.js')});f.write_text(json.dumps(rules,ensure_ascii=False,indent=2),'utf8');shutil.copy2(f,T/'official073/定案規則_0.7.3.json')
# Preserve the complete mother file; only update its official rule subset here.
f=R/'最新定案母檔_0.7.3.json';master=json.loads(f.read_text('utf8'));assert 'currentConfirmed073'in master;master['official073']=rules;f.write_text(json.dumps(master,ensure_ascii=False,indent=2),'utf8')
shutil.copy2(O/'郵件靈幣即時顯示驗收.json',D/'10-19H_郵件靈幣即時顯示驗收.json');shutil.copy2(P/'mail-refresh-before.json',O/'郵件靈幣延遲重現.json')
report='<!doctype html><meta charset="utf-8"><title>0.7.3 信件靈幣即時顯示修正</title><style>body{max-width:900px;margin:40px auto;padding:20px;background:#0b1924;color:#e1e9ed;font:18px/1.8 sans-serif}a{color:#efcd86}</style><h1>信件靈幣即時顯示修正</h1><p>原問題：領取後資料已由600變成5600，但左側仍顯示600，直到後續更新畫面才顯示新餘額。</p><p>修正：領取當下刷新靈幣數字，信件頂端顯示本次領取金額與餘額；餘額及已領附件立即存檔。已領過的信不補發。</p><h2>驗證</h2><ul>'+''.join('<li>'+r['name']+'：通過</li>' for r in qa['rows'])+'</ul><p><a href="../../../?build='+BUILD+'">開啟正式遊戲</a> · <a href="10-19H_郵件靈幣即時顯示驗收.json">驗收資料</a></p>'
(D/'10-19H_信件靈幣修正.html').write_text(report,'utf8');(O/'信件靈幣修正報告.html').write_text(report,'utf8')
old=pub.git(pub.W,'show','HEAD:preview/v0.7.3/index.html');new=(D/'index.html').read_text('utf8');scripts=lambda s:{m[1]:m[2] for m in re.finditer(r'<script id="([^"]+)">(.*?)</script>',s,re.S)};a,b=scripts(old),scripts(new);assert all(b[k]==v for k,v in a.items())
s={'build':BUILD,'url':'https://a03697ss1.github.io/jiuzhou-rpg/?build='+BUILD,'base':pub.git(pub.W,'rev-parse','HEAD'),'tests':5,'siteBytes':sum(f.stat().st_size for f in pub.W.rglob('*') if f.is_file() and '.git' not in f.parts)};assert s['siteBytes']<1073741824;(P/'mail-refresh-state.json').write_text(json.dumps(s,ensure_ascii=False,indent=2),'utf8');print(json.dumps(s,ensure_ascii=False))
