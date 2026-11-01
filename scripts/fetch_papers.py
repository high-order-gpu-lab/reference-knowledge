from pathlib import Path
import requests,concurrent.futures,hashlib,subprocess,json
from lxml import etree
R=Path(__file__).resolve().parents[1]
ids={'P01_PyFR_v2':'2408.16509','P02_GALAEXI':'2404.12703','P03_HORSES3D_GPU':'2607.26674','P04_HORSES3D':'2206.09733','P05_MFEM':'1911.09220','P06_LOR_GPU':'2210.12253','P07_MFEM_RAJA':'2112.07075','P08_Mesh_GPU':'2205.12721','P09_GALAEXI_v2':'2605.28627','P10_GALAEXI_APU':'2606.18927','P11_FP64_Tensor':'2603.09038','P12_Hdiv_solver':'2304.12387','P13_PyFR_original':'1312.1638','P14_PyFR_mixed':'1409.0405'}
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
(R/'metadata/paper_downloads.json').write_text(json.dumps(recs,ensure_ascii=False,indent=2))
