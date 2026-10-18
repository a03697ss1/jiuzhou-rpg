"""Publish the authorized October 18 completed pet cores only under preview/v0.7.3."""
from pathlib import Path
import sys, json, shutil, re, hashlib, datetime
from urllib.parse import unquote, quote
import importlib.util

P = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('publisher', P/'publish-preview.py')
old = importlib.util.module_from_spec(spec); spec.loader.exec_module(old)
ROOT, W, PREFIX, DEST = old.ROOT, old.W, old.PREFIX, old.DEST
O = ROOT/'V0.7.3_18項修正_2026-10-18'
BUILD = '20261018-review18-1'
PAGES = ['閱讀我_先看這裡.html','逐項施工工程覆蓋表.html','BUG修復與待補清單.html','完整測試及驗收報告.html','素材圖片清單與預覽.html']
git, digest = old.git, old.digest

def prepare():
    changed=[n for n in git(W,'diff','--name-only','-z').split('\0') if n]
    untracked=[n for n in git(W,'ls-files','--others','--exclude-standard','-z').split('\0') if n]
    assert all(n.startswith(PREFIX+'/') for n in changed+untracked), 'Unexpected changes outside preview'
    head, remote = git(W,'rev-parse','HEAD'), git(W,'rev-parse','origin/main')
    if head != remote:
        git(W,'merge','--ff-only','origin/main')
    base = git(W,'rev-parse','HEAD')
    protected = {n:git(W,'rev-parse','HEAD:'+n) for n in ['index.html','定案規則_0.7.2.json']}
    text = (P/'preview.html').read_text('utf8')
    for a,b in [('/github-release/assets/','../../assets/'),('/新增美術_2026-10-16/','new-assets/'),('/素材美術_2026-10-18/','material-assets/'),('/物品美術_2026-10-18/','item-assets/'),('/人物全身_2026-10-18/','fullbody-assets/'),('/物品獨立美術_2026-10-18/','unique-item-assets/'),('10/18 本地補完','10/18 獨立測試補完')]:
        text = text.replace(a,b)
    text = text.replace('正式母檔、正式版本與GitHub發布內容維持施工前狀態。','正式母檔與正式入口維持0.7.2；本輪提供GitHub 0.7.3獨立測試頁。')
    text = text.replace('本地獨立測試補完','獨立測試補完').replace('正式母檔與GitHub未更新。','正式母檔與正式入口維持0.7.2；本輪已提供GitHub 0.7.3獨立測試頁。')
    text = re.sub(r'(unique-item-assets/[^"\n]+)\.png',r'\1.webp',text)
    legacy=json.loads((O/'既有預覽圖片無損編碼驗證.json').read_text('utf8'));assert legacy['pass']
    allowed={r['target']+'/'+r['name'] for r in legacy['rows']}
    def current_generic(m):
        data=json.loads(m.group(1))
        return 'window.JZ073_ITEM_ART='+json.dumps({k:v for k,v in data.items() if v in allowed},ensure_ascii=False)+';'
    text=re.sub(r'window\.JZ073_ITEM_ART=(\{[^;]+\});',current_generic,text)
    for row in legacy['rows']:
        text=text.replace(row['target']+'/'+row['name'],row['target']+'/'+Path(row['web']).name)
    text += '<script>window.JZ073_BUILD_ID='+json.dumps(BUILD)+';</script>'
    (DEST/'index.html').write_text(text,'utf8')
    for folder, target in [('新增美術_2026-10-16','new-assets'),('素材美術_2026-10-18','material-assets'),('物品美術_2026-10-18','item-assets'),('人物全身_2026-10-18','fullbody-assets')]:
        (DEST/target).mkdir(exist_ok=True)
        for f in (ROOT/folder).glob('*.png'):
            if f.name in text: shutil.copy2(f,DEST/target/f.name)
    compressed=json.loads((O/'線上圖片無損編碼驗證.json').read_text('utf8'))
    assert compressed['pass'] and len(compressed['rows'])==384
    icon_dir=(DEST/'unique-item-assets').resolve()
    assert icon_dir.parent==DEST.resolve()
    icon_dir.mkdir(exist_ok=True)
    for row in compressed['rows']:
        image=Path(row['web']);assert image.is_file()
        shutil.copy2(image,icon_dir/image.name)
        original=(icon_dir/(row['name']+'.png')).resolve()
        assert original.parent==icon_dir
        if original.is_file():original.unlink()
    for target in ['item-assets','material-assets','fullbody-assets','new-assets']:
        folder=(DEST/target).resolve();assert folder.parent==DEST.resolve()
        for image in folder.glob('*.png'):
            assert image.resolve().parent==folder
            image.unlink()
    for row in legacy['rows']:shutil.copy2(row['web'],DEST/row['target']/Path(row['web']).name)
    assert len(list((DEST/'material-assets').glob('*.webp'))) == 69
    shutil.copytree(O/'施工來源', DEST/'施工來源',dirs_exist_ok=True)
    source=DEST/'test-source/v073'; source.mkdir(parents=True,exist_ok=True)
    for f in (old.O/'Git測試分支/test-source/v073').iterdir():
        if f.is_file(): shutil.copy2(f,source/f.name)
    replacements = [
        ('九州修仙錄_V0.7.3_獨立測試版.html','index.html'),
        ('../素材美術_2026-10-18/','material-assets/'),('../物品美術_2026-10-18/','item-assets/'),('../人物全身_2026-10-18/','fullbody-assets/'),('../物品獨立美術_2026-10-18/','unique-item-assets/'),
        ('正式母檔、正式版本及GitHub內容未更新','正式母檔與正式入口維持0.7.2；本輪提供GitHub 0.7.3獨立測試頁'),
        ('本輪未執行推送或發布','本輪僅發布preview/v0.7.3獨立測試頁，正式入口未改'),
        ('未發布GitHub','已提供GitHub獨立測試頁'),
        ('2026-10-18本地獨立測試補完','2026-10-18獨立測試補完'),
        ('（單檔，內嵌原圖與本輪素材圖）','（GitHub線上版，共用原圖與本輪素材圖）')]
    screens=json.loads((O/'驗收截圖無損編碼驗證.json').read_text('utf8'));assert screens['pass']
    for name in PAGES:
        html=(O/name).read_text('utf8')
        for a,b in replacements: html=html.replace(a,b)
        html=re.sub(r'(unique-item-assets/[^"\n]+)\.png',r'\1.webp',html)
        for row in screens['rows']:
            html=html.replace(quote(row['name']),quote(Path(row['web']).name)).replace(row['name'],Path(row['web']).name)
        if name=='素材圖片清單與預覽.html':html=html.replace('原69張素材圖保留。','原69張素材圖保留。線上使用WebP無損編碼；原PNG保存在獨立測試分支。<a href="線上圖片無損編碼驗證.json">像素與透明度核對</a>。')
        (DEST/name).write_text(html,'utf8')
    for pattern in ['*.json','*.png']:
        for f in O.glob(pattern): shutil.copy2(f,DEST/f.name)
    # Keep the current proof screenshots online; prior proofs remain in Git history.
    for f in DEST.glob('*.png'):
        assert f.resolve().parent==DEST.resolve()
        f.unlink()
    for row in screens['rows']:shutil.copy2(row['web'],DEST/Path(row['web']).name)
    broken=[]
    for name in PAGES:
        for ref in re.findall(r'(?:href|src)="([^"#]+)"',(DEST/name).read_text('utf8')):
            if not re.match(r'^(?:https?:|data:|mailto:)',ref):
                target=DEST/unquote(ref.split('#')[0].split('?')[0])
                if not target.is_file(): broken.append([name,ref])
    assert not broken, broken
    assert all(f.stat().st_size < 100*1024*1024 for f in DEST.rglob('*') if f.is_file())
    site_bytes=sum(f.stat().st_size for f in W.rglob('*') if f.is_file() and '.git' not in f.relative_to(W).parts)
    assert site_bytes<1024**3,site_bytes
    state={'base':base,'protectedBlobs':protected,'build':BUILD,'url':old.URL,'indexSha256':digest(DEST/'index.html'),'materialImages':69,'documents':5,'siteBytes':site_bytes,'uniqueImages':384,'webEncoding':'lossless WebP','sourceCommit':json.loads((O/'本地測試分支保存紀錄.json').read_text('utf8'))['commit']}
    (P/'review18-publish-state.json').write_text(json.dumps(state,ensure_ascii=False,indent=2),'utf8')
    print(json.dumps(state,ensure_ascii=False))

