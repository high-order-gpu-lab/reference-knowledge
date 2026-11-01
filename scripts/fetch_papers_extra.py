from pathlib import Path
import requests,concurrent.futures,hashlib,subprocess,json
from lxml import etree
R=Path(__file__).resolve().parents[1]
ids={'P15_FLEXI':'1910.02858','P16_GPU_CEED':'2109.05072','P17_CEED_review':'2109.04996','P18_GPU_DG_INS':'1801.00246','P19_PETSc_GPU':'2011.00715'}
def fetch(item):
 key,aid=item;url=f'https://arxiv.org/pdf/{aid}'
 rec={'id':key,'arxiv':aid,'url':url,'retrieved':'2026-10-28'}
 try:
  r=requests.get('https://arxiv.org/abs/'+aid,timeout=45);r.raise_for_status();(R/'metadata'/(key+'-abs.html')).write_text(r.text)
  r=requests.get(url,timeout=100);r.raise_for_status();assert r.content.startswith(b'%PDF')
  path=R/'ref-paper/fulltext'/(key+'.pdf');path.write_bytes(r.content);rec.update(sha256=hashlib.sha256(r.content).hexdigest(),bytes=len(r.content),local_pdf=str(path.relative_to(R)),status='fulltext')
  subprocess.run(['pdftotext','-layout',str(path),str(R/'ref-paper/text'/(key+'.txt'))],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  print(key,len(r.content),flush=True)
 except Exception as e:rec['error']=str(e);print(key,'ERROR',str(e),flush=True)
 return rec
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:recs=list(ex.map(fetch,ids.items()))
(R/'metadata/paper_downloads_extra.json').write_text(json.dumps(recs,ensure_ascii=False,indent=2))
