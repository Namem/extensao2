"""Export PPTX slides as PNG images using PowerPoint COM automation."""
import os
import win32com.client
import time

PPTX = r"C:\Users\Rachid\Desktop\NR\Semestre 2026_1\extensao\ceres-diagnostico\Pre_arquivos\SprintReview_1_CeresDiagnostico.pptx"
OUT_DIR = r"C:\Users\Rachid\Desktop\NR\Semestre 2026_1\extensao\ceres-diagnostico\Pre_arquivos\slides_qa"

os.makedirs(OUT_DIR, exist_ok=True)

print("Opening PowerPoint...")
ppt = win32com.client.Dispatch("PowerPoint.Application")
ppt.Visible = True

print(f"Opening: {PPTX}")
prs = ppt.Presentations.Open(PPTX, ReadOnly=True, Untitled=False, WithWindow=False)

n = prs.Slides.Count
print(f"Exporting {n} slides...")

for i in range(1, n + 1):
    out_path = os.path.join(OUT_DIR, f"slide-{i:02d}.png")
    slide = prs.Slides(i)
    slide.Export(out_path, "PNG", 1280, 720)
    print(f"  Exported slide {i}/{n} -> {out_path}")

prs.Close()
ppt.Quit()
print("Done.")
