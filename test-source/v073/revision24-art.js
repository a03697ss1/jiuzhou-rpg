(function(){'use strict';const N=JZ073;
N.art24={boss1:'/修正24美術_2026-10-19/長右_水.webp',boss2:'/修正24美術_2026-10-19/長右_水雷.webp',box1:'/修正24美術_2026-10-19/一階樸素素材箱.webp',box2:'/修正24美術_2026-10-19/二階樸素素材箱.webp',leaf:'/修正24美術_2026-10-19/獸技殘頁.webp'};
for(const src of Object.values(N.art24)){const im=new Image();im.src=src;}
N.art.長右=N.art24.boss1;
const icon=N.itemIcon;N.itemIcon=function(name){if(/獸技殘頁/.test(name))return N.art24.leaf;if(/(?:自選|綜合).*一階.*箱|自選護體丹箱/.test(name))return N.art24.box1;if(/(?:自選|綜合).*二階.*箱|自選晶石箱/.test(name))return N.art24.box2;return icon.apply(this,arguments);};
const core=bmv1CombatCore;bmv1CombatCore=function(b){const html=core.apply(this,arguments),boss=b.enemyTeam.find(f=>f.jz073Boss);if(!boss)return html;const d=JZ072.fragment(html),img=d.querySelector('.jz-boss-body>img');if(img){img.src=boss.jz073Phase===2?N.art24.boss2:N.art24.boss1;img.alt=boss.jz073Phase===2?'長右完整水雷立繪':'長右完整水元素立繪';}return d.innerHTML;};
})();
