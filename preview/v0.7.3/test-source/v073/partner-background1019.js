(function(){'use strict';const N=JZ073;
const home=Object.fromEntries(Object.entries(JZNEXT.npcs).map(([n,d])=>[n,d.place]));
N.partnerPortraitScene1019=n=>{const d=JZNEXT.npcs[n]||JZ071.npcs[n];if(!d?.romance)return '';return d.partnerBackground||d.portraitBackground||JZ38.scene(n)||JZV2_ART[home[n]||d.home||d.place]||'';};
N.paintPartnerPortraits1019=root=>{for(const im of root.querySelectorAll('.r519-member-card>img,.team-slot>img,.jz072-partner-head>img')){const n=Object.keys(JZNEXT.npcs).find(n=>im.alt.startsWith(n));if(!n)continue;const scene=N.partnerPortraitScene1019(n);if(!scene)continue;im.classList.add('jz-romance-partner-portrait');im.dataset.partnerScene=n;im.style.backgroundImage='url("'+scene+'")';im.style.backgroundSize='cover';im.style.backgroundPosition='center';im.style.backgroundColor='#10252b';}};
for(const name of ['renderTeam','renderPartners']){const old=window[name];window[name]=function(){const d=JZ072.fragment(old.apply(this,arguments));N.paintPartnerPortraits1019(d);return d.innerHTML;};}
})();
