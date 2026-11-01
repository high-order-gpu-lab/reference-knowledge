from __future__ import annotations

import csv
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle
import numpy as np


ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
OUT.mkdir(parents=True, exist_ok=True)

mpl.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Noto Sans CJK SC", "DejaVu Sans", "sans-serif"],
        "font.size": 9,
        "axes.spines.right": False,
        "axes.spines.top": False,
        "axes.linewidth": 0.8,
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "figure.dpi": 160,
    }
)

BLUE = "#3B6EA8"
TEAL = "#2A9D8F"
ORANGE = "#E68A3A"
RED = "#C95C5C"
INK = "#263238"
MUTED = "#6C7886"
PALE_BLUE = "#EAF2F8"
PALE_TEAL = "#E8F5F2"
PALE_ORANGE = "#FFF1E2"
PALE_GRAY = "#F4F6F8"


def save(fig, name: str) -> None:
    fig.savefig(OUT / f"{name}.png", dpi=360, bbox_inches="tight", facecolor="white")
    fig.savefig(OUT / f"{name}.svg", bbox_inches="tight", facecolor="white")
    fig.savefig(OUT / f"{name}.pdf", bbox_inches="tight", facecolor="white")
    fig.savefig(OUT / f"{name}.tiff", dpi=600, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def box(ax, x, y, w, h, text, fc=PALE_BLUE, ec=BLUE, fs=9, lw=1.2, radius=0.025):
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0.012,rounding_size={radius}",
        facecolor=fc, edgecolor=ec, linewidth=lw,
        transform=ax.transAxes,
    )
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", color=INK,
            fontsize=fs, transform=ax.transAxes, wrap=True)


def arrow(ax, x1, y1, x2, y2, color=BLUE, lw=1.2, style="-|>", connectionstyle="arc3"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), transform=ax.transAxes,
                                 arrowstyle=style, mutation_scale=12,
                                 linewidth=lw, color=color,
                                 connectionstyle=connectionstyle))


def framework_architecture():
    fig, ax = plt.subplots(figsize=(12.2, 7.1))
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.text(0.02, 0.965, "高阶有限元 GPU 框架的三层架构对比（依据源码与论文归纳）",
            fontsize=14, fontweight="bold", color=INK, transform=ax.transAxes)
    ax.text(0.02, 0.925, "同一层表示相近职责；框架之间的差异主要体现在算子组织、设备数据生命周期和后端特化位置。",
            fontsize=9, color=MUTED, transform=ax.transAxes)

    layers = [(0.73, 0.14, "算法/编排层", PALE_BLUE, BLUE),
              (0.48, 0.14, "算子与 Kernel 层", PALE_TEAL, TEAL),
              (0.23, 0.14, "运行时/后端层", PALE_ORANGE, ORANGE)]
    for y, h, label, fc, ec in layers:
        ax.add_patch(Rectangle((0.02, y), 0.96, h, transform=ax.transAxes,
                               facecolor=fc, edgecolor=ec, linewidth=1.1, alpha=0.55))
        ax.text(0.035, y + h - 0.035, label, fontsize=10, fontweight="bold",
                color=ec, transform=ax.transAxes)

    names = ["PyFR", "GALÆXI", "HORSES3D-GPU", "HiFiLES", "MFEM"]
    xs = np.linspace(0.15, 0.85, len(names))
    for x, name in zip(xs, names):
        ax.text(x, 0.88, name, ha="center", va="center", fontsize=10,
                fontweight="bold", color=INK, transform=ax.transAxes)

    top = ["残差计算图\n时间积分/通信依赖", "DGSEM 阶段\n弱式/分裂式", "对象式残差\n内部面/MPI面分支", "FR/CPR 残差\nRK stage", "Operator / PA\n隐式求解组合"]
    mid = ["矩阵乘、面核、\npointwise、graph", "VolInt / SurfInt /\nConsToPrim / FillFlux", "单元 gang、节点\nvector、局部累加", "GEMM + bespoke\nCUDA kernel", "张量 PA、Q-function、\nJacobian/预条件器"]
    bot = ["CUDA/HIP provider\nGiMMiK、task graph", "CUDA Fortran、\nstream、CUDA-aware MPI", "OpenACC、present/async\nMPI", "CUDA、cuBLAS、\n显式镜像", "Device/Memory、\nCUDA/HIP/RAJA/OCCA"]
    for x, a, b, c in zip(xs, top, mid, bot):
        box(ax, x - 0.085, 0.765, 0.17, 0.075, a, PALE_BLUE, BLUE, fs=8)
        box(ax, x - 0.085, 0.515, 0.17, 0.075, b, PALE_TEAL, TEAL, fs=8)
        box(ax, x - 0.085, 0.265, 0.17, 0.075, c, PALE_ORANGE, ORANGE, fs=8)
        arrow(ax, x, 0.76, x, 0.595, color=MUTED)
        arrow(ax, x, 0.51, x, 0.345, color=MUTED)

    ax.text(0.02, 0.105, "跨框架共同点：单元局部算子适合设备执行；面/MPI耦合决定同步边界；隐式端还需把 Jacobian、Krylov、预条件和归约纳入同一链条。",
            fontsize=9, color=INK, transform=ax.transAxes)
    ax.text(0.02, 0.065, "图例：蓝色=算法编排；绿色=算子与 Kernel；橙色=后端、运行时和硬件接口。",
            fontsize=8.5, color=MUTED, transform=ax.transAxes)
    save(fig, "own_01_framework_architecture")


