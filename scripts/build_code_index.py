from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
items=[
('C01','PyFR','pyfr/solvers/baseadvec/system.py',63,141,'对流残差以图组织：面插值、收发、局部通量、散度及修正'),
('C02','PyFR','pyfr/solvers/baseadvecdiff/system.py',1,220,'粘性路径独立检查，不能用纯对流图代表完整 Navier–Stokes'),
('C03','PyFR','pyfr/backends/cuda/base.py',8,110,'CUDA 后端注册计算核、矩阵、图，SoA 块宽32和128字节对齐'),
('C04','PyFR','pyfr/backends/hip/base.py',9,100,'HIP 后端依设备 warp_size 设置 SoA，支持 standard/hip-aware 配置'),
('C05','PyFR','pyfr/backends/base/types.py',21,120,'矩阵形状、分块、填充与布局变换'),
('C06','PyFR','pyfr/backends/cuda/gimmik.py',8,155,'常矩阵专用生成、候选核计时、缓存及回退'),
('C07','GALAEXI','src/dg/dg.f90',255,423,'显式 DG 残差内状态/梯度/通量交换与多 stream 调度'),
('C08','GALAEXI','src/dg/volint.f90',129,353,'分批体积分和 split-form 点级 CUDA Fortran 核'),
('C09','GALAEXI','src/dg/applydmatrix.t90',19,124,'线程号映射到单元与节点，逐方向求导'),
('C10','GALAEXI','src/dg/dg_vars.f90',25,145,'五维状态、体/面中间量、主机/设备镜像'),
('C11','GALAEXI','src/globals/gpu.f90',18,75,'默认 stream 与多个 stream 的集中管理'),
('C12','GALAEXI','src/mpi/mpi.f90',277,387,'设备面缓冲直接 MPI 收发；发送前同步对应 stream 或整设备'),
('C13','HORSES3D-GPU','README.md',96,115,'GPU beta 功能限制，不能继承主版所有能力'),
('C14','HORSES3D-GPU','Solver/src/NavierStokesSolver/SpatialDiscretization.f90',229,315,'残差总入口及模式分支'),
('C15','HORSES3D-GPU','Solver/src/NavierStokesSolver/SpatialDiscretization.f90',372,560,'先内部面与单元，再 MPI 面与单元；OpenACC gang/vector'),
('C16','HORSES3D-GPU','Solver/src/NavierStokesSolver/SpatialDiscretization.f90',1289,1424,'体通量/积分循环映射，存在具体 vector_length/num_gangs 参数'),
('C17','HORSES3D-GPU','Solver/src/libs/mesh/StorageClass.f90',28,120,'单元对象内状态、梯度及指针/分配数组'),
('C18','HORSES3D-GPU','Solver/src/libs/timeintegrator/ExplicitMethods.f90',250,310,'显式更新 OpenACC 路径示例'),
('C19','HiFiLES','src/HiFiLES.cpp',150,190,'时间步/RK stage 主循环'),
('C20','HiFiLES','src/solver.cpp',73,235,'FR 残差流程，面通信与体运算'),
('C21','HiFiLES','src/eles.cpp',1256,1328,'形状分组后将插值算子组织为 GEMM'),
('C22','HiFiLES','src/eles.cpp',1517,1655,'散度及修正 GEMM/AXPY'),
('C23','HiFiLES','src/cuda_kernels.cu',36,125,'bespoke_SPMV 核，共享内存与每块多单元'),
('C24','HiFiLES','include/array.h',288,312,'多维数组线性索引：第一维连续'),
('C25','HiFiLES','include/array.h',474,570,'主机与设备缓冲显式复制'),
('C26','MFEM','general/device.hpp',30,111,'Device/Backend 将 CUDA、HIP、RAJA、OCCA、CEED 纳入统一分派'),
('C27','MFEM','general/mem_manager.hpp',131,164,'Read/Write/ReadWrite 数据有效性及搬运语义'),
('C28','MFEM','examples/ex1.cpp',195,285,'部分组装、Operator、预条件和求解接口'),
('C29','MFEM','fem/integ/bilininteg_diffusion_kernels.hpp',981,1045,'三维 PA 核的单元/线程层次、共享内存和基矩阵'),
('C30','MFEM','fem/integ/bilininteg_diffusion_pa_simplices.hpp',1,90,'当前源码已有单纯形 PA 文件，官网旧说明不能当完整支持表'),
('C31','FLEXI','docs/documentation/02_codeoverview.md',1,100,'CPU 基线代码结构与 DG 流程说明'),
('C33','HiFiLES','src/mpi_inters.cpp',274,332,'GPU 打包后主机中转 MPI，接收后复制回设备'),
('C32','HORSES3D-GPU','NEWS.md',1,38,'GPU 显式时间步验证记录；与控制文件 Euler 方程限制需区分'),
]
manifest={x['name']:x for x in json.loads((R/'metadata/code_manifest.json').read_text())}
rows=[];lines=['# 源码证据索引','', '采集日期：2026-10-28。行号以本地固定提交为准；引用文件来自同一固定 commit 的本地快照。此处记录静态核查，不表示已编译或完成 GPU 测试。','']
for key,repo,path,lo,hi,meaning in items:
 p=R/'ref-code'/repo/path;assert p.is_file(),p;count=len(p.read_text(errors='replace').splitlines());hi=min(hi,count);assert lo<=hi
 rec={'id':key,'repository':repo,'path':str(p.relative_to(R)),'line_start':lo,'line_end':hi,'meaning':meaning,'commit':manifest[repo]['commit'],'url':manifest[repo]['url']+'/blob/'+manifest[repo]['commit']+'/'+path+f'#L{lo}-L{hi}'};rows.append(rec)
 lines+=['## '+key+' · '+repo,'',meaning,'',f'- 本地：[ {path} ](../ref-code/{repo}/{path})，第 {lo}–{hi} 行。','']
(R/'metadata/code_evidence.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));(R/'analysis/04_源码证据索引.md').write_text('\n'.join(lines))
