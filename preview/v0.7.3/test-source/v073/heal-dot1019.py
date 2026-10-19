def patch(text):
 pairs=[("  if((dot[op.name]&&has(f,'療癒'))||(op.name==='療癒'&&allStates(f).some(s=>dot[s.name])))return '持續傷害與「療癒」同時結算先後待定';",''), ("if(!b.jzpAllowHealDots&&actors.some(f=>alive(f)&&allStates(f).some(s=>dot[s.name])&&has(f,'療癒'))){b.jzPending='持續傷害與持續治療結算先後待定';return false;}",''),("   if(!b.jzpAllowHealDots&&states.some(s=>dot[s.name])&&has(f,'療癒')){b.jzPending='持續傷害與持續治療結算先後待定';return false;}",''),("for(const s of [...states].reverse()){","for(const s of [...states].reverse().sort((a,b)=>(dot[a.name]?0:a.name==='療癒'?2:1)-(dot[b.name]?0:b.name==='療癒'?2:1))){")]
 for a,b in pairs:
  assert text.count(a)==1,(a[:80],text.count(a));text=text.replace(a,b)
 return text