def kernel_storage_flow():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.0, 5.8), gridspec_kw={"width_ratios": [1.15, 1]})
    for ax in (ax1, ax2):
        ax.axis("off")
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
    fig.suptitle("Kernel 职责与存储生命周期：从残差到设备缓冲", fontsize=14, fontweight="bold", color=INK, y=0.98)
    ax1.text(0.02, 0.93, "A  方法/流程分解", fontsize=11, fontweight="bold", color=BLUE, transform=ax1.transAxes)
    steps = [
        ("状态/几何", "U, metric, face map", PALE_BLUE, BLUE),
        ("插值/限制", "体点、面点、积分点", PALE_TEAL, TEAL),
        ("点物理", "ConsToPrim、通量、物性", PALE_ORANGE, ORANGE),
        ("体/面算子", "VolInt、SurfInt、数值通量", "#FBE9E7", RED),
        ("通信/归约", "pack→MPI→unpack；CFL/范数", PALE_GRAY, MUTED),
        ("残差/QDot", "阶段更新或 Krylov apply", PALE_BLUE, BLUE),
    ]
    ys = np.linspace(0.78, 0.14, len(steps))
    for (title, desc, fc, ec), y in zip(steps, ys):
        box(ax1, 0.10, y, 0.77, 0.09, f"{title}\n{desc}", fc, ec, fs=8.5)
        if y > 0.15:
            arrow(ax1, 0.485, y - 0.005, 0.485, y - 0.085, color=MUTED)
    ax1.text(0.10, 0.035, "融合边界：共享中间量且无通信/归约依赖时可尝试；否则保留事件和可审计的写回边界。",
             fontsize=8.3, color=MUTED, transform=ax1.transAxes)

    ax2.text(0.02, 0.93, "B  存储生命周期与所有权", fontsize=11, fontweight="bold", color=TEAL, transform=ax2.transAxes)
    phases = ["初始化", "每步/每阶段", "MPI halo", "隐式迭代", "输出/诊断"]
    px = np.linspace(0.18, 0.86, len(phases))
    for x, p in zip(px, phases):
        ax2.text(x, 0.82, p, ha="center", va="center", fontsize=8.5, color=INK, transform=ax2.transAxes)
        ax2.plot([x, x], [0.78, 0.18], color="#D5DDE5", lw=0.8, transform=ax2.transAxes)
    rows = [
        ("状态/阶段向量", 0.70, 0.16, BLUE),
        ("几何/算子表", 0.58, 0.06, TEAL),
        ("面/通信缓冲", 0.46, 0.20, ORANGE),
        ("Krylov/预条件器", 0.34, 0.24, RED),
        ("临时工作区", 0.22, 0.11, MUTED),
    ]
    for label, start, length, color in rows:
        ax2.text(0.03, start + 0.025, label, ha="left", va="center", fontsize=8.2, color=INK, transform=ax2.transAxes)
        x0 = 0.10 + (start * 0)  # keep the geometry explicit below
        start_idx = {0.70: 0, 0.52: 1, 0.34: 2}.get(start, 1)
        # map explicit phase spans to columns; this keeps the chart readable without implying byte values
        if label == "状态/阶段向量": x0, x1 = 0.28, 0.93
        elif label == "几何/算子表": x0, x1 = 0.28, 0.67
        elif label == "面/通信缓冲": x0, x1 = 0.42, 0.70
        elif label == "Krylov/预条件器": x0, x1 = 0.55, 0.93
        else: x0, x1 = 0.42, 0.60
        ax2.add_patch(FancyBboxPatch((x0, start), x1 - x0, 0.06,
                                     boxstyle="round,pad=0.006,rounding_size=0.01",
                                     transform=ax2.transAxes, facecolor=color, edgecolor=color, alpha=0.78))
        ax2.text((x0 + x1) / 2, start + 0.03, "设备驻留/按需复用", ha="center", va="center", fontsize=7.4,
                 color="white", transform=ax2.transAxes)
    ax2.text(0.03, 0.035, "生命周期要点：先登记语义、布局、所有权、最后写入队列和可读事件，再决定是否融合或回收。",
             fontsize=8.3, color=MUTED, transform=ax2.transAxes)
    save(fig, "own_02_kernel_storage_flow")


