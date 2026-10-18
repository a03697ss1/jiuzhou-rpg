from pathlib import Path
import json, hashlib, re, shutil, html, collections, subprocess, datetime

P=Path(__file__).resolve().parent
R=P.parents[1]
O=R/'V0.7.3_獨立測試_2026-10-17'
W=O/'Git測試分支'
G=Path('C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/git/cmd/git.exe')
def read(p): return json.loads(p.read_text('utf8'))
def digest(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(8*1024*1024),b''):h.update(chunk)
    return h.hexdigest()
def git(root,*args):
    return subprocess.check_output([str(G),'-c','safe.directory='+root.as_posix(),'-C',str(root),*args],text=True,encoding='utf8').strip()
def writejson(name,data): (O/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),'utf8')
e=lambda x:html.escape(str(x))
baseline=read(P/'baseline.json')
protected=[]
for n,v in baseline['protected'].items():
    f=R/n
    actual=digest(f)
    protected.append({'path':n,'bytes':f.stat().st_size,'before':v['sha256'],'after':actual,'unchanged':actual==v['sha256']})
assert all(r['unchanged'] for r in protected),'Formal file changed'
assert git(R/'github-release','rev-parse','HEAD')==baseline['commit']
assert git(R/'github-release','status','--porcelain')=='','Formal tree changed'

# Only the local independent worktree receives this build and its editable source.
preview=(P/'preview.html').read_text('utf8').replace('/github-release/assets/','assets/').replace('/新增美術_2026-10-16/','new-assets/')
(W/'index.html').write_text(preview,'utf8')
(W/'new-assets').mkdir(exist_ok=True)
for name in set(re.findall(r'new-assets/([^"\x27<>\n]+\.png)',preview)):
    shutil.copy2(R/'新增美術_2026-10-16'/name,W/'new-assets'/name)
source=W/'test-source/v073';source.mkdir(parents=True,exist_ok=True)
for f in list(P.glob('*.js'))+[P/'build.py',P/'baseline.json',P/'story-data.json']:
    shutil.copy2(f,source/f.name)

meta=read(O/'施工狀態與規格.json')
newtests=read(O/'施工測試結果.json')['rows']+read(O/'擴充流程測試結果.json')['rows']+read(O/'B線與補充定案測試結果.json')['rows']+read(O/'A線與NPC公式測試結果.json')['rows']
assert all(t['pass'] for t in newtests)
reg=[]
for f,label in [('r1011-reg-main-results.json','舊主線'),('reg-sides-results.json','舊支線'),('reg-commissions-results.json','舊25委託'),('reg-systems-results.json','既有系統')]:
    d=read(P/'regression'/f);rows=d['results']
    assert all(t['pass'] for t in rows) and not d.get('errors')
    reg.append({'name':label,'file':f,'checks':len(rows),'passed':sum(t['pass'] for t in rows)})
    shutil.copy2(P/'regression'/f,O/f)
boss=read(O/'長右30回合實戰資料.json')
live=read(O/'長右實際自動戰鬥驗收.json')
offline=read(O/'單檔離線驗收.json')
assert offline['pass'] and all(r['win'] for r in boss['runs']) and live['live']['win']
spec=(P/'spec.txt').read_text('utf8')
specrows=[]
for line in spec.splitlines():
    m=re.match(r'\d+ \[表\] (L\d{2}) \| ([^|]+) \| ([^|]+) \| (.+)',line)
    if m:
        row=list(m.groups())
        if row[0]=='L25':row[3]='CQ035～050；本次使用者已補齊046～049最終目標與獎勵，原待補條款被覆蓋'
        specrows.append(row)
assert len(specrows)==38
files={
 'L01':'world.js','L02':'completion.js','L03':'ui.js','L04':'ui.js','L05':'style.css',
 'L06':'ui.js','L07':'ui.js','L08':'core.js','L09':'build.py','L10':'pets.js','L11':'ui.js',
 'L12':'completion.js','L13':'world.js','L14':'world.js','L15':'monsters.js','L16':'combat.js',
 'L17':'quests.js','L18':'combat.js','L19':'pets.js','L20':'pets.js','L21':'a-story.js','L22':'a-story.js',
 'L23':'quests.js','L24':'commissions.js','L25':'commissions.js','L26':'commissions.js',
 'L27':'clarifications.js','L28':'economy.js','L29':'combat.js','L30':'npc-generation.js','L31':'codex.js',
 'L32':'world.js','L33':'codex.js','L34':'pets.js','L35':'completion.js','L36':'build.py',
 'L37':'build.py','L38':'baseline.json'}
