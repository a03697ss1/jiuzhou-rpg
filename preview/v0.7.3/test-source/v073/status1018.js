(function(){'use strict';const N=JZ073;
const descriptions={灼熱:'火屬傷害接續灼燒成功機率＋3%；遇水屬性傷害取消。',潮濕:'遭雷傷額外傷害＋3%；遭冰凍成功機率＋3%。',纏身:'遭火傷額外傷害＋3%；遭中毒成功機率＋3%。',泥身:'遭遲緩成功機率＋3%。',風蝕:'遭迷茫成功機率＋3%。',電能:'遭麻痺成功機率＋3%。',光明:'遭暗傷額外傷害＋3%；遭失明成功機率＋3%。',黑暗:'遭光傷額外傷害＋3%；遭恐懼成功機率＋3%。'};
for(const [name,text] of Object.entries(descriptions))R511_CODEX[name]=[name,[text,'獨立狀態，不占用Buff／Debuff各4個上限。必定附加，合法互動觸發一次即消失。'],name==='潮濕'?'正式施加來源：洪水。':'正式施加技能尚未指定。',['戰鬥']];
N.openStateGuide=()=>showModal('八種獨立狀態',Object.entries(descriptions).map(([name,text])=>'<div class="card"><b>'+N.stateDefs[name].icon+' '+name+'</b><p>'+text+'</p><p>'+(name==='潮濕'?'洪水必定附加。':'目前保留狀態及測試接口，尚無指定施加技能。')+'</p></div>').join(''));
const codex=N.openCodex;N.openCodex=function(tab,filter){if(tab==='狀態')return N.openStateGuide();const out=codex.apply(this,arguments);document.getElementById('modalBody')?.querySelector('.actions')?.insertAdjacentHTML('beforeend','<button onclick="JZ073.openStateGuide()">八種獨立狀態</button>');return out;};
N.pending=N.pending.filter(x=>!/^八種狀態/.test(x.id));
N.pending.push({id:'七種狀態未指定施加技能',reason:'依本輪確認，灼熱、纏身、泥身、風蝕、電能、光明、黑暗保留獨立狀態、互動與測試接口；正式施加技能尚未指定。洪水必定附加潮濕。未更改368功法庫，未讓同屬性招式自動附加。'});
N.note('L18','已實裝','八種獨立狀態、必定施加、3%互動、單次消耗、獨立上限與圖示懸停；正式施加來源僅洪水→潮濕，其餘七種依本輪要求保留接口。');
})();
