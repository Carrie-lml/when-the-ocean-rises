# Data validation

Last reviewed: **28 August 2026**

This file records where each number used by the story comes from and how it is
checked. The final pipeline also writes
`output/data_validation_report.json` when `05_build_html.ipynb` runs.

## Provenance matrix

| Value shown in the site | Type | Source / calculation | Validation |
|---|---|---|---|
| 10,632 Tuvalu residents | Context reference | Tuvalu CSD 2022–23 Census | Official source checked |
| 6,602 Funafuti residents | Context reference | Tuvalu CSD 2022–23 Census | Official source checked |
| 62.1% Funafuti share | Derived context | `6602 / 10632 × 100` | Recalculated in build |
| 1.55 m national mean elevation | Context reference | Wandres et al. (2024) LiDAR | Peer-reviewed source checked |
| 1.48 m Funafuti mean elevation | Context reference | Wandres et al. (2024) LiDAR | Peer-reviewed source checked |
| 6.93 m Funafuti local maximum | Context reference | Wandres et al. (2024) LiDAR | Source checked; human-modified local high point noted |
| 6,320 Funafuti 2017 population | Context reference | Tuvalu 2017 Mini-Census | Used only as WorldPop sanity reference |
| ~6,320 native WorldPop total | Analysis output | WorldPop 2020 clipped raster | Calculated in `01_flood_exposure_analysis.ipynb` |
| 5,905 model baseline population | Analysis output | WorldPop aligned to ASTER positive-elevation pixels | Calculated in `01_flood_exposure_analysis.ipynb` |
| 3.502 km² model baseline area | Analysis output | ASTER pixels > 0 m | Calculated in `01_flood_exposure_analysis.ipynb` |
| 0 / 0 / 201 / 201 / 532 exposed people | Analysis output | ASTER + WorldPop thresholds | Calculated in `01_flood_exposure_analysis.ipynb` |
| 100 / 100 / 84.5 / 84.5 / 72.3% land above threshold | Derived analysis | `100 - land_loss_pct` | Calculated in build |
| GeoJSON threshold polygons | Analysis output | ASTER threshold masks | Exported in `02_export_geojson.ipynb`; raster/vector area QA |
| 31 SPC annual values, 1993–2023 | Analysis input/output | Pacific Data Hub / SPC CSV | Coverage and JSON round-trip checked in `04_sea_level_trend.ipynb` |
| 3,537 NZ Tuvaluan ethnic group, 2013 | Context reference | Stats NZ | Official source checked |
| 4,653 NZ Tuvaluan ethnic group, 2018 | Context reference | Stats NZ | Official source checked |
| 6,585 NZ Tuvaluan ethnic group, 2023 | Context reference | Stats NZ | Official source checked |
| about 86% growth, 2013–2023 | Derived context | `(6585 - 3537) / 3537 × 100` | Recalculated in build |
| 67.1% Auckland regional share | Context reference | Stats NZ regional council area of usual residence | Official source checked |
| 75 Tuvalu PAC residence places, 2026 | Context reference | Immigration New Zealand | Official source checked |

## Current generated-page checks

The latest generated HTML supplied for review contains:

- the 2022–23 Tuvalu census values (`10,632`, `6,602`, `62.1%`);
- the latest model baseline (`3.502 km²`, `5,905`, native WorldPop approximately
  `6,320`);
- scenario population exposure values `0, 0, 201, 201, 532`;
- Stats NZ values `3,537`, `4,653`, `6,585` and `67.1%`;
- the 2026 PAC value `75`;
- five scenario geometries carrying a `5.0 m` simplification metadata value;
- no old `10,099`, `4.6 m`, `5,904`, `200`, `~2050`, `~2080` or `~2100`
  story values.

## Interpretation controls

- SPC observations and DEM thresholds are separate evidence streams.
- WorldPop 2020 is a modelled population surface, not a census count.
- Stats NZ ethnicity is self-identified and is not equivalent to citizenship,
  nationality, birthplace or migration status.
- The 67.1% figure is the Auckland **regional council area** share, not the sum
  of Auckland local-board figures.
- LiDAR statistics provide independent topographic context; the threshold model
  itself uses ASTER GDEM.
- Scenario outputs are screening-level elevation exposure, not hydrodynamic
  flood predictions.

## Final run

Before submission, run:

```text
python notebooks/run_pipeline.py
```

The build should finish with all checks passing and write:

```text
output/data_validation_report.json
web/index.html
docs/index.html
```

`web/index.html` and `docs/index.html` should be identical.
