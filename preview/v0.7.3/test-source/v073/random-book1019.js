(function(){'use strict';const N=JZ073,R=JZR,U=JZ071,bags=['materials','items','special','gearInventory','souvenirs'];
const pieces=()=>bags.flatMap(b=>Object.entries(S[b]||{}).filter(([n])=>U.short(n)==='功法殘卷').map(([name,v])=>({bag:b,name,count:Math.max(0,Math.floor(Number(typeof v==='object'?v.count:v)||0))})));N.bookFragmentCount1019=()=>pieces().reduce((n,r)=>n+r.count,0);
const reqBook=req=>{const rows=r59ParseReq(req);return rows.length===1&&U.short(rows[0][0])==='功法殘卷'&&rows[0][1]===10;};
const has=r59HasIngredients;r59HasIngredients=function(req){return reqBook(req)?N.bookFragmentCount1019()>=10:has.apply(this,arguments);};
const missing=r512Missing;r512Missing=function(req){return reqBook(req)?N.bookFragmentCount1019()>=10?'':'功法殘卷 缺 '+(10-N.bookFragmentCount1019()):missing.apply(this,arguments);};
const craft=r59CraftItem;r59CraftItem=function(name,req,category){if(U.short(name)!=='隨機功法書'||category!=='合成')return craft.apply(this,arguments);const formal=(RECIPES.合成||[]).find(r=>U.short(r[0])==='隨機功法書');if(battle||!formal||!reqBook(req)||!reqBook(formal[1])||N.bookFragmentCount1019()<10)return false;let left=10;for(const row of pieces()){const take=Math.min(left,row.count);if(!take)continue;const entry=S[row.bag][row.name];if(typeof entry==='object')entry.count-=take;else S[row.bag][row.name]-=take;left-=take;if(!left)break;}R.give('［特殊］隨機功法書',1);N.recipeCrafted('［特殊］隨機功法書','合成');log('🧩 合成完成：消耗功法殘卷×10，獲得［特殊］隨機功法書×1。');R.save();render();r59RenderCraftPage();return true;};
for(const row of RECIPES.合成||[])if(U.short(row[0])==='隨機功法書')row[0]='［特殊］隨機功法書';
if(N.releaseHistory073)N.releaseHistory073.BUG修復.push('隨機功法書合成正確讀取各背包分頁的功法殘卷；10張合成1本可使用的特殊隨機功法書，不誤用獸技殘頁。');
})();
