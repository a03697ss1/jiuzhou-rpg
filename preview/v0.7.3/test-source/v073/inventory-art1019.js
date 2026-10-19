(function(){'use strict';const N=JZ073;
N.inventoryArt1019=Object.fromEntries(['背包擴充格','抽獎卷','改名卡','靈幣'].map(n=>[n,'/郵箱背包美術_2026-10-19/'+n+'.webp']));
const icon=N.itemIcon;N.itemIcon=function(n){return N.inventoryArt1019[JZ071.short(n)]||icon.apply(this,arguments);};
})();
