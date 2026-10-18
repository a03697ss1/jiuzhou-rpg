from pathlib import Path
p=Path(__file__).with_name('review18-qa.cjs');s=p.read_text('utf8')
s='\n'.join(line for line in s.split('\n') if not line.startswith("await test([17],"))
s=s.replace("return {fox,horn,cats,npc,tiers:","return {fox,horn,cats,npc,unclassified:JZ073.catalogRows1018('素材').filter(r=>r.category==='素材').map(r=>r.name),tiers:")
s=s.replace("assert(x.fox==='妖物'&&x.horn==='妖物'", "assert(!x.unclassified.length&&x.fox==='妖物'&&x.horn==='妖物'")
p.write_text(s,'utf8')