def publish():
    state=json.loads((P/'review18-publish-state.json').read_text('utf8'))
    git(W,'add','--',PREFIX)
    changed=[x for x in git(W,'diff','--cached','--name-only','-z').split('\0') if x]
    assert changed and all(x.startswith(PREFIX+'/') for x in changed)
    assert digest(DEST/'index.html') == state['indexSha256']
    git(W,'commit','-m','Publish 18 gameplay review fixes and independent item art to 0.7.3 preview')
    changed=[x for x in git(W,'diff','--name-only','-z',state['base'],'HEAD').split('\0') if x]
    assert all(x.startswith(PREFIX+'/') for x in changed)
    for n,blob in state['protectedBlobs'].items(): assert git(W,'rev-parse','HEAD:'+n)==blob
    git(W,'push','origin','HEAD:refs/heads/main')
    record={**state,'kind':'independent-preview','deploymentCommit':git(W,'rev-parse','HEAD'),'changedFiles':len(changed),'changedOnlyPreview':True,'formalEntryUnchanged':True,'formalVersion':'0.7.2','publishedAt':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(timespec='seconds')}
    (O/'GitHub獨立測試部署紀錄.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),'utf8')
    print(json.dumps(record,ensure_ascii=False))

if __name__=='__main__':
    {'prepare':prepare,'publish':publish}[sys.argv[1]]()
