from pathlib import Path
p=Path(__file__).parent/'quests.js';s=p.read_text('utf8')
changes=[
 ("if(!d||!N.canOffer(d)||S.place!==d.place)return false;const q=N.makeQuest(d);", "if(!d||N.quest(d.id)?.claimed||(!N.quest(d.id)&&!N.canOffer(d))||S.place!==d.place)return false;if(key==='033B')return N.notice('劇情待補','此段完整原稿與回報未提供，保留分支與進度。');const q=N.makeQuest(d);"),
 ("if(!q||q.claimed||battle)return false;let f;", "if(!q||q.claimed||!q.progress.started||battle)return false;let f;"),
 ("const key=d.key;if(key==='029'", "const key=d.key;if(!q.progress.started)return N.acceptStory(key,d.type);if(key==='032'&&!N.state().branch)return N.chooseBranch();if(key==='030'&&!q.progress.routes)return N.chooseInvestigation();if(key==='029'"),
 ("if(!q||q.claimed||!['林夏于','沈玄川','柳清妍'].includes(name)", "if(!q||q.claimed||!q.progress.started||!['林夏于','沈玄川','柳清妍'].includes(name)"),
 ("N.clearStoryParty();closeModal();R.save();render();return true;}if(key==='034B')", "N.clearStoryParty();closeModal();moveTo('青陽鎮');R.save();render();return true;}if(key==='034B')"),
]
for a,b in changes:
 if a not in s:raise ValueError('Missing repair hook '+a)
 s=s.replace(a,b)
p.write_text(s,'utf8')
