from pathlib import Path
p=Path(__file__).with_name('review18-fixes.js');s=p.read_text('utf8')
s=s.replace("live=team.filter(x=>x.name===f.name&&!assigned.has(x))[0]||team[i];", "const choices=team.filter(x=>N.canonical(x.name)===N.canonical(f.name)&&!assigned.has(x));live=choices.find(x=>x.realm===f.realm&&x.tier===f.tier)||choices[0]||team[i];")
p.write_text(s,'utf8')
