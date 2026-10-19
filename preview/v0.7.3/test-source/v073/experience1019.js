(function(){'use strict';
const N=JZ073,R=JZR,U=JZ071,X=N.experience1019={version:1},number=v=>Math.max(0,Math.floor(Number(v)||0));
let scanning=false,legacyBattle=0,travel=0;
const souvenirNames=Object.keys(JZW.data.souvenirs),teaNames=['焦葉粗茶','雲芽清茶','玉露凝香','悟道仙茗'];
const quantity=v=>number(typeof v==='object'?v?.count:v);
// Keep the original save fields and counters; only normalize the shared pool.
v070EnsureExperience=function(){if(!S)return;const total=Math.min(120,number(S.experience)+number(S.experienceHidden));S.experience=Math.min(100,total);S.experienceHidden=Math.max(0,total-100);const c=S.experienceCounters??={};c.commission=number(c.commission);c.gather=number(c.gather);c.wildMinutes=number(c.wildMinutes);c.monster??={};};
v070TotalExperience=function(){v070EnsureExperience();return S.experience+S.experienceHidden;};
X.add=(n,why)=>{v070EnsureExperience();const gain=Math.min(number(n),120-v070TotalExperience()),total=v070TotalExperience()+gain;S.experience=Math.min(100,total);S.experienceHidden=Math.max(0,total-100);if(gain&&why)log('📘 '+why+'：歷練＋'+gain+'。');return gain;};
v070AddExperience=function(n,why){return legacyBattle?0:X.add(n,why);};
v070SpendExperience=function(n){const total=v070TotalExperience(),spent=Math.min(Math.floor(total/10)*10,Math.floor(number(n)/10)*10),left=total-spent;S.experience=Math.min(100,left);S.experienceHidden=Math.max(0,left-100);return spent;};
X.petId=p=>{const d=R.petData(p);return d.v3TouchId??=(crypto.randomUUID());};
X.eligibleNpc=n=>{const d=U.npcs[n]||JZNEXT.npcs[n];return !!d&&!d.noAffinity&&d.affinityMax!==0;};
X.state=()=>{v070EnsureExperience();if(S.experienceV073)return S.experienceV073;const x=S.experienceV073={schema:1,souvenirs:{},quests:{},npc:{},pets:{},tea:{},teaEarned:0,receipts:[]};
 // Past quest/heart/star awards cannot be reconstructed safely. Seed their
 // milestones without replaying them. Souvenirs were confirmed never paid.
 for(const q of S.quests||[])if(q.claimed)x.quests[q.id]=true;
 for(const [n,a] of Object.entries(S.npcAffinity||{}))if(X.eligibleNpc(n))x.npc[n]={five:a>=50,ten:a>=100};
 for(const p of S.pets||[]){const d=R.petData(p);x.pets[X.petId(p)]={five:d.affection>=50,ten:d.affection>=100,star:d.stars>=5};}
 for(const t of teaNames)if(S.teaHistory?.[t]){x.tea[t]=true;x.teaEarned+=t==='悟道仙茗'?4:1;}x.teaEarned=Math.min(7,x.teaEarned);return x;};
X.receipt=(kind,key,amount,label)=>{const x=X.state(),gain=X.add(amount,label);x.receipts.push({kind,key,amount,credited:gain,at:r4GameMinutes()});if(x.receipts.length>200)x.receipts.splice(0,x.receipts.length-200);return gain;};
X.souvenir=n=>{const x=X.state();if(!souvenirNames.includes(n)||x.souvenirs[n])return false;x.souvenirs[n]=true;X.receipt('souvenir',n,n==='［特殊］月玉珮'?5:1,'首次取得'+n);return true;};
X.scan=()=>{if(!S||scanning)return;scanning=true;try{const x=X.state(),proof=new Set();for(const n of souvenirNames)if(['souvenirs','items','special','materials','gearInventory'].some(b=>quantity(S[b]?.[n])>0))proof.add(n);
 for(const [npc,rows] of Object.entries(JZNEXT.gifts||{}))rows.forEach((r,i)=>{if(S.npcGiftClaims?.[npc+':'+i]&&souvenirNames.includes(r[1]))proof.add(r[1]);});
 // The complete jade consumes both half-jades, which are themselves souvenirs.
 if(proof.has('［特殊］月玉珮')){proof.add('［特殊］半月水玉');proof.add('［特殊］半月山玉');}
 if(number(S.eastWord?.wendao?.passed)>=10)proof.add('［特殊］問道茶壺');
 for(const n of proof)X.souvenir(n);
 for(const q of S.quests||[]){if(!q.claimed||x.quests[q.id])continue;x.quests[q.id]=true;if(q.type==='主線'||q.type==='支線')X.receipt('quest',q.id,1,'完成［'+q.type+'］'+q.title);else if(q.type==='委託'){const c=S.experienceCounters;c.commission++;if(c.commission>=5){const times=Math.floor(c.commission/5);c.commission%=5;X.receipt('commission',q.id,times,'累積完成委託');}}}
 for(const [n,a] of Object.entries(S.npcAffinity||{})){if(!X.eligibleNpc(n))continue;const m=x.npc[n]??={};if(a>=50&&!m.five){m.five=true;X.receipt('npc',n+':5',1,n+'好感達到5心');}if(a>=100&&!m.ten){m.ten=true;X.receipt('npc',n+':10',2,n+'好感達到10心');}}
 for(const p of S.pets||[]){const d=R.petData(p),id=X.petId(p),m=x.pets[id]??={};if(d.affection>=50&&!m.five){m.five=true;X.receipt('pet',id+':5',1,p.name+'好感達到5心');}if(d.affection>=100&&!m.ten){m.ten=true;X.receipt('pet',id+':10',2,p.name+'好感達到10心');}if(d.stars>=5&&!m.star){m.star=true;X.receipt('pet',id+':star5',3,p.name+'首次達到5星');}}
 }finally{scanning=false;}};
for(const [obj,key] of [[R,'ensure'],[R,'save'],[window,'r4WriteSave'],[window,'render'],[window,'renderPage'],[window,'r56SyncQuestArchive']]){const old=obj[key];if(typeof old!=='function')continue;obj[key]=function(){if(key==='ensure'){const out=old.apply(this,arguments);X.scan();return out;}X.scan();const out=old.apply(this,arguments);X.scan();return out;};}
// Observe the private NPC/crafting grant paths as well as public grants.
const give=R.give;R.give=function(){X.scan();const out=give.apply(this,arguments);X.scan();return out;};
const claim=jzClaimNpcGift;jzClaimNpcGift=function(){X.scan();const out=claim.apply(this,arguments);X.scan();return out;};
// The tutorial formerly added two points directly, outside the common award.
// It now follows the same one-point main-quest rule as subsequent chapters.
R56_QUESTS.tutorial2.reward=String(R56_QUESTS.tutorial2.reward).replace(/歷練[×＋+]2/g,'歷練＋1');
r5CompleteTutorial2=function(){const q=S.quests?.find(q=>q.id==='tutorial2');if(!q?.done||q.claimed)return false;X.scan();q.reward=String(q.reward||'').replace(/歷練[×＋+]2/g,'歷練＋1');q.claimed=true;q.pinned=false;S.coins+=300;S.items['［初階］氣血藥水']=number(S.items['［初階］氣血藥水'])+2;S.items['［初階］靈力藥水']=number(S.items['［初階］靈力藥水'])+2;S.flags.peopleUnlocked=S.flags.questUiUnlocked=true;S.questState.tutorial2??={};S.questState.tutorial2.claimed=true;r56SyncQuestArchive(q);currentPage='people';R.save();render();return true;};
reportTutorial2=function(){return r5CompleteTutorial2();};
// Half-jades live in the souvenir bag, rather than the material bag.
const halves=['半月水玉','半月山玉'],jadeRecipe=req=>halves.every(n=>String(req).includes(n));
const countMaterial=JZW.materialCount,spendMaterial=JZW.spendMaterial;
JZW.materialCount=function(n){if(!halves.includes(U.short(n)))return countMaterial.apply(this,arguments);return ['items','special','materials','souvenirs'].reduce((v,b)=>v+Object.entries(S[b]||{}).filter(([k])=>U.short(k)===U.short(n)).reduce((a,[,q])=>a+quantity(q),0),0);};
JZW.spendMaterial=function(n,q){if(!halves.includes(U.short(n)))return spendMaterial.apply(this,arguments);if(JZW.materialCount(n)<q)return false;for(const b of ['souvenirs','special','items','materials'])for(const [k,v] of Object.entries(S[b]||{})){if(U.short(k)!==U.short(n))continue;const used=Math.min(q,quantity(v));S[b][k]=quantity(v)-used;q-=used;if(!q)return true;}return false;};
const hasIngredients=r59HasIngredients,consumeIngredients=r59ConsumeIngredients,missingIngredients=r512Missing;
r59HasIngredients=function(req){return jadeRecipe(req)?r59ParseReq(req).every(([n,c])=>JZW.materialCount(n)>=c):hasIngredients.apply(this,arguments);};
r59ConsumeIngredients=function(req){if(!jadeRecipe(req))return consumeIngredients.apply(this,arguments);if(!r59HasIngredients(req))return false;X.scan();for(const [n,c] of r59ParseReq(req))JZW.spendMaterial(n,c);return true;};
r512Missing=function(req){return jadeRecipe(req)?r59ParseReq(req).filter(([n,c])=>JZW.materialCount(n)<c).map(([n,c])=>n+' 缺 '+(c-JZW.materialCount(n))).join('、'):missingIngredients.apply(this,arguments);};
r58TeaFirst=function(name){const x=X.state();S.teaHistory??={};if(!teaNames.includes(name)||S.teaHistory[name]||x.tea[name])return false;S.teaHistory[name]=true;x.tea[name]=true;const amount=Math.min(7-x.teaEarned,name==='悟道仙茗'?4:1);x.teaEarned+=amount;if(amount)X.receipt('tea',name,amount,'首次品嘗'+name);return true;};
X.recordBattle=(b,win)=>{if(!b||b.experience1019Recorded)return;b.experience1019Recorded=true;if(!win||b.jzLab||b.jzSpar||b.jzWendao||b.jzPetMode||b.tutorialCase||b.jz073PlotLoss||b.jz073NoLoot)return;X.scan();const c=S.experienceCounters.monster;
 for(const e of b.enemyTeam||[]){if(e.hp>0)continue;const name=N.canonical(e.name),kind=e.hostileKind||N.kind(e),monster=!!JZMON.byName[name]||['妖王種','神獸種','災獸種'].includes(kind);
 if(!monster){if(['長老級','道祖級'].includes(kind))X.receipt('battle',kind,5,'擊殺'+kind);else if(/州府統領/.test([e.identity,e.role,e.npcRole,kind,JZNEXT.npcs[name]?.identity,U.npcs[name]?.identity].join(' ')))X.receipt('battle',name,3,'戰勝州府統領');continue;}
 if(['一般種','特殊種'].includes(kind)&&JZ072.rank(e.realm)<JZ072.rank(S.realm))continue;
 const direct={'妖王種':1,'神獸種':5,'災獸種':5}[kind];if(direct){X.receipt('battle',name,direct,'擊殺'+kind);continue;}
 const category=kind==='高危種'?'高位種':kind==='高危種(特)'?'高危種（特）':kind,need={'一般種':30,'特殊種':20,'高位種':10,'高危種（特）':5}[category];if(!need)continue;c[category]=number(c[category])+1;if(c[category]>=need){c[category]-=need;X.receipt('battle',category,1,'累積擊殺'+need+'隻'+category);}
 }};
const record=U.recordBattle;U.recordBattle=function(b,win){X.recordBattle(b,win);return record.apply(this,arguments);};
// The old single-foe reward handler still runs for cultivation/loot. Suppress
// only its experience award/counter mutation, preserving all other settlement.
const win=battleWin;battleWin=function(){const b=battle;X.recordBattle(b,true);v070EnsureExperience();const counters=structuredClone(S.experienceCounters.monster);legacyBattle++;try{return win.apply(this,arguments);}finally{legacyBattle--;S.experienceCounters.monster=counters;X.scan();}};
const gather=gatherNearby;gatherNearby=function(){X.scan();const before=Object.values(S.materials||{}).reduce((a,v)=>a+quantity(v),0),out=gather.apply(this,arguments),after=Object.values(S.materials||{}).reduce((a,v)=>a+quantity(v),0);if(after>before){const c=S.experienceCounters;c.gather++;if(c.gather>=30){c.gather-=30;X.receipt('gather','30',1,'累積採集30次');}R.save();}return out;};
const move=moveTo;moveTo=function(){travel++;try{return move.apply(this,arguments);}finally{travel--;}};
const advance=r4AdvanceMinutes;r4AdvanceMinutes=function(mins,opt){X.scan();const place=S.place,before=r4GameMinutes(),out=advance.apply(this,arguments),elapsed=Math.max(0,r4GameMinutes()-before);if(!travel&&place===S.place&&placeType(place)==='野外'&&elapsed){const c=S.experienceCounters;c.wildMinutes+=elapsed;const times=Math.floor(c.wildMinutes/1440);if(times){c.wildMinutes%=1440;X.receipt('wild','24h',times,'野外累積遊歷'+times+'日');}}return out;};
const useToken=n=>{if(U.short(n)!=='歷練令牌')return null;if(battle||!R.count(n)||!R.take(n,1))return false;X.receipt('token',n,3,'使用歷練令牌');R.save();render();return true;};
for(const key of ['useItem'])for(const ob of [R,JZW]){const old=ob[key];if(typeof old!=='function')continue;ob[key]=function(n){const out=useToken(n);return out===null?old.apply(this,arguments):out;};}
for(const ob of [R,JZW]){const old=ob.itemDescription;if(typeof old==='function')ob.itemDescription=function(n){if(U.short(n)==='歷練令牌')return '使用後獲得3點歷練。';return old.apply(this,arguments);};}
const training=renderTraining;renderTraining=function(){return training.apply(this,arguments).replace(/\s*<span class="tiny muted">（另有隱藏儲備）<\/span>/g,'');};
R511_CODEX.歷練=['歷練來自修行中的遊歷與成長，可投入突破或破境，提高成功率。',[],
 '<p>平常顯示最高100／100；超過的歷練最多保留20點。消耗時會從總量扣除，保留的歷練自動補回顯示值。超過總上限的部分不再累積。</p><p>每次可投入10點的整數倍。每消耗10點，突破或破境成功率增加1個百分點；即使失敗也會消耗。</p><h3>任務與品茗</h3><p>每完成一個主線或支線，獲得1點；每完成5次委託，獲得1點。每種茶首次品嘗獲得1點，首次喝到悟道仙茗額外獲得3點；品茗最多提供7點。</p><h3>戰鬥</h3><p>一般種每30隻、特殊種每20隻、高危種（高位種）每10隻、高危種（特）每5隻，各獲得1點。妖王種每隻1點；神獸種與災獸種每隻5點。一般種或特殊種若低於自己的大境界，該次擊殺不累積。</p><p>擊殺長老級或道祖級敵人獲得5點；戰勝或擊殺州府統領獲得3點，同一場不重複計算。</p><h3>探索與培養感情</h3><p>採集每30次獲得1點。在野外累積24小時遊戲時間獲得1點，可以跨野外區域累積；往返城鎮與野外的移動時間不計入。</p><p>有好感度的NPC與每一隻寵物，首次達到5心獲得1點，10心再獲得2點。每隻寵物首次達到5星，獲得3點。</p><h3>紀念品與道具</h3><p>每種紀念品首次取得獲得1點；月玉珮首次取得獲得5點。相同紀念品再次取得不會重複給予歷練。歷練令牌使用後獲得3點。</p>', ['突破與破境','茶館','NPC','寵物養成']];
const history=JZ072.versionHistory;JZ072.versionHistory=function(){history();document.getElementById('modalBody')?.insertAdjacentHTML('afterbegin','<section class="card"><h2>10/19 歷練修正</h2><h3>新增</h3><p>紀念品首次取得歷練，月玉珮5點，其餘每種1點；已持有或已領取的紀念品補發一次。</p><h3>改動</h3><p>任務、委託、好感、寵物升星、採集與野外遊歷依歷練規則累積。</p><h3>BUG修復</h3><p>品茗的7點上限獨立計算；多隻敵人的歷練逐隻結算；低於自身大境界的一般與特殊種不累積。存讀檔不重複發放，投入量維持10點整數倍。</p></section>');};
})();
