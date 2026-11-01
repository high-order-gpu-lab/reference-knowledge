from pathlib import Path
import json,re,hashlib,datetime,subprocess
from pypdf import PdfReader
R=Path(__file__).resolve().parents[1]
errors=[];checks=[]
# Validate the published subset, not locally retained ignored datasets.
tracked=None
if (R/'.git').exists():
 tracked={p.decode('utf-8') for p in subprocess.check_output(['git','ls-files','-z'],cwd=R).split(b'\0') if p}
papers=json.loads((R/'metadata/papers.json').read_text());code=json.loads((R/'metadata/code_manifest.json').read_text());evidence=json.loads((R/'metadata/code_evidence.json').read_text())
assert len(papers)==25 and len(code)==7 and len(evidence)==33
pdfs=[]
for p in papers:
 if p['local_pdf']:
  f=R/p['local_pdf']
  try:pdfs.append({'file':str(f.relative_to(R)),'pages':len(PdfReader(f).pages)})
  except Exception as e:errors.append(str(f)+': '+str(e))
 assert p['status']!='fulltext' or (R/p['local_text']).is_file()
for f in (R/'ref-paper/manuals').rglob('*.pdf'):
 try:pdfs.append({'file':str(f.relative_to(R)),'pages':len(PdfReader(f).pages)})
 except Exception as e:errors.append(str(f)+': '+str(e))
for e in evidence:
 f=R/e['path'];assert f.is_file();assert len(f.read_text(errors='replace').splitlines())>=e['line_end']
# Check authored Markdown only; upstream docs retain upstream link semantics.
authored=[R/'README.md',R/'ref-code/README.md']+list((R/'analysis').glob('*.md'))+list((R/'ref-paper').glob('*.md'))+list((R/'logs').glob('*.md'))
links=0
for f in authored:
 for url in re.findall(r'\]\(([^\n]+?)\)',f.read_text()):
  u=url.strip('<>');
  if u.startswith(('https://','http://','mailto:')) or Path(u).is_absolute():
   errors.append(f'{f.relative_to(R)} -> non-relative reference: {u}');continue
  if u.startswith('#'):continue
  u=u.split('#')[0]
  if u and not (f.parent/u).exists():errors.append(f'{f.relative_to(R)} -> {u}')
  if u and tracked is not None and (f.parent/u).is_file():
   target=(f.parent/u).absolute().relative_to(R).as_posix()
   target=str((f.parent/u).resolve().relative_to(R))
   if target not in tracked:errors.append(f'{f.relative_to(R)} -> not tracked: {u}')
  links+=1
for x in code:
 assert (R/'ref-code'/x['name']).is_dir();assert len(x['commit'])==40
# DOI equality after case normalization and no duplicate DOI/arXiv records.
for field in ['doi','arxiv']:
 vals=[p[field].lower() for p in papers if p[field]];assert len(vals)==len(set(vals))
for f in ['references.bib','references.ris']:
 text=(R/'ref-paper'/f).read_text();assert '\ufffd' not in text
# Build hashes for archived materials, metadata and authored reports, excluding this evolving QA result.
files=[]
for folder in ['ref-code','ref-paper','analysis']:
 for p in (R/folder).rglob('*'):
  if p.is_file() and not p.is_symlink() and (tracked is None or p.relative_to(R).as_posix() in tracked):files.append(p)
with (R/'metadata/SHA256SUMS').open('w') as f:
 for p in sorted(files):f.write(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(R))+'\n')
result={'repositories':len(code),'paper_records':len(papers),'paper_pdfs':sum(bool(p['local_pdf']) for p in papers),'all_checked_pdfs':len(pdfs),'checked_local_markdown_links':links,'code_evidence_entries':len(evidence),'sha256_files':len(files),'errors':errors,'pdfs':pdfs}
(R/'logs/validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='pdfs'},ensure_ascii=False,indent=2))
if errors:raise SystemExit(1)
