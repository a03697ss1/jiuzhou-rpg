(function(){'use strict';const N=JZ073,towns=new Set(Object.values(REGIONS).flatMap(r=>r.towns||[]));N.clinicTowns1019=[...towns];
const facilities=facilitiesFor;facilitiesFor=function(place){const rows=facilities.apply(this,arguments);return towns.has(place)&&!rows.includes('醫館')?[...rows,'醫館']:rows;};
// Ordinary treatment, prices, wards and rescue use the unchanged main-city clinic.
// Story patients stay at their actual city rather than appearing in every clinic.
const clinic=openClinic;openClinic=function(){const out=clinic.apply(this,arguments);if(S?.place!=='朝御城')for(const card of document.querySelectorAll('#modalBody .card'))if(card.querySelector('h3')?.textContent==='病房・沈玄川')card.remove();return out;};
if(N.releaseHistory073)N.releaseHistory073.新增.push('城鎮設備新增醫館，治療、異常狀態、疲勞調養與病房救援沿用主城相同規則及費用。');
})();
