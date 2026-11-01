from pathlib import Path
from PIL import Image, ImageOps

HERE = Path(__file__).resolve().parent
RAW = HERE / "raw300"

# Coordinates are in pixels for the 300 dpi page renders. Crops retain the
# original figure graphics and are labelled in the Markdown with source/page.
CROPS = {
    "original_P01_fig2_pyfr_architecture.png": ("P01-05.png", (110, 150, 2160, 1090)),
    "original_P01_fig4_pyfr_task_graph.png": ("P01-06.png", (260, 150, 2050, 2470)),
    "original_P02_fig4_galaexi_flow.png": ("P02-08.png", (100, 60, 1290, 2100)),
    "original_P02_fig7_galaexi_weak_scaling.png": ("P02-13.png", (1370, 720, 2390, 1770)),
    "original_P20_fig1_libceed_operator.png": ("P20-2.png", (600, 1020, 2410, 2580)),
    "original_P19_fig2_petsc_backends.png": ("P19-02.png", (20, 1900, 1250, 3030)),
}

for outname, (srcname, crop) in CROPS.items():
    src = Image.open(RAW / srcname).convert("RGB")
    img = src.crop(crop)
    img = ImageOps.expand(img, border=18, fill="white")
    img.save(HERE / outname, dpi=(300, 300), optimize=True)
    print(outname, img.size)
