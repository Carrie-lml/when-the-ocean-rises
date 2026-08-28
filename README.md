# When the Ocean Rises

**When the Ocean Rises** is an interactive story map about sea-level rise, population exposure in Funafuti, Tuvalu, and the living Tuvaluan community connection with Aotearoa New Zealand. It was created for the **2026 Pacific Dataviz Challenge — Main Competition, Interactive Dataviz**.

## Project status

The analytical pipeline, threshold maps, population exposure estimates,
sea-level chart and New Zealand section are complete. The current build has
passed the project's automated validation checks and local desktop/mobile
visual QA. The repository is ready for GitHub publication and GitHub Pages
deployment.

## What the project shows

The site combines two separate pieces of evidence:

- observed sea-level anomalies for Tuvalu from the Pacific Data Hub / SPC,
  covering 1993–2023;
- illustrative 0.0, +0.5, +1.0, +1.5 and +2.0 m elevation thresholds applied
  to the Funafuti DEM.

The thresholds are not forecast years and are not calculated from the observed
SPC series.

The spatial analysis is an elevation-threshold screening model. It compares
ASTER DEM elevation with each selected threshold and estimates the WorldPop
population overlapping pixels at or below that level. It does not model tides,
waves, wave run-up, storm surge, groundwater flooding, drainage, erosion,
coastal defences, hydrodynamic connectivity or future shoreline change.

The results are used as screening-level exposure estimates rather than precise
flood extents.

## Current model outputs

The committed analysis output reports a DEM-positive baseline area of **3.502 km²** and a rounded model population baseline of **5,905** people. These are analytical grid quantities, not official Funafuti area/population statistics:

- baseline land is the set of valid ASTER DEM pixels above 0 m inside the Funafuti study-area clip;
- the model population baseline is the WorldPop population overlapping those DEM-positive pixels after alignment to the DEM grid;
- the native clipped WorldPop population estimate totals about **6,320** before the DEM-positive land mask is applied.

Current scenario outputs:

| Scenario | DEM-positive area at/below threshold | Population exposed |
|---|---:|---:|
| Baseline (0.0 m) | 0.0% | 0 |
| +0.5 m | 0.0% | 0 |
| +1.0 m | 15.5% | 201 |
| +1.5 m | 15.5% | 201 |
| +2.0 m | 27.7% | 532 |

ASTER GDEM elevations are stored in whole metres. The repeated +1.0 m / +1.5 m
result and the zero +0.5 m result therefore reflect DEM quantisation as well as
the broader vertical limitations of ASTER over a very low, narrow coral atoll.
The 0.5 m slider increments do **not** imply 0.5 m DEM precision.

Population alignment uses nearest-neighbour resampling to the DEM grid, explicit
NoData removal, and rescaling of the aligned values so that the total matches
the native clipped WorldPop population total.


## Tuvalu context

The **2022–23 Tuvalu Population and Housing Census** recorded a resident
population of **10,632**. Funafuti accounted for **6,602 residents by region of
enumeration**, or about **62.1%** of the national resident population.

Recent LiDAR topography published by Wandres et al. (2024) gives a national
mean elevation of **1.55 m above mean sea level** and a Funafuti mean of
**1.48 m**. The same study reports a Funafuti maximum of **6.93 m**, noting that
this local high point is associated with human-modified ground.

These contextual figures are stored in
`data/reference/context_stats.json` and injected into the site during the build.

## New Zealand context

New Zealand's **2023 Census** recorded **6,585 usual residents identifying with
the Tuvaluan ethnic group**.

Stats NZ recorded **3,537** in 2013, **4,653** in 2018 and **6,585** in 2023.
The increase from 2013 to 2023 is about **86%**.

In 2023, **67.1%** of New Zealand's Tuvaluan ethnic group had their usual
residence in the **Auckland region**. Stats NZ census counts use fixed random
rounding, so individual figures may not sum exactly.

The Pacific Access Category is a ballot-based New Zealand residence pathway for
eligible citizens of participating Pacific countries. For the **2026 ballot,
75 residence places were available to Tuvalu citizens**.

These statistics describe a strong trans-Pacific community connection. They do
not show why individual people migrated and are not used to attribute migration
to climate change.

## Data flow

Model outputs and contextual statistics are kept separate.

```text
ASTER DEM + WorldPop
        ↓
01_flood_exposure_analysis.ipynb
        ↓
output/sea_level_scenarios.json
        ↓
05_build_html.ipynb

ASTER threshold masks
        ↓
02_export_geojson.ipynb
        ↓
output/geojson/combined.json
        ↓
05_build_html.ipynb

Pacific Data Hub / SPC CSV
        ↓
04_sea_level_trend.ipynb
        ↓
output/sea_level_trend.json
        ↓
05_build_html.ipynb

Tuvalu CSD + Stats NZ + INZ + LiDAR references
        ↓
data/reference/context_stats.json
        ↓
05_build_html.ipynb
```

`03_validate_data.ipynb` runs before the analysis notebooks and checks the
processed rasters and contextual statistics.

## Repository structure