def event_timeline():
    fig, ax = plt.subplots(figsize=(12.5, 4.8))
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.text(0.02, 0.94, "设备面交换的可审计事件时间线（自绘）", fontsize=14, fontweight="bold", color=INK, transform=ax.transAxes)
    ax.text(0.02, 0.885, "目标不是假设通信被隐藏，而是逐事件记录 pack、MPI、wait、unpack 与后续面通量之间的完成关系。",
            fontsize=9, color=MUTED, transform=ax.transAxes)
    x0, x1 = 0.12, 0.94
    xs = np.linspace(x0, x1, 8)
    labels = ["S0\npack完成", "S1\nready event", "S2\nIsend/Irecv", "S3\n本地计算", "S4\nwait/event", "S5\nunpack完成", "S6\nMPI面通量", "S7\n残差更新"]
    for i, (x, label) in enumerate(zip(xs, labels)):
        ax.plot([x, x], [0.20, 0.78], color="#D5DDE5", lw=0.8)
        ax.scatter([x], [0.74], s=65, color=[BLUE, BLUE, ORANGE, TEAL, RED, RED, ORANGE, BLUE][i], zorder=3)
        ax.text(x, 0.80, label, ha="center", va="bottom", fontsize=8.3, color=INK, transform=ax.transAxes)
        if i < 7:
            ax.add_patch(FancyArrowPatch((x + 0.015, 0.74), (xs[i + 1] - 0.015, 0.74),
                                         transform=ax.transAxes, arrowstyle="-|>", mutation_scale=10,
                                         color=MUTED, linewidth=1.0))
    bands = [(0.57, 0.10, 2, 5, TEAL, "设备计算：内部单元/非 MPI 面"),
             (0.40, 0.10, 2, 4, ORANGE, "通信：发送、传输、接收"),
             (0.23, 0.10, 4, 7, BLUE, "面路径：unpack、MPI 面通量、残差更新")]
    for y, h, a, b, color, label in bands:
        xa, xb = xs[a] - 0.025, xs[b] + 0.025
        ax.add_patch(FancyBboxPatch((xa, y), xb - xa, h, boxstyle="round,pad=0.008,rounding_size=0.012",
                                    transform=ax.transAxes, facecolor=color, edgecolor=color, alpha=0.16))
        ax.text(xa + 0.01, y + h / 2, label, va="center", fontsize=8.2, color=color, transform=ax.transAxes)
    ax.text(0.02, 0.075, "审查规则：S2 前的全设备同步会取消 S3 重叠；S4 前缺少接收完成事件会导致 S5 竞态；S6/S7 共享工作区需明确写后读依赖。",
            fontsize=8.5, color=INK, transform=ax.transAxes)
    save(fig, "own_03_event_timeline")


