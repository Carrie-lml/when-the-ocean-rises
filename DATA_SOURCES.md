# Data sources and evidence roles

This project keeps analytical inputs, analytical outputs and contextual
references separate. Values calculated from project data are produced by the
notebooks. External facts and official statistics are stored as references and
cited with their original source.

Last source review: **28 August 2026**.

## 1. Pacific Data Hub / SPC — Sea Level Anomalies

**Role:** analytical input and official 2026 Pacific Dataviz Challenge dataset.

- Geography: Tuvalu
- Period used: 1993–2023
- Frequency: annual
- Dataflow: `SPC:DF_CLIMATE_CHANGE`
- Indicator: Sea Level Anomalies
- Project output: `output/sea_level_trend.json`
- Processing notebook: `notebooks/04_sea_level_trend.ipynb`

The notebook checks that the parsed series contains exactly 31 annual
observations from 1993 through 2023, with no missing or duplicate years. The
saved JSON is then read back and compared with the parsed CSV series.

The observed SPC series is independent of the +0.5 m, +1.0 m, +1.5 m and
+2.0 m elevation thresholds. It is not used to assign dates to those
thresholds.

Source: Pacific Data Hub / Pacific Community (SPC), Climate Change Indicators,
dataflow `SPC:DF_CLIMATE_CHANGE`.

## 2. ASTER Global Digital Elevation Model V3

**Role:** analytical input for the Funafuti elevation-threshold model.

Citation:

> NASA/METI/AIST/Japan Spacesystems and U.S./Japan ASTER Science Team
> (2019). *ASTER Global Digital Elevation Model V003*. NASA EOSDIS Land
> Processes DAAC. DOI: `10.5067/ASTER/ASTGTM.003`.

Project use:

- ASTER is clipped to the Funafuti study area;
- valid DEM pixels above 0 m define the analytical baseline land mask;
- threshold exposure is calculated by comparing DEM elevation with 0.0, 0.5,
  1.0, 1.5 and 2.0 m;
- raster masks are converted to GeoJSON in
  `notebooks/02_export_geojson.ipynb`.

The current GeoJSON export uses a **5 m simplification tolerance**. Raster and
vector areas are compared after export and the notebook stops if the difference
exceeds the project QA limit.

ASTER GDEM V3 uses 1 arc-second posting and stores DEM elevations as integer
metres. NASA documentation also notes residual errors and artefacts. These
limitations are material for a very low coral atoll, so the project treats the
results as screening-level elevation exposure rather than precise flood
boundaries.

The LiDAR statistics shown in the introduction are an external topographic
reference only. They are not substituted into the ASTER-based model.

## 3. WorldPop 2020 Population Counts, R2025A v1

**Role:** analytical input for population exposure.

Citation:

> Bondarenko M., Priyatikanto R., Tejedor-Garavito N., Zhang W., McKeen T.,
> Cunningham A., Woods T., Hilton J., Cihan D., Nosatiuk B., Brinkhoff T.,
> Tatem A., Sorichetta A. (2025). *Constrained estimates of 2015–2030 total
> number of people per grid square at a resolution of 3 arc seconds
> (approximately 100 m at the equator), R2025A version v1*. WorldPop,
> University of Southampton. DOI: `10.5258/SOTON/WP00839`.

- Reference year used: 2020
- Native resolution: 3 arc seconds, approximately 100 m at the equator
- Product type: modelled population estimate
- Licence: CC BY 4.0
- Native clipped Funafuti total in the current analysis: approximately **6,320
  modelled people**

Processing in `01_flood_exposure_analysis.ipynb`:

- clipped to the Funafuti study area;
- reprojected to the ASTER grid using nearest-neighbour resampling;
- NoData values removed explicitly;
- aligned values rescaled so their total matches the native clipped WorldPop
  total before exposure is calculated.

The current DEM-positive model baseline is approximately **5,905 people**. This
is not a census count; it is the modelled population overlapping valid ASTER
pixels above 0 m.

The native 2020 WorldPop total of about 6,320 is close to Funafuti's 2017 census
resident population of 6,320. That comparison is used only as a reasonableness
check.

## 4. Tuvalu Central Statistics Division

**Role:** contextual population reference and WorldPop sanity check.

### 2022–23 Population and Housing Census

Official page:
`https://stats.gov.tv/news/tuvalu-population-and-housing-census-2022-23/`

Values used in the site:

- Tuvalu resident population: **10,632**
- Funafuti resident population by region of enumeration: **6,602**
- Derived Funafuti share: **62.1%**

The 62.1% figure is calculated during the build from `6,602 / 10,632`, rather
than stored as an independent source value.

### 2017 Mini-Census

Values retained for historical/context validation:

- Tuvalu resident population: **10,507**
- Funafuti resident population: **6,320**

The 2017 Funafuti value is used only as a sanity reference for the WorldPop
2020 native clipped total.

## 5. Wandres et al. (2024) — LiDAR topography

**Role:** contextual elevation benchmark. It is not an input to the ASTER
threshold model.

Citation:

> Wandres, M. et al. (2024). *A National-Scale Coastal Flood Hazard Assessment
> for the Atoll Nation of Tuvalu*. Earth's Future, 12(4).
> DOI: `10.1029/2023EF003924`.

Values referenced:

- Tuvalu mean elevation: **1.55 m above MSL**
- Funafuti mean elevation: **1.48 m above MSL**
- Funafuti maximum mapped elevation: **6.93 m above MSL**

The paper notes that the Funafuti local maximum is associated with
human-modified ground. For that reason, the site foregrounds the national mean
rather than presenting 6.93 m as a simple natural "highest point".

## 6. Stats NZ — Tuvaluan ethnic group

**Role:** contextual New Zealand population evidence.

Official summary:
`https://tools.summaries.stats.govt.nz/ethnic-group/tuvaluan`

Figures used:

- 2013: **3,537**
- 2018: **4,653**
- 2023: **6,585**
- Auckland regional council area of usual residence, 2023: **67.1%**

The 2013–2023 increase shown as "about 86%" is calculated from the published
counts:

`(6,585 - 3,537) / 3,537 = 86.17%`.

The 67.1% figure is taken directly from Stats NZ's **regional council area of
usual residence** output. It is not reconstructed from Auckland local-board
counts.

Stats NZ states that the data are for the census usually resident population
count. Ethnicity is self-identified and is not the same as citizenship,
nationality or country of birth. Census counts are subject to fixed random
rounding for confidentiality, so individual figures may not sum exactly to
published totals.

Licence: Stats NZ content is generally available under Creative Commons
Attribution 4.0 unless otherwise stated on the source.

## 7. Immigration New Zealand — Pacific Access Category

**Role:** contextual evidence for an established New Zealand residence pathway.

2026 ballot results:
`https://www.immigration.govt.nz/about-us/news-centre/2026-pacific-access-category-ballot-results/`

Value used:

- 2026 Tuvalu quota: **75 residence places**

Immigration New Zealand explains that quota places refer to the number of
people who can be granted residence, not the number of ballot registrations
drawn. Ballot registrations can include more than one family member.

Historical establishment:
`https://www.beehive.govt.nz/release/government-announces-pacific-access-scheme`

The project does not use PAC figures to infer individual migration motives.

## 8. OpenStreetMap

**Role:** study-area boundary derivation and map context.

- Map attribution is displayed in the interactive map.
- Copyright/licence information:
  `https://www.openstreetmap.org/copyright`

The Funafuti clip is described as an **OpenStreetMap-derived study area**, not
as an authoritative official administrative boundary.

## 9. NASA Earth Observatory — Funafuti image

**Role:** visual context in the introduction.

NASA Earth Observatory:
`https://science.nasa.gov/earth/earth-observatory/funafuti-atoll-tuvalu-153047/`

- Instrument: Landsat 8 Operational Land Imager (OLI)
- Acquisition date: 28 September 2023
- Image credit: NASA Earth Observatory / Wanmei Liang, using Landsat data from
  the U.S. Geological Survey

The credit remains visible below the image in the site.

## Reference periods

| Source | Reference period |
|---|---|
| SPC Sea Level Anomalies | 1993–2023 |
| ASTER GDEM V3 | product V3; scenes used by the product span earlier years |
| WorldPop | 2020 modelled estimate |
| Tuvalu Census | 2022–23 |
| Tuvalu Mini-Census | 2017 |
| Wandres et al. LiDAR | published 2024 |
| Stats NZ | 2013, 2018 and 2023 Census |
| Pacific Access Category | 2026 ballot; scheme established in 2002 |
| NASA Funafuti image | 28 September 2023 |

These sources represent different reference periods. The website keeps their
roles and dates explicit rather than treating them as a single-year snapshot.