```text
.
├── index.html                     # redirects to the deployable site in /docs
├── docs/
│   └── index.html                 # GitHub Pages-ready final story map
├── web/
│   ├── index_template.html        # source template for story, copy and styling
│   └── index.html                 # generated local-preview build
├── notebooks/
│   ├── clip_data_to_funafuti.ipynb
│   ├── 01_flood_exposure_analysis.ipynb
│   ├── 02_export_geojson.ipynb
│   ├── 03_validate_data.ipynb
│   ├── 04_sea_level_trend.ipynb
│   ├── 05_build_html.ipynb
│   └── run_pipeline.py            # executes the post-clipping notebook pipeline
├── data/
│   ├── raw/
│   └── reference/
│       ├── context_stats.json
│       └── statsnz_tuvaluan_ethnic_group_2023.csv
├── output/
│   ├── data_validation_report.json
│   ├── sea_level_scenarios.json
│   ├── sea_level_trend.json
│   └── geojson/
│       ├── combined.json
│       ├── s0.geojson
│       ├── s05.geojson
│       ├── s10.geojson
│       ├── s15.geojson
│       └── s20.geojson
├── DATA_SOURCES.md
├── DATA_VALIDATION.md
├── requirements.txt
└── README.md
```

## Portable paths

All active project code has been refactored to avoid machine-specific absolute filesystem paths. Paths are resolved from the repository structure at runtime.

The notebooks use only project-relative paths and support the two common Jupyter launch patterns:

- launch Jupyter from the repository root, or
- launch Jupyter from `notebooks/`.

Stored notebook outputs have been cleared so the repository does not retain historical local-machine paths.

## Rebuild the site

Create an environment and install dependencies:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

For the normal reproducible rebuild, when the processed Funafuti rasters already
exist, run from the repository root:

```bash
python notebooks/run_pipeline.py
```

The pipeline executes:

```text
03_validate_data.ipynb
    ↓
01_flood_exposure_analysis.ipynb
    ↓
02_export_geojson.ipynb
    ↓
04_sea_level_trend.ipynb
    ↓
05_build_html.ipynb
    ↓
web/index.html + docs/index.html
```

`clip_data_to_funafuti.ipynb` is only needed when the processed Funafuti rasters are recreated.

If you change only copy/CSS/JS in `web/index_template.html`, a build-only run of
`05_build_html.ipynb` is sufficient.

`web/index.html` and `docs/index.html` are generated from `web/index_template.html`.


## Local preview

From the repository root:

```bash
python -m http.server 8000
```

Then open `http://localhost:8000/docs/`.

A local HTTP server gives behaviour closer to the deployed GitHub Pages site.

## GitHub Pages

The simplest deployment is:

1. push this repository to GitHub;
2. open **Settings → Pages**;
3. choose **Deploy from a branch**;
4. choose your main branch and the **`/docs`** folder;
5. save and test the published URL in a private/incognito window and on mobile.

The root `index.html` is also a small redirect to `docs/` for convenience.

## Validation

The current generated validation report is written to
`output/data_validation_report.json`. The final build passes all configured
checks.

The notebooks check:

- raster CRS, extent and native grid differences;
- ASTER elevation range against recent LiDAR context;
- native clipped WorldPop total;
- required contextual statistics and arithmetic;
- scenario ordering and population accounting;
- raster-to-GeoJSON area differences after vector simplification;
- complete SPC annual coverage from 1993 to 2023;
- equality between the parsed SPC series and the saved sea-level JSON;
- unresolved build placeholders and obsolete scenario labels.

`02_export_geojson.ipynb` uses a **5 m simplification tolerance**. It compares
the exported polygon area with the source raster mask and stops if the
difference exceeds **3%**.

The native WorldPop clip remains close to Funafuti's 2017 resident population
of **6,320**. That comparison is used as a reasonableness check only; WorldPop
2020 is a modelled population surface, not a census count.

## AI-assisted development

AI tools were used as supporting tools for coding assistance, debugging,
interface iteration and copy editing. Dataset selection, spatial-analysis scope,
methodological decisions, validation, interpretation and final editorial
judgement were undertaken and reviewed by the entrant.

## Data and citations

The main analytical datasets are Pacific Data Hub / SPC Sea Level Anomalies,
ASTER GDEM V3, WorldPop 2020 R2025A v1 and OpenStreetMap-derived study-area
context.

Contextual sources include the Tuvalu Central Statistics Division 2017
Mini-Census and 2022–23 Population and Housing Census, Wandres et al. (2024)
LiDAR elevation statistics (DOI `10.1029/2023EF003924`), Stats NZ census data
and Immigration New Zealand Pacific Access Category information.

See **[DATA_SOURCES.md](DATA_SOURCES.md)** for full citations, reference periods
and licence notes.

## Challenge submission

The site is designed for deployment through GitHub Pages from the `main`
branch and `/docs` folder. Before submission, the public URL should be tested
in a private/incognito browser window to confirm that MapLibre, OpenStreetMap
tiles, external fonts, the NASA image, the scenario slider and the
Funafuti/Auckland interaction all load correctly.

The official Challenge rules require an interactive entry to be publicly
accessible by URL and to remain accessible until at least **31 August 2029**.
The registration form also requires a problem statement explaining the problem
addressed and how the dataviz responds.