shutil.copy2(P/'style.css',source/'style.css')
for filename in ['b-dialogues.txt','b-dialogues.json','a-dialogues.txt','a-dialogues.json']:
    shutil.copy2(P/filename,source/filename)
shutil.copy2(P/'b-dialogues.txt',O/'B線完整對話805節點.txt')
shutil.copy2(P/'a-dialogues.txt',O/'A線完整對話709節點.txt')
shutil.copy2(O/'NPC通用生成正式資料.json',source/'NPC通用生成正式資料.json')
writejson('補充定案_修為與問道.json',{'source':'本輪使用者對待補提問的回答','floor10':{'一般種':1,'特殊種':2,'高危種':4,'高危種（特）':5,'妖王種':8,'神獸種':15,'災獸種':15},'higher11':0,'human10':'ceil(1×該人形種類正式倍率)','rootBands':[[80,140,55],[141,190,30],[191,230,12],[231,250,3]],'weapons':{'preferred':70,'other':30,'emptyPool':'從另一合法池抽取'}})
coverage=[]
for id,title,area,accept in specrows:
    c=meta['coverage'][id]
    tests=[t for t in newtests if t['id']==id]
    evidence=[t['name'] for t in tests]
    if id=='L37': evidence=['14張新增資源全部離線解碼成功，引用10月16日既有PNG；未重生美術。']
    if id=='L38':evidence+=['5個受保護檔案SHA-256未變；正式main提交與工作目錄未變。']
    if id=='L26':evidence+=['既有25委託全部實際完成／領獎回歸通過。']
    if id=='L07':evidence+=['1440／1024／768／390四尺寸實際戰鬥畫面。']
    coverage.append({'id':id,'item':title.strip(),'area':area.strip(),'requiredAcceptance':accept,
       'implementation':c['state'],'reason':c['reason'],'source':files[id],
       'tests':evidence,'automatedPass':all(t['pass'] for t in tests),
       'userAcceptance':'待玩家明確驗收','fullAcceptance':False})
writejson('逐項施工工程覆蓋表.json',coverage)
writejson('正式檔案保護驗證.json',protected)
statuscounts=collections.Counter(c['implementation'] for c in coverage)
now=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
game=O/'九州修仙錄_V0.7.3_獨立測試版.html'
publication=read(O/'GitHub獨立測試部署紀錄.json') if (O/'GitHub獨立測試部署紀錄.json').exists() else None
manifest={'version':'0.7.3','phase':'獨立測試／尚未玩家驗收／未發布','createdAt':now,
 'branch':git(W,'branch','--show-current'),'baseCommit':baseline['commit'],
 'baselineHtmlSha256':baseline['protected']['九州修仙錄_測試分支.html']['sha256'],
 'game':{'name':game.name,'bytes':game.stat().st_size,'sha256':digest(game)},
 'formalFilesUnchanged':all(r['unchanged'] for r in protected),'formalWorktreeClean':True,
 'published':bool(publication),'committed':bool(publication),'publication':publication,'coverageCounts':dict(statuscounts),
 'newChecks':len(newtests),'newPassed':sum(t['pass'] for t in newtests),'regression':reg,
 'bossRuns':len(boss['runs']),'bossRoundRange':[min(r['round'] for r in boss['runs']),max(r['round'] for r in boss['runs'])],
 'liveBossRound':live['live']['round'],'offlinePass':offline['pass']}
writejson('交付驗證清單.json',manifest)

