(function(){'use strict';const N=JZ073,R=JZR,W=JZW,C=JZ360,E=N.esc;
N.itemsReview19={version:'0.7.3',date:'2026-10-19',linXiGift:false};
// User-confirmed acquisition locations. This does not invent shop prices or stock.
N.wendaoConfirmed19=new Set(['鎮岳錘','逐星弓','問道槍','問心劍','納靈葫蘆','破境拳套','破軍刀','玄機靈傘','問靈道冠','玄心道袍','問天戰衣','問道戰靴','踏虛靈履','問道戰衣','問心戒','戰心指環','破境項鍊','道心靈墜','問道佩','問天玉佩'].map(n=>'［特殊］'+n));
const sources=N.itemSources1018;N.itemSources1018=function(name){const base=JZ072.baseGear(name),rows=sources.apply(this,arguments).slice();if(N.wendaoConfirmed19.has(base)&&!rows.some(r=>r.name==='問道檯'))rows.push({kind:'挑戰',name:'問道檯',text:'問道檯'});if(base==='［無階］新手護符'&&!rows.some(r=>r.name==='新手大禮包'))rows.push({kind:'禮包',name:'新手大禮包',text:'開啟［特殊］新手大禮包取得×1。'});return rows;};
N.specialTech19=Object.fromEntries(Object.values(C.byId).filter(r=>!r.monster&&r.tier==='特殊').map(r=>['［特殊］'+r.name,r]));
const technique=n=>N.specialTech19[n]||Object.values(N.specialTech19).find(r=>r.name===n);
const itemClass=W.itemClass;W.itemClass=function(n){return technique(n)?'功法':itemClass.apply(this,arguments);};
// Earlier rewards can have placed a book in a generic special-item bucket.
// Move every existing copy into the established technique inventory without learning it.
N.migrateSpecialTech19=()=>{if(!S)return;S.techInventory??=[];for(const bucket of ['items','special','materials','gearInventory','souvenirs'])for(const [name,value] of Object.entries(S[bucket]||{})){const r=technique(name),count=typeof value==='object'?Number(value?.count||0):Number(value||0);if(!r||!Number.isInteger(count)||count<=0)continue;for(let i=0;i<count;i++)S.techInventory.push('［特殊］'+r.name);delete S[bucket][name];}};
const ensure=R.ensure;R.ensure=function(){const out=ensure.apply(this,arguments);N.migrateSpecialTech19();return out;};
const give=W.give;W.give=function(name,qty=1){if(technique(name))return R.give('［特殊］'+technique(name).name,qty);return give.apply(this,arguments);};
const use=W.useItem;W.useItem=function(name){const r=technique(name);if(!r)return use.apply(this,arguments);if(battle)return false;R.ensure();const full='［特殊］'+r.name;if(!S.techInventory.includes(full))return false;return learnTechnique(full);};
const artNames=[...Object.keys(N.specialTech19),'［特殊］不滅獸甲'];
N.itemArt19=Object.fromEntries(artNames.map(n=>[n,'/物品修正美術_2026-10-19/'+n+'.png']));
const icon=N.itemIcon;N.itemIcon=function(name){const base=JZ072.baseGear(name),r=technique(base);return N.itemArt19[base]||r&&N.itemArt19['［特殊］'+r.name]||icon.apply(this,arguments);};
const techPage=renderTech;renderTech=function(){R.ensure();const fragment=JZ072.fragment(techPage.apply(this,arguments));for(const entry of fragment.querySelectorAll('.card,.tech-entry')){if(entry.querySelector('.card,.tech-entry'))continue;const title=entry.querySelector('b')?.textContent?.trim(),r=technique(title);if(r&&!entry.querySelector('.jz-item-image'))entry.insertAdjacentHTML('afterbegin',N.itemImage1018('［特殊］'+r.name,'jz19-tech-book'));}return fragment.innerHTML;};
const setPieces=['忡靈頭盔','忡靈戰甲','忡靈鎖褲','忡靈戰靴'].map(n=>'［特殊］'+n);
const card=N.catalogCard1018;N.catalogCard1018=function(row,tab){const html=card.apply(this,arguments);if(!setPieces.includes(row.name)||tab!=='裝備')return html;const fragment=JZ072.fragment(html),details=fragment.querySelector('.jz-catalog-details'),section=document.createElement('section');section.className='jz-catalog-section jz19-set-effect';section.innerHTML='<h4>忡靈套裝效果</h4><p>集齊忡靈頭盔、忡靈戰甲、忡靈鎖褲與忡靈戰靴四件後，永久解鎖［特殊］忡靈術，不另要求功法書。</p><button class="jz-reference" onclick="JZ073.skillInfo1018(\'T001\')">查看［特殊］忡靈術</button>';details?.insertBefore(section,details.querySelector('.jz-catalog-sources'));return fragment.innerHTML;};
const history=JZ072.versionHistory;JZ072.versionHistory=function(){history.apply(this,arguments);document.getElementById('modalBody')?.insertAdjacentHTML('afterbegin','<section class="card"><h2>10/19 物品與戰鬥介面更新</h2><h3>新增</h3><p>忡靈套裝四件效果說明、特殊功法書圖片及獨立的不滅獸甲圖片。</p><h3>改動</h3><p>補齊問道檯裝備、新手護符的取得來源；長右專屬血條與較小的我方戰位。</p><h3>BUG修復</h3><p>修復主線戰鬥結算後仍停留在戰鬥畫面。特殊功法歸回功法分類，舊紀錄中的功法書保留並移回持有功法。</p></section>');};
const style=document.createElement('style');style.textContent='.jz19-tech-book{width:86px;height:86px;flex:0 0 86px;object-fit:contain}.jz19-set-effect{border:1px solid #b79b54;background:linear-gradient(135deg,#24291c,#10222c);border-radius:8px;padding:12px}.jz19-set-effect h4{color:#edcf83}';document.head.append(style);
const decorate=N.decorate;N.decorate=()=>{decorate();const banner=document.querySelector('.jz073-banner');if(banner&&!banner.dataset.items19){banner.dataset.items19='true';banner.insertAdjacentHTML('beforeend','<span class="jz18-build">10/19 主線戰鬥／物品修正</span>');}};
})();
