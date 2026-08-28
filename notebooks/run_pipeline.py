"""
Run the submission pipeline from processed Funafuti rasters to final HTML.

Default order:
03_validate_data.ipynb
01_flood_exposure_analysis.ipynb
02_export_geojson.ipynb
04_sea_level_trend.ipynb
05_build_html.ipynb

Usage from repository root:
    python notebooks/run_pipeline.py

If the processed Funafuti rasters do not yet exist and you intentionally want
to re-fetch the OSM boundary and re-clip the raw rasters:
    python notebooks/run_pipeline.py --include-clip
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


NOTEBOOKS = [
    "03_validate_data.ipynb",
    "01_flood_exposure_analysis.ipynb",
    "02_export_geojson.ipynb",
    "04_sea_level_trend.ipynb",
    "05_build_html.ipynb",
]


def run_notebook(path: Path) -> None:
    print(f"\n=== Running {path.name} ===")
    cmd = [
        sys.executable,
        "-m",
        "jupyter",
        "nbconvert",
        "--to",
        "notebook",
        "--execute",
        "--inplace",
        "--ExecutePreprocessor.timeout=900",
        str(path),
    ]
    subprocess.run(cmd, check=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--include-clip",
        action="store_true",
        help="Run clip_data_to_funafuti.ipynb first. Requires internet access and raw rasters.",
    )
    args = parser.parse_args()

    notebooks_dir = Path(__file__).resolve().parent
    project_root = notebooks_dir.parent

    if not (project_root / "web" / "index_template.html").exists():
        raise FileNotFoundError(
            "web/index_template.html was not found. "
            "Place this notebooks folder inside the project repository."
        )

    if args.include_clip:
        run_notebook(notebooks_dir / "clip_data_to_funafuti.ipynb")

    required_processed = [
        project_root / "data" / "raw" / "tuvalu_dem_funafuti_admin.tif",
        project_root / "data" / "raw" / "tuvalu_pop_funafuti_admin.tif",
        project_root / "data" / "raw" / "official_sea_level_anomalies_tuvalu.csv",
    ]
    missing = [p for p in required_processed if not p.exists()]
    if missing:
        print("\nMissing required input(s):")
        for p in missing:
            print(" -", p)
        print(
            "\nIf the processed rasters are missing, run with --include-clip "
            "after confirming the raw ASTER and WorldPop files are present."
        )
        raise SystemExit(1)

    for name in NOTEBOOKS:
        run_notebook(notebooks_dir / name)

    preview = project_root / "web" / "index.html"
    deploy = project_root / "docs" / "index.html"
    if not preview.exists() or not deploy.exists():
        raise FileNotFoundError("Build finished but one or both index.html outputs are missing.")

    if preview.read_bytes() != deploy.read_bytes():
        raise RuntimeError("web/index.html and docs/index.html are not identical.")

    print("\nPipeline complete.")
    print("Local preview:", preview)
    print("GitHub Pages:", deploy)
    print("\nPreview command:")
    print(f'  cd "{project_root / "web"}"')
    print("  py -m http.server 8000")
    print("Then open http://localhost:8000")


if __name__ == "__main__":
    main()
