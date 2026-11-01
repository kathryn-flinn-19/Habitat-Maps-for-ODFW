# Habitat Maps for ODFW

An OSU CS Capstone project for the Oregon Department of Fish and Wildlife (ODFW). The goal is an accessible tool that lets wildlife experts view and edit species range and habitat maps, built from existing USGS maps and from machine-learning approaches, and that is easy to download, run and use.

**Status:** design phase (fall 2026). The team is choosing the application's stack; see [Risks](docs/risks.md), R-1. What runs today is the starter script provided by ODFW, which the team has annotated: it turns a USGS Gap Analysis Project (GAP) species habitat model into a habitat map, using three of the project's eleven planned data sources. It runs for one species, the kit fox, and saves a PNG.

## How the starter script works

`starter_script/script.py` builds one yes/no layer per rule and keeps the cells where every rule is true:

1. **Land cover:** the cell's GAP land cover class is one of the species' primary ecosystems.
2. **Elevation:** the cell is within the model's minimum and maximum elevation.
3. **Hydrography:** the cell is within the model's distance buffers from or into flowing water, open water or wet vegetation.
4. **Range:** the cell is inside the species' known range polygon, when one is configured.

It does this separately for the GAP Northwest and Southwest regions, merges them, and draws the map in the Albers equal-area projection (EPSG:5070).

## Quickstart

From a clean clone to `figures/kit_fox_habitat_map-updated2.png`. Plan for the data downloads to take a while; they are large.

### 1. Clone the repository

```bash
git clone https://github.com/kathryn-flinn-19/Habitat-Maps-for-ODFW.git
cd Habitat-Maps-for-ODFW/starter_script
```

### 2. Create the Python environment

Follow the [starter script setup guide](starter_script/README.md) to install conda and the dependencies (matplotlib, geopandas, rasterio). It also covers adding conda to your PATH on Windows.

### 3. Download the GAP data

Download each dataset from USGS ScienceBase and unzip it so the folders below exist inside `starter_script/`:

| Dataset | Download | Folder the script expects |
|---------|----------|---------------------------|
| GAP land cover, Northwest | [ScienceBase](https://www.sciencebase.gov/catalog/item/5540e2d7e4b0a658d79395db) | `data/gap_map/northwest/lcgap_nw` |
| GAP land cover, Southwest | same page | `data/gap_map/southwest/lcgap_sw` |
| Elevation, Northwest | [ScienceBase](https://www.sciencebase.gov/catalog/item/5540e111e4b0a658d79395d9) | `data/elevation/northwest/elev_nw` |
| Elevation, Southwest | same page | `data/elevation/southwest/elev_sw` |
| Hydrography, Northwest | [ScienceBase](https://www.sciencebase.gov/catalog/item/5540eb44e4b0a658d7939624) | `data/hydrography/GAPHydroData/nw` |

The kit fox habitat model, range, iNaturalist observations and US state boundaries are already in `data/`.

Do not commit these downloads; they are too large for GitHub. Never commit data ODFW shares with the team that is not public, or paste it into AI tools; see [Contributing](CONTRIBUTING.md).

### 4. Point the script at your data

The data paths are set in the code. Replace the `C:/Users/super/...` paths with paths on your machine. Paths relative to `starter_script/` work, as long as you run the script from that folder.

In `script.py`, class `RegionalDataLayers`:

```python
northwest: RegionPaths = RegionPaths(
    gap_land_cover=Path("data/gap_map/northwest/lcgap_nw"),
    elevation=Path("data/elevation/northwest/elev_nw"),
    hydrography=Path("data/hydrography/GAPHydroData/nw"),
)
southwest: RegionPaths = RegionPaths(
    gap_land_cover=Path("data/gap_map/southwest/lcgap_sw"),
    elevation=Path("data/elevation/southwest/elev_sw"),
)
state_boundaries: Path = Path("data/boundaries/cb_2024_us_state_20m.shp")
```

In `data/species/kit_fox/kit_fox.yaml`:

```yaml
habitat_model: data/species/kit_fox/mKIFOx_CONUS_HabModel_2001v1.json
species_range: data/species/kit_fox/mKIFOx_CONUS_Range_2001v1.shp
inaturalist_observations: data/species/kit_fox/inaturalist/observations-758741.csv
```

Leave these edits out of your commits so other machines keep working.

### 5. Run it

From `starter_script/`:

```bash
mkdir figures
python script.py
```

The script prints `Saved figures/kit_fox_habitat_map-updated2.png` when it finishes. Habitat cells are light blue and iNaturalist sightings are red dots.

## Adding a species

1. Download the species' GAP habitat model (JSON) and range (shapefile) from ScienceBase into `data/species/<species>/`.
2. Optionally export its sightings from iNaturalist as CSV with `latitude` and `longitude` columns.
3. Write `data/species/<species>/<species>.yaml` with `habitat_model` (required), `species_range` and `inaturalist_observations` (both optional).
4. Add a function like `kit_fox_main()` in `script.py` that calls `plot_species_habitat` with that YAML, and call it from `main()`.

The habitat model JSON must contain both a Northwest and a Southwest model. `yuma_bat_main()` and `western_toad_main()` are stubs; their config files do not exist yet.

## Project layout

```
.github/workflows/ci.yml   CI (placeholder: checks out the repo only)
docs/                      Requirements, design and risk register
starter_script/
  script.py                The habitat map pipeline
  README.md                Detailed Windows/conda setup notes
  data/boundaries/         US state boundaries (Census, 2024)
  data/species/kit_fox/    GAP habitat model, range and iNaturalist sightings
```

## Known limitations

- Data paths are hard-coded, so each machine must edit the code before running (see `docs/risks.md`, R-2).
- There are no automated tests; CI only checks out the repo (R-3, R-7).
- The Southwest region has no hydrography layer, so water rules are skipped there.
- When a species' model sets no water buffers for a region, as the kit fox's Northwest model does, the hydrography layer marks every cell in that region as unsuitable, so the map shows no habitat there.
- The map plots every iNaturalist observation, including ones not yet research grade.
- The GAP models and land cover describe conditions around 2001.
- Output is a PNG image only.

## Documentation

- [Requirements](docs/requirements.md)
- [Technical design](docs/design.md)
- [Risk register](docs/risks.md)
- [Contributing](CONTRIBUTING.md)
- [AI context](AGENTS.md)

## Data sources

- USGS Gap Analysis Project species habitat models, land cover, elevation and hydrography, via [ScienceBase](https://www.sciencebase.gov/).
- U.S. Census Bureau cartographic boundary file `cb_2024_us_state_20m`.
- Kit fox observations from [iNaturalist](https://www.inaturalist.org/), shared by their observers under the license on each record.

## Team

Oregon State University CS Capstone, working with the Oregon Department of Fish and Wildlife. Roles rotate each term; for fall 2026:

| Role | Name |
|------|------|
| Project Manager | Julie Feldhousen |
| Quality Owner (repo, CI, releases) | Adison Daggett |
| AI Coordinator; Testing and QA Lead | Jae Grunwald |
| Documentation Manager | Kathryn Flinn |

For setup or CI problems, contact the Quality Owner. For questions about scope or the partner, contact the Project Manager. How to contribute is in [CONTRIBUTING.md](CONTRIBUTING.md).

## License

No license has been chosen yet; until one is, all rights are reserved by the authors.