def load_csv(name):
    with open(ROOT / "review" / "analysis" / "raw_data" / name, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def performance_evidence():
    py = load_csv("PyFR强扩展原始表.csv")
    ga = load_csv("GALAEXI显存原始表.csv")
    fig, axs = plt.subplots(1, 2, figsize=(12.6, 5.0))
    fig.suptitle("公开结果的可比性分析：扩展效率与每 DoF 显存是两类不同证据", fontsize=14, fontweight="bold", color=INK, y=1.02)

    for platform, color, marker in [("Frontier_MI250X", RED, "o"), ("Alps_GH200", BLUE, "s")]:
        rows = [r for r in py if r["platform"] == platform]
        gpus = [int(r["physical_GPUs"]) for r in rows]
        eff = [float(r["efficiency"]) for r in rows]
        axs[0].plot(gpus, eff, marker=marker, color=color, lw=2, ms=5, label=platform.replace("_", " "))
    axs[0].set_xscale("log", base=2)
    axs[0].set_ylim(0.35, 1.12)
    axs[0].set_xlabel("物理 GPU 数（论文口径）")
    axs[0].set_ylabel("相对 16-rank 强扩展效率")
    axs[0].set_title("PyFR v2.0.3：硬件与 MPI 感知设置不同")
    axs[0].grid(True, which="both", alpha=0.22)
    axs[0].legend(frameon=False, fontsize=8)
    axs[0].text(0.03, 0.05, "Frontier：2 GCD/卡，HIP-aware MPI 未启用\nAlps：1 GPU/rank，CUDA-aware MPI 启用",
                transform=axs[0].transAxes, fontsize=8, color=MUTED)

    n = [int(r["polynomial_degree"]) for r in ga]
    mem = [float(r["KiB_per_spatial_DoF"]) for r in ga]
    axs[1].plot(n, mem, color=TEAL, marker="o", lw=2, ms=4)
    axs[1].set_xlabel("多项式阶次 N")
    axs[1].set_ylabel("KiB / spatial DoF")
    axs[1].set_title("GALÆXI：显式 NS 设备显存随阶次变化")
    axs[1].grid(True, alpha=0.22)
    axs[1].annotate("N=7：0.869 KiB/DoF", xy=(7, 0.869), xytext=(7.6, 1.08),
                    arrowprops={"arrowstyle": "->", "color": TEAL}, fontsize=8.5, color=INK)
    axs[1].text(0.03, 0.05, "该表是显式 Navier–Stokes 的实际分配口径；\n不能直接当作隐式 Krylov/预条件器容量。",
                transform=axs[1].transAxes, fontsize=8, color=MUTED)
    save(fig, "own_04_performance_evidence")


def literature_timeline():
    years = [2013, 2014, 2016, 2017, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026]
    themes = ["DG/FR\n基础", "GPU\n算子", "生成核/\n混合网格", "隐式\nDG", "框架/\nPA", "后端/\n求解器", "CEED/\nKokkos", "LOR/\n网格", "矩阵自由/\nH(div)", "多 GPU/\n显存", "大规模\n扩展", "跨架构/\n硬件特化"]
    vals = np.array([
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    ], dtype=float).T
    fig, ax = plt.subplots(figsize=(12.8, 4.6))
    im = ax.imshow(vals, aspect="auto", cmap="Blues", vmin=0, vmax=1)
    ax.set_xticks(range(len(years)), years)
    ax.set_yticks(range(len(themes)), themes)
    ax.set_title("文献技术路线：从流式高阶算子到跨架构 GPU 求解", fontsize=14, fontweight="bold", color=INK, pad=16)
    ax.set_xlabel("文献首次公开/出版年份（依据目录日期）")
    ax.set_ylabel("主题标签（按调研报告归纳）")
    for i in range(vals.shape[0]):
        for j in range(vals.shape[1]):
            if vals[i, j] > 0:
                ax.text(j, i, "●", ha="center", va="center", color=BLUE, fontsize=12)
    ax.text(0.0, -0.28,
            "读图：早期工作先解决局部高阶算子与 GPU 核，随后转向矩阵自由/预条件器、设备常驻与多 GPU；2024 年后证据更多聚焦跨架构和硬件特化。\n注：热图为文献主题标签的归纳展示，不是论文数量统计；单篇文献可覆盖多个主题。",
            transform=ax.transAxes, fontsize=8.5, color=MUTED, va="top")
    save(fig, "own_05_literature_timeline")


if __name__ == "__main__":
    framework_architecture()
    kernel_storage_flow()
    event_timeline()
    performance_evidence()
    literature_timeline()
    print("generated", ", ".join(sorted(p.name for p in OUT.glob("own_*.png"))))
