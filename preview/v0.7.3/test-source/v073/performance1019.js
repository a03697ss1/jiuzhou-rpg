(function(){'use strict';const N=JZ073,U=JZ071;
// Name normalization is pure; never cache stats, combat results, or inventory.
const short=U.short,shorts=new Map();U.short=function(name){if(typeof name!=='string')return short.apply(this,arguments);if(shorts.has(name))return shorts.get(name);const value=short.apply(this,arguments);if(shorts.size>=4096)shorts.clear();shorts.set(name,value);return value;};
// Older root-art passes replace each other's output. Keep their final artwork,
// but do not rerun them for the very same, already-normalized DOM nodes.
const rebuild=window.r554RebuildAllRootWidgets,seenRoots=new WeakMap(),selector='.bsv2-card > .r554-bsv2-root,.r554-root-widget,.r521-root-orb';
const signature=e=>[e.className,e.dataset.root,e.getAttribute('title'),e.childElementCount,...[...e.querySelectorAll('img')].map(im=>im.getAttribute('src'))].join('|');
window.r554RebuildAllRootWidgets=function(scope=document){const roots=[...scope.querySelectorAll(selector)];if(!roots.some(e=>seenRoots.get(e)!==signature(e)))return;const out=rebuild.apply(this,arguments);for(const e of scope.querySelectorAll(selector))seenRoots.set(e,signature(e));return out;};
// One compiled material-name matcher replaces a fresh regexp for every material
// on every text node. Preserve the exact tier rules and only write changed text.
let catalogue='',matcher=null,canonical=new Map();const seenText=new WeakMap();
N.materialLabels1019=root=>{if(!root)return;const key=U.materialCatalog.join('\n');if(key!==catalogue){catalogue=key;canonical=new Map();for(const name of U.materialCatalog){const s=U.short(name);if(!canonical.has(s))canonical.set(s,N.materialName(s));}const names=[...canonical.keys()].sort((a,b)=>b.length-a.length).map(s=>s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&'));matcher=new RegExp('(^|[^\\u4e00-\\u9fff］])('+names.join('|')+')(?=\\s*(?:[×xｘ]|$))','g');}
const walker=document.createTreeWalker(root,NodeFilter.SHOW_TEXT),nodes=[];while(walker.nextNode())nodes.push(walker.currentNode);for(const node of nodes){const text=node.nodeValue;if(seenText.get(node)===text||node.parentElement?.closest('script,style,button,input,textarea,select,.jz-catalog-card'))continue;matcher.lastIndex=0;const next=text.replace(matcher,(_,prefix,name)=>prefix+(canonical.get(name)||name));if(next!==text)node.nodeValue=next;seenText.set(node,next);}};
if(N.releaseHistory073)N.releaseHistory073.BUG修復.push('減少戰鬥畫面中靈根圖示與物品文字的重複處理，改善較慢裝置的介面及自動戰鬥卡頓。');
})();
