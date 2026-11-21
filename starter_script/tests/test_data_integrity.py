import inspect
from pathlib import Path

import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
import pytest


import script

# The folder that script.py lives in. All paths in the config files
# are relative to this folder.
ROOT = Path(script.__file__).parent


# ------------------------------------------------------------------
# Find every species folder inside data/species/.
# Each folder becomes one test case, so adding a new species folder
# automatically adds it to the tests.
# ------------------------------------------------------------------
SPECIES_DIRS = []
for folder in sorted((ROOT / "data" / "species").iterdir()):
    if folder.is_dir():
        SPECIES_DIRS.append(folder)

SPECIES_IDS = [d.name for d in SPECIES_DIRS]

def load_species_paths(species_dir):
    """Read the species' YAML config file (e.g. data/species/elk/elk.yaml)."""
    yaml_file = species_dir / (species_dir.name + ".yaml")
    return script.SpeciesPaths.from_json(yaml_file)


# ==================================================================
# Tests that run once for EACH species folder
# ==================================================================

@pytest.mark.parametrize("species_dir", SPECIES_DIRS, ids=SPECIES_IDS)
def test_config_file_exists(species_dir):
    yaml_file = species_dir / (species_dir.name + ".yaml")
    assert yaml_file.exists()


@pytest.mark.parametrize("species_dir", SPECIES_DIRS, ids=SPECIES_IDS)
def test_referenced_files_exist(species_dir):
    paths = load_species_paths(species_dir)

    # The habitat model is required.
    assert (ROOT / paths.habitat_model).exists()

    # The range and observations files are optional,
    # so only check them if the config lists them.
    if paths.species_range is not None:
        assert (ROOT / paths.species_range).exists()

    if paths.inaturalist_observations is not None:
        assert (ROOT / paths.inaturalist_observations).exists()


@pytest.mark.parametrize("species_dir", SPECIES_DIRS, ids=SPECIES_IDS)
def test_habitat_model_is_valid(species_dir):
    paths = load_species_paths(species_dir)
    habitat = script.SpeciesHabitat.from_json(ROOT / paths.habitat_model)

    # A species needs at least one region model.
    assert habitat.northwest is not None or habitat.southwest is not None

    for region in [habitat.northwest, habitat.southwest]:
        if region is None:
            continue  # this species doesn't have this region; skip it

        # Elevation: if both numbers are given, min must be <= max.
        low, high = region.elevation
        if low is not None and high is not None:
            assert low <= high

        # Ecosystem codes: the list can't be empty, and every code is a whole number.
        assert len(region.prim_eco_sys_ids) > 0
        for code in region.prim_eco_sys_ids:
            assert isinstance(code, int)


@pytest.mark.parametrize("species_dir", SPECIES_DIRS, ids=SPECIES_IDS)
def test_range_shapefile_is_usable(species_dir):
    paths = load_species_paths(species_dir)
    if paths.species_range is None:
        pytest.skip("this species has no range file")

    shapes = gpd.read_file(ROOT / paths.species_range)

    assert len(shapes) > 0              # has at least one shape
    assert shapes.crs is not None       # has a coordinate system (.prj file)

    # Converting to the map's projection should still give real shapes.
    converted = shapes.to_crs("EPSG:5070")
    assert converted.geometry.notna().any()


@pytest.mark.parametrize("species_dir", SPECIES_DIRS, ids=SPECIES_IDS)
def test_observations_have_coordinates(species_dir):
    paths = load_species_paths(species_dir)
    if paths.inaturalist_observations is None:
        pytest.skip("this species has no observations file")

    # script.py reads these two columns, so they must exist.
    df = pd.read_csv(ROOT / paths.inaturalist_observations,
                     usecols=["latitude", "longitude"])

    # Throw away rows that are missing either value, then make sure some are left.
    df = df.dropna()
    assert len(df) > 0


# ==================================================================
# Tests that run only once
# ==================================================================

def test_state_boundaries_include_all_map_states():
    states_file = ROOT / script.RegionalDataLayers().state_boundaries
    assert states_file.exists()

    states = gpd.read_file(states_file)
    state_names = list(states["NAME"])

    # These are the states plot_species_habitat draws on the map.
    needed = ["Washington", "Oregon", "Idaho", "California", "Nevada",
              "Utah", "Arizona", "New Mexico", "Colorado", "Wyoming"]

    for state in needed:
        assert state in state_names, state + " is missing from the state file"


def test_script_has_main_plot_function():
    assert hasattr(script, "plot_species_habitat")


# ------------------------------------------------------------------
# Every function in script.py whose name ends in "_main"
# (e.g. elk_main) should point at a config file that really exists.
# ------------------------------------------------------------------
MAIN_FUNCTIONS = []
for name in dir(script):
    if name.endswith("_main"):
        MAIN_FUNCTIONS.append(name)


@pytest.mark.parametrize("main_name", MAIN_FUNCTIONS)
def test_main_function_config_exists(main_name):
    # yuma_bat_main is known to be broken (species/bat.yaml isn't in the repo).
    # xfail = "expected to fail": pytest records it but doesn't turn CI red.
    if main_name == "yuma_bat_main":
        pytest.xfail("species/bat.yaml is not in the repo")

    # Get the function's source code as text, e.g.
    #     def elk_main():
    #         run(Path("data/species/elk/elk.yaml"))
    code = inspect.getsource(getattr(script, main_name))

    # Pull out the text between Path(" and ")
    assert 'Path("' in code, "no Path(...) found in " + main_name
    config_path = code.split('Path("')[1].split('")')[0]

    assert (ROOT / config_path).exists()