css='''body{margin:0;background:#0c1720;color:#dbe5ed;font:16px/1.7 "Microsoft JhengHei",sans-serif}main{max-width:1280px;margin:auto;padding:26px}a{color:#93caff}h1{color:#f2d68b;font-size:28px}h2{margin-top:32px;color:#c8dded}nav{display:flex;flex-wrap:wrap;gap:16px;margin:18px 0}.note{border:1px solid #b88c44;background:#33291a;padding:15px;border-radius:10px}.ok{color:#9be3ad}.pending{color:#ffcf84}.summary{display:flex;gap:16px;flex-wrap:wrap}.summary>div{padding:16px;background:#182b39;border-radius:8px}table{border-collapse:collapse;width:100%;font-size:14px}th,td{border:1px solid #355266;padding:10px;vertical-align:top}th{background:#1c3343;position:sticky;top:0}tr:nth-child(even){background:#12232f}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:12px/1.6 Consolas,monospace}img{max-width:100%;border:1px solid #375367;border-radius:8px}button,select,input{font:inherit;color:inherit;background:#203749;border:1px solid #59758a;border-radius:6px;padding:8px;margin:5px}details{margin:9px 0}li{margin:7px 0}.scroll{overflow:auto}.muted{color:#a9bccb}@media(max-width:700px){main{padding:14px}table{min-width:900px}}'''
nav='<nav><a href="閱讀我_先看這裡.html">交付入口</a><a href="九州修仙錄_V0.7.3_獨立測試版.html">單檔遊戲</a><a href="逐項施工工程覆蓋表.html">38項覆蓋表</a><a href="BUG修復與待補清單.html">BUG／待補</a><a href="完整測試及驗收報告.html">測試報告</a></nav>'
def page(name,title,body,js=''):
    (O/name).write_text('<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+e(title)+'</title><style>'+css+'</style><main><h1>'+e(title)+'</h1>'+nav+body+'</main><script>'+js+'</script></html>','utf8')
warning='<p class="note">本檔是可玩的0.7.3獨立測試交付，尚未整版驗收通過。正式母檔、正式0.7.2及GitHub均未修改。測試通過包含「缺資料時保護鎖正常」；不代表待補功能已完成。</p>'
if publication:warning='<p class="note">0.7.3獨立測試版已依使用者授權發布至GitHub測試子網址，尚未整版驗收通過。正式母檔與0.7.2正式入口保持不變。尚缺資料的功能仍列待補，未冒充完成。</p><p><a href="'+e(publication['url'])+'">開啟GitHub 0.7.3獨立測試版</a></p>'
total=len(newtests)+sum(r['checks'] for r in reg)
summary='<div class="summary"><div>施工項目：38</div><div>新增測試：'+str(len(newtests))+'／'+str(len(newtests))+'</div><div>既有回歸：'+str(sum(r['checks'] for r in reg))+'／'+str(sum(r['checks'] for r in reg))+'</div><div>長右固定種子：16／16<br>15～18回合</div></div>'
table='<table><thead><tr><th>ID／項目</th><th>實裝狀態</th><th>修改與未完成原因</th><th>測試證據</th><th>玩家驗收</th></tr></thead><tbody>'
for c in coverage:
    table+='<tr data-status="'+e(c['implementation'])+'"><td><b>'+e(c['id']+' '+c['item'])+'</b><br>'+e(c['area'])+'<br><a href="Git測試分支/test-source/v073/'+e(c['source'])+'">施工來源</a></td><td class="'+('ok' if c['implementation']=='已實裝' else 'pending')+'">'+e(c['implementation'])+'</td><td>'+e(c['reason'])+'<details><summary>工作檔驗收要求</summary>'+e(c['requiredAcceptance'])+'</details></td><td>'+''.join('<p>✓ '+e(t)+'</p>' for t in c['tests'])+('' if c['implementation']=='已實裝' else '<b class="pending">僅已實裝部分／保護鎖測試通過；整項未通過。</b>')+'</td><td>待玩家明確驗收</td></tr>'
table+='</tbody></table>'
page('逐項施工工程覆蓋表.html','V0.7.3 逐項施工工程覆蓋表',warning+summary+'<p>'+e('；'.join(k+' '+str(v)+'項' for k,v in statuscounts.items()))+'。所有項目均尚待玩家驗收。</p><p><input id="search" placeholder="搜尋項目、原因或測試"><select id="status"><option>全部</option><option>已實裝</option><option>部分實裝</option><option>待補</option></select></p><div class="scroll">'+table+'</div>',"function filter(){const q=document.querySelector('#search').value.toLowerCase(),s=document.querySelector('#status').value;document.querySelectorAll('tbody tr').forEach(r=>r.hidden=!(r.textContent.toLowerCase().includes(q)&&(s==='全部'||r.dataset.status===s)));}document.querySelector('#search').oninput=filter;document.querySelector('#status').onchange=filter;")

fixes=[
 ('任務引導','沿合法道路與傳送移動，未解鎖／戰鬥／劇情移動鎖不繞過；張榕真實際抵達測試通過。'),
 ('教學通行回歸','修正新移動閘門誤擋初期教學及問道主線例外，舊28段主線完整重跑通過。'),
 ('長右第四名隊友','排除主線同行邱山河被普通夥伴境界差上限剔除，BOSS可確實四人出戰。'),
 ('素材箱與合成','按階級及類別選取、多箱確認才扣除；個人合成不耗鑄造靈氣、100%成功、不加經驗、材料不加品質。'),
 ('火尾毛','補背包描述與圖鑑反查；顯示為二階妖物材料。未擅自擴張舊泛用委託提交資格集合。'),
 ('新地圖名稱與資訊','修正舊地圖子字串匹配把雷鳴沼地下深窟截成雷鳴沼；顯示完整名稱、正確BOSS／野外狀態與入口原因。'),
 ('新委託結算','CQ033靈幣僅列三選二選項；CQ046～049採本輪最終獎勵，實際領獎逐件核對、防止重領。'),
 ('新增主線續接','保留030／031／032／033A；已接入033B～036B完整805節點及034A～036A完整709節點。兩線分別有固定首動特殊必敗戰、免費寵物復原、逐段對話、合法移動／傳送與NPC會合；A線命符及陸家旗標保留，不給B線。修正033A同行任務導航、舊交戰重複按鈕與對話立繪。'),
 ('補充規則','差10級七種保底與12人形向上取整、差11級全0；主根分段55／30／12／3與合法武器偏好70／30及空池後備均已補入。NPC80組境界基線、品質與流派倍率已採本輪正式原表；裝備品質依55／25／12／5／2／1在現有成品中抽取，不套候選能力倍率。'),
 ('戰鬥判定','前後排60／40、護盾反擊一次、破夢先讀睡眠、新狀態一次消耗、長右轉階同體鎖血及控制免疫。'),
 ('既有醫館保留','驗證夥伴／寵物手動救治、原費用、30遊戲分鐘後自動返回；沒有回退1日規則。'),
 ('UI與存檔','主黃／支藍／委綠、平民愛心移除、可製作置頂、裝備比較、原檔匯入與新旗標重載。')]
pending=meta['pending']
bugbody=warning+'<h2>已修復／已保留並回歸驗證</h2><ol>'+''.join('<li><b>'+e(a)+'</b>：'+e(b)+'</li>' for a,b in fixes)+'</ol><h2>待補與未完成原因</h2><p>CQ-DZ-046～049已依本次確認解除待補，四條均完成實裝及獎勵測試。</p><ol>'+''.join('<li><b>'+e(x['id'])+'</b>：'+e(x['reason'])+'</li>' for x in pending)+'</ol><h2>不補造的未定內容</h2><p>命符真正破碎／復活、靈獸之骨後續用途、未公開宗主及災獸之主身份保持未定；未替使用者新增故事。</p><h2>本次解除待補與仍未完成的範圍</h2><ul><li>A線034A～036A及B線033B～036B均已依本次完整原稿實裝，兩線各有032至038完整連續戰鬥流程驗收。火紅蓮及九珠陰雷採指定劇情效果，不另創一般功法資料。</li><li>問道跨境界入口已開放，NPC80組基線、九層、品質、八流派、靈根／武器／合法功法、現有裝備抽選及1V1結算均有測試。裝備候選倍率只保留資料，依本次指示不修改玩家或成品能力。</li><li>新三寵從孵蛋到全境界成長：缺起始及連續成長八核；技能由隔離測試寵實驗，選新種不扣蛋。</li><li>圖鑑第一階段可查；尚無來源的欄位標待補。素材圖示為獨立SVG占位，需美術驗收。</li></ul>'
page('BUG修復與待補清單.html','V0.7.3 BUG修復與待補清單',bugbody)
writejson('BUG修復與待補清單.json',{'fixed':[{'item':a,'detail':b} for a,b in fixes],'pending':pending})

testbody=warning+summary+'<h2>測試結果與界限</h2><p>共'+str(total)+'項自動化檢查通過（新增'+str(len(newtests))+'＋既有回歸'+str(sum(r['checks'] for r in reg))+'）。另有16組BOSS解析器實戰、1場UI自動戰鬥、4尺寸畫面及單檔離線驗證。這些是工程證據；38項完整功能與數值平衡尚未取得玩家驗收。</p><h2>長右BOSS</h2><p>固定種子1732～1739，沈玄川／柳清妍各8組，正式NPC八核＋測試999原始八核、不喝藥、不加作弊傷害；全部15～18回合獲勝。實際點擊自動戰鬥第'+str(live['live']['round'])+'回合通過第二階段並獲勝。50%鎖血2250、MP1200、首動轟雷、次動洪水、潮濕優先潮閃引雷、硬控免疫另有單項檢查。</p><p>此結果只對候選八核及此隊伍／操作有效，不保證所有玩家配置都能30回合擊殺；長右獨立隱藏值與正式戰力仍待定。</p><p><a href="長右30回合實戰資料.json">16組完整戰鬥資料</a>　<a href="長右實際自動戰鬥驗收.json">UI實戰紀錄</a></p><img src="長右戰鬥畫面.png" alt="長右完整戰鬥畫面"><h2>新增流程與既有回歸</h2><ul>'+''.join('<li>'+e(r['name'])+'：'+str(r['passed'])+'／'+str(r['checks'])+'檢查。<a href="'+e(r['file'])+'">原始結果</a></li>' for r in reg)+'</ul><p>原28段主線、12條支線、25委託由原回歸腳本在本輪新HTML實際走流程。舊工作檔只作測試用存檔種子，沒有作施工底稿。</p><h2>本次補充B線與兩項機率</h2><p>033B三處調查六種順序、林夏于追擊離隊、九珠陰雷強制首動／免費特殊結算、滿貫丹實際服下才恢復、三波每場結算與失敗續接、036B調查傳送陣與五人會合，皆有逐項測試。另實際連續從032選B到038長右結算；此流程案例使用隔離角色提高八核以滿足地圖門檻，只驗收流程，不能當作平衡結論。</p><p><a href="B線與補充定案測試結果.json">本次完整測試結果</a>　<a href="B線完整對話805節點.txt">B線805節點文字</a>　<a href="補充定案_修為與問道.json">修為與問道補充規則</a></p><img src="B線九珠陰雷戰鬥畫面.png" alt="B線九珠陰雷劇情戰"><h2>本次A線與NPC公式補完</h2><p>A線709節點原稿已接入，實際從032選A、033A兩場戰鬥、034A固定火紅蓮必敗與免費寵物復原、035A陸景和救援／命符／無戰利品黑衣人戰、036A四人入窟會合，再到037／038長右結算，保留A線專屬物品與紀錄且不完成B線。</p><p>問道測試包含80組正式NPC基線、築基及金丹九層、五種可抽品質及弱者通用品質、八流派／額外效果、每核獨立±5%、1200個完整合法對手、八流派各20000次武器抽樣、100000次裝備品質抽樣及缺品質重新分配。實際1V1勝利發33點，連勝結算最高37、失敗歸0；禁止道具／戰前效果／逃跑，存檔後對手不重抽。</p><p>NPC品質只乘自身基線，裝備只加成品記錄值一次。普通1／優良1.1／精品1.2／珍稀1.35／極品1.5／完美1.7僅保存未來候選，未改玩家裝備或成品能力。</p><p><a href="A線與NPC公式測試結果.json">A線／NPC完整測試結果</a>　<a href="A線完整對話709節點.txt">A線709節點原稿</a>　<a href="NPC通用生成正式資料.json">NPC正式生成資料與候選表</a></p><img src="A線必敗戰結算.png" alt="A線必敗戰結算"><img src="問道跨境界戰實際結算.png" alt="問道跨境界戰結算"><h2>全部新增測項</h2>'
for t in newtests:
    testbody+='<details><summary>✓ '+e(t['id']+' '+t['name'])+'</summary><pre>'+e(json.dumps(t.get('detail'),ensure_ascii=False,indent=2))+'</pre></details>'
testbody+='<h2>離線與畫面</h2><p>單檔'+str(game.stat().st_size)+'位元組（約'+str(round(game.stat().st_size/1024/1024,1))+' MiB），file://開啟且封鎖HTTP/HTTPS；0外網請求、0頁面執行錯誤，14張新圖皆為內嵌且成功解碼。四視窗1440×1000、1024×768、768×1024、390×844確認特殊／高危／高危特角尾叉可見、頁面無水平溢出。390寬沿既有全景縮放，並非新增手機版佈局。</p><p><a href="單檔離線驗收.json">離線結果</a>　<a href="四尺寸畫面驗收.json">四尺寸紀錄</a></p><img src="東州新地圖.png" alt="新東州地圖"><img src="圖鑑素材反查.png" alt="火尾毛來源反查"><h2>正式檔保護</h2><p>正式main仍為'+e(baseline['commit'])+'，正式工作目錄乾淨；下列五檔SHA-256前後一致。只建立本地test/v0.7.3-20261017分支，尚未commit或push，未變更GitHub設定或發布。</p><pre>'+e(json.dumps(protected,ensure_ascii=False,indent=2))+'</pre><h2>交付檔驗證</h2><pre>'+e(json.dumps(manifest,ensure_ascii=False,indent=2))+'</pre>'
if publication:testbody=testbody.replace('正式main仍為'+e(baseline['commit'])+'，正式工作目錄乾淨；','正式母檔基準為'+e(baseline['commit'])+'；GitHub主分支另增加獨立測試子目錄提交，正式入口與五個受保護檔案未變。').replace('只建立本地test/v0.7.3-20261017分支，尚未commit或push，未變更GitHub設定或發布。','已另提交並推送preview/v0.7.3測試子目錄；未變更Pages設定或正式遊戲版本。遊戲內容提交：'+e(publication['gameCommit']))
page('完整測試及驗收報告.html','V0.7.3 完整測試及驗收報告',testbody)

readme='''《九州修仙錄》0.7.3 獨立測試交付

基準：最新0.7.2「九州修仙錄_測試分支.html」，未使用舊HTML重做。
本地Git分支：test/v0.7.3-20261017；未commit、未push、未發布。
正式0.7.2母檔及GitHub保持不變。

遊玩：開啟「九州修仙錄_V0.7.3_獨立測試版.html」。此單一HTML已包含圖片，可離線遊玩，約500.7MB。
也可開啟「Git測試分支/index.html」；這是同一版的拆分資源形式，必須保留該資料夾內assets與new-assets。

快速驗收：建立角色時名稱填「測試999」。進遊戲後按主介面「本輪測試入口」，可選長右、A/B分支、或新地圖與委託情境。這些僅是隔離測試入口，會改動該測試角色進度，不會改正式存檔。
普通角色可沿既有主線遊玩，再接新增主線；A／B兩線均已完成032至038連續流程實戰。問道檯跨境界入口已開放，金丹玩家暫關；對手是下一個大境界一層至圓滿。

存檔：測試HTML採獨立儲存前綴。若要帶入原角色，請使用遊戲內匯入原存檔副本；仍請自行保留原匯出檔。瀏覽器不會自動把正式版角色寫入此測試空間。

請先看「逐項施工工程覆蓋表.html」「BUG修復與待補清單.html」「完整測試及驗收報告.html」。
新增37項系統檢查、26項擴充流程、13項B線／補充定案及22項A線／NPC檢查通過；既有95項回歸保留。
長右16組候選數值實戰15～18回合通過，另實際操作自動戰鬥第16回合獲勝。
測試通過不代表待補功能完成；玩家尚未驗收整版。

主要待補：新三寵起始及連續成長八核、部分圖鑑來源與美術驗收、新狀態非潮濕取得方式、支線016記載衝突。A／B完整主線、修為差10級保底、問道NPC正式原表及裝備抽樣均已補齊。裝備新能力倍率僅保存未來候選，不作用於現有成品。
CQ046～049本輪最終目標及報酬已實裝，已從待補移除。
潮閃引雷限制長右專屬；沒有重加音樂。
'''
if publication:readme=readme.replace('本地Git分支：test/v0.7.3-20261017；未commit、未push、未發布。','本地施工分支：test/v0.7.3-20261017。另已依授權commit/push GitHub獨立測試子目錄。').replace('正式0.7.2母檔及GitHub保持不變。','正式0.7.2母檔及正式入口保持不變。測試網址：'+publication['url']).replace('快速驗收：','快速驗收（GitHub亦同）：')
(O/'閱讀我_先看這裡.txt').write_text(readme,'utf8')
page('閱讀我_先看這裡.html','《九州修仙錄》0.7.3 獨立測試交付',warning+summary+'<pre>'+e(readme)+'</pre><h2>來源與驗證</h2><p>施工規格：使用者2026-10-17工作檔＋本輪潮閃引雷專屬及四條委託最終修正。另已併入使用者本輪補充的A線034A～036A709節點、B線033B～036B805節點、差10級保底、NPC正式基線／品質／八流派與裝備品質抽樣；文件內舊待補標記已按本輪明確指示覆蓋；未把文件內其他未定提議升格定案。</p><p>測試基準SHA-256：<code>'+baseline['protected']['九州修仙錄_測試分支.html']['sha256']+'</code></p><p><a href="交付驗證清單.json">交付驗證清單</a>　<a href="正式檔案保護驗證.json">正式檔保護驗證</a></p>')
print(json.dumps({'protected':True,'coverage':dict(statuscounts),'new':len(newtests),'regression':sum(r['checks'] for r in reg),'total':total,'branch':manifest['branch'],'gameBytes':game.stat().st_size},ensure_ascii=False))
