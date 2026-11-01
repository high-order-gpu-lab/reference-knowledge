from pathlib import Path
import shutil,json,hashlib
R=Path(__file__).resolve().parents[1];src=R.parent/'doc/files/背景材料/曙光DCU';out=R/'ref-paper/manuals/DCU';out.mkdir(exist_ok=True)
keys=['CUDA 程序适配','HIP C++','HIP Runtime','HIP最佳','DCC使用','hipprof','RCCL','hipSOLVER','hipSPARSE','rocBLAS','开发环境安装','兼容性','DCU编程实战']
rows=[]
for p in sorted(src.glob('*.pdf')):
 if not any(k in p.name for k in keys):continue
 dest=out/p.name;shutil.copy2(p,dest);rows.append({'file':str(dest.relative_to(R)),'source_local':str(p.relative_to(R.parent)),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'bytes':dest.stat().st_size})
(R/'metadata/dcu_manuals.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
h=R/'ref-code/HORSES3D-GPU/doc/HORSES3D_User_Manual.pdf';shutil.copy2(h,R/'ref-paper/manuals/M10_HORSES3D_User_Manual.pdf')
books=[]
for k in ['B01_PMPP','B02_Conservation']:
 j=json.loads((R/'metadata'/(k+'-crossref.json')).read_text())['message'];books.append({'id':k,'title':j['title'][0],'subtitle':j.get('subtitle',[]),'doi':j['DOI'],'isbn':j.get('ISBN',[]),'date':j['published']['date-parts'][0],'publisher':j['publisher'],'authors':j.get('author',[]),'status':'metadata-only; publisher fulltext not downloaded'})
(R/'metadata/books.json').write_text(json.dumps(books,ensure_ascii=False,indent=2))
lines=['# 图书与手册索引','','## 图书：已核验书目，未下载受限全文','', '| ID | 书名 | 出版与标识 | 用途与取得范围 |','|---|---|---|---|', '| B01 | Programming Massively Parallel Processors | Elsevier，Crossref日期2023；ISBN 9780323912310；[DOI元数据](../metadata/B01_PMPP-crossref.json) | GPU并行、访存与优化的教材入口；仅元数据。此记录未返回作者字段，不补写未核实作者。 |', '| B02 | Numerical Methods for Conservation Laws: From Analysis to Algorithms | Jan S. Hesthaven，SIAM，2018；ISBN 9781611975093 / 9781611975109；[DOI元数据](../metadata/B02_Conservation-crossref.json) | 守恒律离散与算法基础；仅元数据。 |','', '图书元数据原始响应保存在metadata；网页访问403不等于图书不存在，也不构成已取得全文。','', '## 已保存的官方手册/文档','', '| 资料 | 本地入口 | 使用重点 |','|---|---|---|', '| PyFR 用户指南 | [HTML](manuals/M02_PyFR_user.html) | 后端、输入输出与运行方式 |', '| PyFR 性能调优 | [HTML](manuals/M02b_PyFR_tuning.html) | CUDA/HIP参数与调优入口 |', '| PyFR 开发指南 | [HTML](manuals/M02c_PyFR_developer.html) | 后端接口、数据和扩展点 |', '| FLEXI 文档源 | [代码概览](../ref-code/FLEXI/docs/documentation/02_codeoverview.md)、[流程](../ref-code/FLEXI/docs/documentation/03_workflow.md)、[教程](../ref-code/FLEXI/docs/documentation/04_tutorials) | 官网旧PDF链接404，改保存官方仓库文档源 |', '| GALÆXI | [README](../ref-code/GALAEXI/README.md)及[源码](../ref-code/GALAEXI) | CUDA Fortran/NVHPC编译及GPU运行；不借用FLEXI CPU说明宣称GPU支持 |', '| HORSES3D | [PDF](manuals/M10_HORSES3D_User_Manual.pdf)、[GPU限制](../ref-code/HORSES3D-GPU/README.md) | 通用手册与GPU版限制必须同时阅读 |', '| HiFiLES | [README](../ref-code/HiFiLES/README.md)及[论文源稿](../ref-code/HiFiLES/doc/AIAApaper/aiaa_atlanta_2014/main.tex) | 历史构建与FR实现说明 |', '| MFEM GPU | [HTML](manuals/M04_MFEM_GPU.html) | Device/Memory、层次并行及访存 |', '| MFEM PA | [HTML](manuals/M05_MFEM_PA.html) | 算子分解、部分组装、预条件；历史网页能力表需核对源码 |', '| Kokkos Programming Guide | [HTML](manuals/M06_Kokkos.html) | 索引页快照；章节以官网或本地Kokkos源码对应版本继续核对 |', '| CUDA Best Practices | [HTML](manuals/M07_CUDA_best.html) | 访存、资源占用和性能测量 |', '| HIP Performance Guidelines | [HTML](manuals/M08_HIP.html) | HIP实现注意事项；不是DTK/DCU兼容性证明 |', '| libCEED | [HTML](manuals/M09_libCEED.html) | 代数算子、接口与后端组织 |','', 'HTML已保存正文与提取文本，外部图片/样式未做整站镜像。参考源码中的文档和PDF可离线查看；官网latest文档不是固定软件发布版，采集日期见manifest。','', '## 项目已有曙光DCU材料的本地收集','', '下列PDF从本仓库既有资料复制到本知识库，原文件保持不变。此操作只确认文件来源和完整性，不声称逐页精读。','']
for x in rows:lines+=['- ['+Path(x['file']).name+']('+x['file'].replace('ref-paper/','')+')']
lines+=['','逐文件源路径与SHA256见 [DCU手册清单](../metadata/dcu_manuals.json)。Kokkos的DTK参考代码另见项目已有 `refcode/kokkos-4.5.01`，本次不重复复制大型依赖。']
(R/'ref-paper/图书与手册索引.md').write_text('\n'.join(lines)+'\n')
print('DCU manuals',len(rows))
