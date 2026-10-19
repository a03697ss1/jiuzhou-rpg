(function(){'use strict';const N=JZ073,R=JZR,W=JZW,V=JZV2,E=N.esc;
const short=n=>String(n||'').replace(/^(普通|優良|精品|珍稀|極品|完美)(?=［)/,'').replace(/^［[^］]+］/,'');
N.revision24Descriptions={
戰意玉:'特殊裝備進階素材。',獸魂晶:'寵物升星核心素材',獸靈果:'寵物煉丹素材',靈獸露:'寵物煉丹素材',
獸靈果丹:'可永久提升該寵物八核選一數值＋5；選擇氣血或靈力時提升＋20。配方：獸靈果×5。',
靈獸露丹:'可永久提升該寵物的屬性傷害＋1%，每種屬性最高提升10%。配方：靈獸露×5。',
寵物自選專屬技能箱:'打開後可自選該寵物合法池技能。',獸技殘頁:'妖物技能相關素材，可用於特殊合成。',
靈契玉:'進階寵物裝備用材料',萬獸徽記:'萬獸檯授予高階御獸修士的特殊徽記。可用於五星寵物的特殊突破，亦可作為萬獸檯高級兌換所需的珍貴憑證。',
寵物秘術卷軸:'直接提升寵物一層境界，無法用於寵物破境。',
凝力丹:'戰鬥中使用，使自身攻＋8%，持續3回合。',凝道丹:'戰鬥中使用，使自身道＋8%，持續3回合。',靈息丹:'戰鬥中使用，使自身命＋8%，持續3回合。',清靈丹:'戰鬥中使用，使自身效果命中＋12，持續3回合。',鎮心丹:'戰鬥中使用，使自身效果抵抗＋12，持續3回合。'
};
const desc=W.itemDescription;W.itemDescription=function(n){if(n==='［初階］寵物用破境丹')return '寵物境界突破與破境率＋5%';if(n==='［中階］寵物用破境丹')return '寵物境界突破與破境率＋8%';return N.revision24Descriptions[short(n)]||desc.apply(this,arguments);};
// Explicit final gear values; NPC quality and the existing hidden rank scaling stay independent.
const data=[
['問心劍','武',{atk:29,dao:15,hit:13},'每場戰鬥首次使用功法時，該次功法命中率＋10個百分點'],
['破軍刀','武',{atk:36,hit:8,agi:-4},'攻擊氣血高於70%的目標時，直接傷害＋6%'],
['問道槍','武',{atk:31,agi:14,hit:10},'連續攻擊同一目標時，自第二次開始造成的直接傷害＋4%；更換目標後重新計算'],
['逐星弓','武',{atk:25,dao:14,agi:7,hit:15,critRate:3},'暴擊率＋3%'],
['破境拳套','武',{atk:22,agi:24,hit:15},'自身身高於目標身時，直接傷害額外＋5%'],
['鎮岳錘','武',{hp:160,atk:40,def:8,agi:-10},'自身氣血高於50%時，錘類功法造成的直接傷害＋5%'],
['問靈寶珠','武',{mp:75,dao:38,daoDef:7,agi:-8,hit:-3},'道術類功法靈力消耗－6%'],
['清虛道扇','武',{mp:35,dao:20,agi:25,hit:8},'使用增益／輔助或身法功法後，自身身＋6%，持續2回合，不疊加'],
['納靈葫蘆','武',{mp:100,dao:22,daoDef:10,effectResist:8},'每場戰鬥首次低於30%最大靈力時，立即恢復最大靈力的10%，每場僅觸發1次'],
['玄機靈傘','武',{atk:16,dao:27,agi:18,hit:9,daoDef:6},'使用攻擊功法後，下次增益／輔助功法效果持續時間＋1回合；觸發後消耗，不能連續累積'],
['問道護符','飾',{hp:70,mp:35,def:5,daoDef:5},'每場戰鬥首次受到異常狀態時，效果抵抗＋10，持續2回合'],
['戰心指環','戒',{atk:15,hit:8,critRate:2},'成功暴擊後，攻＋6%，持續2回合，不疊加'],
['問心戒','戒',{dao:16,hit:7,effectHit:6},'對帶有異常狀態的目標造成道術直接傷害＋5%'],
['問道佩','飾',{hp:90,mp:50,agi:6,hit:6},'每場戰鬥首次氣血低於50%時，效果抵抗＋12，持續2回合'],
['破境項鍊','項',{atk:18,dao:18,hit:8},'攻擊境界高於自身的目標時，直接傷害＋6%'],
['道心靈墜','項',{mp:70,dao:20,daoDef:8,effectHit:8},'使用道術類功法後，下一次治療或增益／輔助功法的靈力消耗－10%，觸發後消耗'],
['問天玉佩','飾',{mp:260,dao:48,daoDef:32,hit:15,effectHit:12},'道術直接傷害＋8%；使用道術功法時靈力消耗－5%'],
['破天戰佩','飾',{hp:420,atk:52,def:34,hit:16,critRate:3},'物理直接傷害＋8%；自身氣血高於50%時，暴擊傷害＋10%']
];N.gear24=data;
for(const [name,slot,stats,effect] of data){const n='［特殊］'+name,g={...stats,slot,source:'問道檯',hidden:/問天玉佩|破天戰佩/.test(name)?'特殊·仙位':'特殊·中位',effect};R546_GEAR_FULL[n]=g;R4_GEAR_STATS[n]={...g};}
const aliases={'清風靈葫':'納靈葫蘆','靈水傘':'玄機靈傘'};
N.migrateGear24=()=>{if(!S)return;const rename=n=>{for(const [a,b] of Object.entries(aliases))if(String(n).endsWith('［特殊］'+a))return n.slice(0,-a.length)+b;return n;};
for(const bag of ['gearInventory','special'])for(const [old,v] of Object.entries(S[bag]||{})){const n=rename(old);if(n!==old){const count=x=>typeof x==='object'?Number(x.count||0):Number(x||0);S[bag][n]=count(S[bag][n])+count(v);delete S[bag][old];}}
for(const p of [S,...(S.partners||[]),...Object.values(JZ072.state().partnerGrowth||{})]){for(const k of Object.keys(p.equipment||{}))p.equipment[k]=rename(p.equipment[k]);for(const field of ['shared','intrinsic'])for(const k of Object.keys(p.jz072?.[field]||{}))p.jz072[field][k]=rename(p.jz072[field][k]);}
const purchased=S.eastWord?.wendao?.purchased;if(purchased)for(const old of Object.keys(purchased)){const n=rename(old);if(n!==old){purchased[n]=purchased[n]||purchased[old];delete purchased[old];}}
};const ensure=V.ensure;V.ensure=function(){const out=ensure.apply(this,arguments);N.migrateGear24();return out;};
const pills=['凝力丹','凝道丹','靈息丹','清靈丹','鎮心丹'];V.spec.arenas.ask_platform.shop.pills=pills.map(name=>({name:'［初階］'+name,price:35,effect:N.revision24Descriptions[name]}));
V.askRows=[['［特殊］問道殘頁',32,false],['［特殊］戰意玉',16,false],...data.map(([n])=>['［特殊］'+n,/問天玉佩|破天戰佩/.test(n)?1280:320,true]),...pills.map(n=>['［初階］'+n,35,false])];N.wendaoSourceRows1018=V.askRows.map(([n,price])=>[n,price]);
W.shop=()=>{if(battle||S.place!=='問道檯')return;V.ensure();const wd=S.eastWord.wendao;showModal('問道檯兌換商店','<p>問道點數：'+V.points()+'</p>'+V.askRows.map(([n,price,once])=>'<section class="card jz24-shop-item">'+N.itemImage1018(n)+'<b>'+E(n)+'</b><p>'+price+' 問道點數／'+(R546_GEAR_FULL[n]?'件':pills.includes(short(n))?'顆':'個')+' · '+(once?'每份存檔限兌換一次':'可重複兌換')+'</p>'+(R546_GEAR_FULL[n]?'<p>'+r4BonusText(n)+'</p>':'')+'<p>'+E(R546_GEAR_FULL[n]?.effect||W.itemDescription(n))+'</p><button '+(V.points()<price||once&&wd.purchased[n]?'disabled':'')+' onclick="JZW.purchase(\''+n+'\')">'+(once&&wd.purchased[n]?'已兌換':'兌換')+'</button></section>').join(''));};
// Renaming the shop row also updates its purchase path: the closure holds this same array.
for(const row of R.beastShopRows)if(short(row[0])==='獸技秘卷')row[0]='［特殊］獸技殘頁';
const sale=R.saleBlocked;R.saleBlocked=function(n){return String(n).includes('［特殊］')||/自選.*箱|［任務］/.test(n)||sale.apply(this,arguments);};
const quote=R.sellQuote;R.sellQuote=function(merchant,n){if(short(n)==='功法殘卷'&&!R.saleBlocked(n)&&R.merchants[merchant]&&R.count(n))return 200;return quote.apply(this,arguments);};
for(const list of Object.values(RECIPES))for(const row of list){if(row[0]==='［特殊］獸靈果丹')row[1]='獸靈果×5';if(row[0]==='［特殊］靈獸露丹')row[1]='靈獸露×5';}
const petMaterials=['獸靈果','靈獸露'],materialKeys=n=>[...new Set(['items','special','materials'].flatMap(b=>Object.keys(S[b]||{})).filter(k=>short(k)===n))];
N.petMaterialCount24=n=>materialKeys(short(n)).reduce((v,k)=>v+R.count(k),0);
N.spendPetMaterial24=(n,q)=>{const s=short(n);if(N.petMaterialCount24(s)<q)return false;for(const k of materialKeys(s)){const take=Math.min(q,R.count(k));if(take)R.take(k,take);q-=take;if(!q)break;}return true;};
const wCount=W.materialCount,wSpend=W.spendMaterial;W.materialCount=function(n){return petMaterials.includes(short(n))?N.petMaterialCount24(n):wCount.apply(this,arguments);};W.spendMaterial=function(n,q){return petMaterials.includes(short(n))?N.spendPetMaterial24(n,q):wSpend.apply(this,arguments);};
const has=r59HasIngredients,consume=r59ConsumeIngredients;const petRecipe=req=>petMaterials.some(m=>String(req).includes(m));
r59HasIngredients=function(req){return petRecipe(req)?r59ParseReq(req).every(([n,c])=>W.materialCount(n)>=c):has.apply(this,arguments);};
r59ConsumeIngredients=function(req){if(!petRecipe(req))return consume.apply(this,arguments);if(!r59HasIngredients(req))return false;for(const [n,c] of r59ParseReq(req))W.spendMaterial(n,c);return true;};
const missing=r512Missing;r512Missing=function(req){return petRecipe(req)?r59ParseReq(req).filter(([n,c])=>W.materialCount(n)<c).map(([n,c])=>n+' 缺 '+(c-W.materialCount(n))).join('、'):missing.apply(this,arguments);};
R.craftPetDan=n=>{const m={'［特殊］獸靈果丹':'獸靈果','［特殊］靈獸露丹':'靈獸露'}[n];if(battle||!m||!N.spendPetMaterial24(m,5))return false;R.give(n);R.save();renderPage();return true;};
const sources=N.itemSources1018;N.itemSources1018=function(n){const out=sources.apply(this,arguments);if(['獸靈果丹','靈獸露丹'].includes(short(n))&&!out.some(r=>r.name==='煉金爐'))out.push({kind:'配方',name:'煉金爐',text:'煉金爐・煉丹：'+(short(n)==='獸靈果丹'?'獸靈果':'靈獸露')+'×5'});return out;};
const all=N.allItemNames1018;N.allItemNames1018=()=>[...new Set([...all(),...data.map(([n])=>'［特殊］'+n),...pills.map(n=>'［初階］'+n),'［特殊］獸技殘頁'])].filter(n=>!aliases[short(n)]);
const catalog=N.catalogRows1018;N.catalogRows1018=function(tab){return catalog.apply(this,arguments).filter(r=>!aliases[short(r.name)]);};
const bag=renderBag;renderBag=function(){const d=JZ072.fragment(bag.apply(this,arguments));for(const button of d.querySelectorAll('button[onclick*="JZ073.usePack"]')){const card=[...d.querySelectorAll('[data-item-product],.card')].find(c=>c.dataset.itemProduct==='［特殊］東州大禮包'||c.querySelector('b')?.textContent.trim()==='［特殊］東州大禮包');if(card)card.append(button);}for(const card of d.querySelectorAll('[data-item-product]')){const n=card.dataset.itemProduct;if(N.revision24Descriptions[short(n)]||/寵物用破境丹/.test(n)){const text=W.itemDescription(n);if(!card.textContent.includes(text)){let p=card.querySelector('.jz24-item-description');if(!p){p=document.createElement('p');p.className='jz24-item-description';card.append(p);}p.textContent=text;}}}return d.innerHTML;};
const battleBag=r58BattleBag;r58BattleBag=function(){const out=battleBag.apply(this,arguments);for(const card of document.querySelectorAll('.r526-battle-pop .card'))if(/箱|禮包/.test(card.querySelector('b')?.textContent||''))card.remove();return out;};
const use=W.useItem;W.useItem=function(n){if(battle&&/箱|禮包/.test(n))return false;return use.apply(this,arguments);};
})();
