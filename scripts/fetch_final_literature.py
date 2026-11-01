import requests,json,time,concurrent.futures,hashlib,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
items={'P24_Portability':'10.1016/j.jpdc.2023.104831','P25_Kokkos3':'10.1109/TPDS.2021.3097283','P23_Kokkos':'10.1109/MCSE.2021.3098509','P22_GiMMiK':'10.1016/j.cpc.2015.12.012','P21_HiFiLES':'10.2514/6.2014-3168'}
for k,d in items.items():
 try:
  r=requests.get('https://api.crossref.org/works/'+d,timeout=40);r.raise_for_status();(R/'metadata'/(k+'-crossref.json')).write_text(json.dumps(r.json(),ensure_ascii=False,indent=2))
 except Exception as e:print(k,'crossref',str(e),flush=True)
 try:
  r=requests.get('https://api.openalex.org/works/https://doi.org/'+d,timeout=40);r.raise_for_status();j=r.json();(R/'metadata'/(k+'-oa.json')).write_text(json.dumps(j,ensure_ascii=False,indent=2))
  urls=[l['pdf_url'] for l in j.get('locations',[]) if l.get('pdf_url')]
  print(k,'candidates',urls,flush=True)
  for u in urls:
   try:
    rr=requests.get(u,timeout=65);rr.raise_for_status()
    if not rr.content.startswith(b'%PDF'):continue
    p=R/'ref-paper/fulltext'/(k+'.pdf');p.write_bytes(rr.content);subprocess.run(['pdftotext','-layout',str(p),str(R/'ref-paper/text'/(k+'.txt'))],check=True);(R/'metadata'/(k+'-download.json')).write_text(json.dumps({'url':u,'sha256':hashlib.sha256(rr.content).hexdigest(),'local_pdf':str(p.relative_to(R)),'retrieved':'2026-10-28'},indent=2));print(k,'saved',len(rr.content),flush=True);break
   except Exception as e:print(k,'download',str(e),flush=True)
 except Exception as e:print(k,'openalex',str(e),flush=True)
 time.sleep(1)
