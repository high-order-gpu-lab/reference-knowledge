from pathlib import Path
import requests,hashlib,json,concurrent.futures,subprocess
from lxml import html
R=Path(__file__).resolve().parents[1]
urls={'M02_PyFR_user':'https://pyfr.readthedocs.io/en/latest/user_guide.html','M02b_PyFR_tuning':'https://pyfr.readthedocs.io/en/latest/performance_tuning.html','M02c_PyFR_developer':'https://pyfr.readthedocs.io/en/latest/developer_guide.html','M06_Kokkos':'https://kokkos.org/kokkos-core-wiki/programmingguide.html','P20_libCEED':'https://joss.theoj.org/papers/10.21105/joss.02945.pdf'}
def fetch(kv):
 k,u=kv;rec={'id':k,'url':u,'retrieved':'2026-10-28'}
 try:
  r=requests.get(u,timeout=80);r.raise_for_status();pdf=r.content.startswith(b'%PDF');p=R/'ref-paper/manuals'/(k+('.pdf' if pdf else '.html'));p.write_bytes(r.content);rec.update(local=str(p.relative_to(R)),sha256=hashlib.sha256(r.content).hexdigest(),status='saved')
  if pdf:subprocess.run(['pdftotext','-layout',str(p),str(p.with_suffix('.txt'))],check=True)
  else:
   d=html.fromstring(r.content)
   for e in d.xpath('//script|//style'):e.drop_tree()
   p.with_suffix('.txt').write_text(d.text_content())
  print(k,len(r.content),flush=True)
 except Exception as e:rec.update(status='failed',error=str(e));print(k,str(e),flush=True)
 return rec
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:rows=list(ex.map(fetch,urls.items()))
(R/'metadata/manual_manifest_extra.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
