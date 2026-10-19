(function(){'use strict';const N=JZ073,B=N.inventory1019;
B.defaults.材料=100;
const state=B.state;B.state=function(){const existing=!!S.inventoryMail1019,s=state.apply(this,arguments);if(s.materialBaseSlots!==100){const old=Number(s.capacity.材料);s.capacity.材料=existing?Math.max(50,Number.isFinite(old)?Math.floor(old):50)+50:Math.max(100,Number.isFinite(old)?Math.floor(old):100);s.materialBaseSlots=100;}return s;};
if(R511_CODEX.背包與郵箱)R511_CODEX.背包與郵箱[2]=R511_CODEX.背包與郵箱[2].replace('物品與材料各有50格','物品初始50格、材料初始100格');
if(N.releaseHistory073)N.releaseHistory073.改動.push('材料背包初始容量由50格提高至100格；既有角色增加50格，保留先前擴充的額外格數，僅套用一次。');
})();
