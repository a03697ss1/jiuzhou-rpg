(function(){'use strict';const N=JZ073,B=N.inventory1019;
const claim=B.claim;B.claim=function(){const before=Number(S?.coins)||0,out=claim.apply(this,arguments);if(out!==true)return out;const received=(Number(S?.coins)||0)-before;
if(received>0){
 // The attachment and balance already change together in the original claim.
 // Refresh the sidebar without closing the letter or rerendering the page.
 renderPlayer();
 const body=document.getElementById('modalBody');if(body){const status=document.createElement('p');status.className='jz-mail-coin-receipt';status.setAttribute('role','status');status.style.cssText='color:#f1d28a;padding:12px;border:1px solid #8e753c;border-radius:8px';status.textContent='已領取靈幣＋'+received.toLocaleString('zh-TW')+'，目前持有 '+S.coins.toLocaleString('zh-TW')+' 靈幣。';body.prepend(status);}
 log('📮 信件領取：靈幣＋'+received+'。');
 // Persist the balance and consumed attachment in the same immediate snapshot.
 r4WriteSave('auto',{silent:true});
}return out;};
if(N.releaseHistory073&&!N.releaseHistory073.BUG修復.includes('信件領取靈幣時即時刷新餘額與入帳提示，避免數字延遲更新。'))N.releaseHistory073.BUG修復.push('信件領取靈幣時即時刷新餘額與入帳提示，避免數字延遲更新。');
})();
