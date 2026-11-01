from pathlib import Path
import requests,hashlib,json,concurrent.futures,subprocess
from lxml import html
R=Path(__file__).resolve().parents[1]
urls={'M01_PyFR':'https://pyfr.readthedocs.io/en/latest/','M02_PyFR_backend':'https://pyfr.readthedocs.io/en/latest/configuration/backend.html','M03_FLEXI':'https://numericsresearchgroup.org/userguide/userguide.pdf','M04_MFEM_GPU':'https://mfem.org/gpu-support/','M05_MFEM_PA':'https://mfem.org/performance/','M06_Kokkos':'https://kokkos.org/kokkos-core-wiki/ProgrammingGuide/','M07_CUDA_best':'https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/','M08_HIP':'https://rocm.docs.amd.com/projects/HIP/en/latest/how-to/performance_guidelines.html','M09_libCEED':'https://libceed.org/en/latest/'}
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
(R/'metadata/manual_manifest.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
